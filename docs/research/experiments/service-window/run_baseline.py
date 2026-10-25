"""Synthetic fixed-duty feasibility experiment; not a real-fleet V2G model."""

import csv
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
N, T = CFG["fleet_size"], CFG["steps"]
DT, CAP = CFG["time_step_hours"], CFG["battery_kwh"]
HOURS = CFG["start_hour"] + np.arange(T) * DT
SERVICE = (HOURS >= CFG["service_start_hour"]) & (HOURS < CFG["service_end_hour"])
C, D, UC, UD = np.arange(4 * N * T).reshape(4, N, T)
E = np.arange(4 * N * T, 4 * N * T + N * (T + 1)).reshape(N, T + 1)
R = int(E.max() + 1)
SIZE = R + 1


def duties(delayed, shifts=None):
    available = np.ones((N, T), dtype=bool)
    used = np.full((N, T), CFG["auxiliary_kw_per_vehicle"] * DT)
    for i in range(N):
        offset = i % CFG["vehicle_offset_modulo"]
        for trip, base in enumerate(CFG["trip_start_steps"]):
            start = base + offset
            if trip == 1 and shifts is not None:
                start += shifts[i]
            end = start + CFG["trip_duration_steps"]
            available[i, start:end] = False
            used[i, start:end] += CFG["trip_energy_kwh"] / CFG["trip_duration_steps"]
            if delayed and trip == 1:
                available[i, end:end + CFG["delay_steps"]] = False
    return available, used


def solve(delayed=False, required_kw=None, throughput_only=False,
          storage_kwh=0, storage_kw=0, shift_steps=0, minimize_shift=False):
    available, used = duties(delayed)
    choices = list(range(-shift_steps, shift_steps + 1)) if shift_steps else []
    size = SIZE
    if storage_kwh:
        SC, SD, SM = np.arange(size, size + 3 * T).reshape(3, T)
        SE = np.arange(size + 3 * T, size + 4 * T + 1)
        size += 4 * T + 1
    if choices:
        Q = np.arange(size, size + N * len(choices)).reshape(N, len(choices))
        size += Q.size
        # Remove the second trip from fixed consumption and availability.
        for i in range(N):
            offset = i % CFG["vehicle_offset_modulo"]
            start = CFG["trip_start_steps"][1] + offset
            end = start + CFG["trip_duration_steps"]
            used[i, start:end] -= CFG["trip_energy_kwh"] / CFG["trip_duration_steps"]
            available[i, start:end + (CFG["delay_steps"] if delayed else 0)] = True
    lb, ub = np.zeros(size), np.full(size, np.inf)
    ub[C] = CFG["charge_kw_per_vehicle"] * available
    ub[D] = CFG["discharge_kw_per_vehicle"] * available * SERVICE
    ub[UC], ub[UD] = available, available * SERVICE
    lb[E], ub[E] = CFG["soc_min"] * CAP, CFG["soc_max"] * CAP
    lb[E[:, 0]] = ub[E[:, 0]] = CFG["initial_soc"] * CAP
    lb[E[:, -1]] = CFG["terminal_soc_min"] * CAP
    ub[R] = CFG["site_export_limit_kw"]
    if required_kw is not None:
        lb[R] = required_kw
    integrality = np.zeros(size, dtype=np.int32)
    integrality[UC], integrality[UD] = 1, 1
    if storage_kwh:
        ub[SC], ub[SD], ub[SM] = storage_kw, storage_kw * SERVICE, 1
        integrality[SM] = 1
        lb[SE], ub[SE] = 0.2 * storage_kwh, 0.9 * storage_kwh
        lb[SE[0]] = ub[SE[0]] = 0.8 * storage_kwh
        lb[SE[-1]] = 0.8 * storage_kwh
    if choices:
        ub[Q], integrality[Q] = 1, 1
    rows, cols, vals, lower, upper = [], [], [], [], []

    def add(terms, lo=-np.inf, hi=np.inf):
        row = len(lower)
        for index, value in terms:
            rows.append(row)
            cols.append(int(index))
            vals.append(value)
        lower.append(lo)
        upper.append(hi)

    for i in range(N):
        if choices:
            add([(q, 1) for q in Q[i]], 1, 1)
        for t in range(T):
            energy_terms = [(E[i, t + 1], 1), (E[i, t], -1),
                 (C[i, t], -CFG["charge_efficiency"] * DT),
                 (D[i, t], DT / CFG["discharge_efficiency"])]
            busy_terms = []
            if choices:
                for j, shift in enumerate(choices):
                    start = CFG["trip_start_steps"][1] + i % CFG["vehicle_offset_modulo"] + shift
                    end = start + CFG["trip_duration_steps"]
                    if start <= t < end:
                        energy_terms.append((Q[i, j], CFG["trip_energy_kwh"] / CFG["trip_duration_steps"]))
                    if start <= t < end + (CFG["delay_steps"] if delayed else 0):
                        busy_terms.append((Q[i, j], 1))
            add(energy_terms, -used[i, t], -used[i, t])
            add([(C[i, t], 1), (UC[i, t], -CFG["charge_kw_per_vehicle"])], hi=0)
            add([(D[i, t], 1), (UD[i, t], -CFG["discharge_kw_per_vehicle"])], hi=0)
            add([(UC[i, t], 1), (UD[i, t], 1)] + busy_terms, hi=1)
    for t in range(T):
        add([(UC[i, t], 1) for i in range(N)] + [(UD[i, t], 1) for i in range(N)],
            hi=CFG["connectors"])
        grid_terms = [(C[i, t], 1) for i in range(N)] + [(D[i, t], -1) for i in range(N)]
        if storage_kwh:
            add([(SE[t + 1], 1), (SE[t], -1), (SC[t], -0.95 * DT),
                 (SD[t], DT / 0.95)], 0, 0)
            add([(SC[t], 1), (SM[t], -storage_kw)], hi=0)
            add([(SD[t], 1), (SM[t], storage_kw)], hi=storage_kw)
            grid_terms += [(SC[t], 1), (SD[t], -1)]
        add(grid_terms, -CFG["site_export_limit_kw"], CFG["site_import_headroom_kw"])
        if SERVICE[t]:
            add(grid_terms + [(R, 1)], hi=0)
    matrix = coo_matrix((vals, (rows, cols)), shape=(len(lower), size)).tocsc()
    objective = np.zeros(size)
    if minimize_shift:
        objective[Q] = np.abs(choices) * DT * 60
    elif throughput_only:
        objective[C], objective[D] = DT, DT
        if storage_kwh:
            objective[SC], objective[SD] = DT, DT
    else:
        objective[R] = -1
    result = milp(objective, integrality=integrality, bounds=Bounds(lb, ub),
                  constraints=LinearConstraint(matrix, lower, upper),
                  options={"time_limit": 45, "mip_rel_gap": 1e-7})
    if result.status != 0:
        return {"status": int(result.status), "message": result.message}
    x = result.x
    residual = matrix @ x
    violation = max(float(np.max(np.maximum(np.array(lower) - residual, 0))),
                    float(np.max(np.maximum(residual - np.array(upper), 0))),
                    float(np.max(np.maximum(lb - x, 0))),
                    float(np.max(np.maximum(x - ub, 0))))
    assert violation < 1e-5, violation
    assert np.max(np.abs(x[UC] - np.round(x[UC]))) < 1e-5
    assert np.max(np.abs(x[UD] - np.round(x[UD]))) < 1e-5
    charge, discharge = x[C], x[D]
    selected_shifts = [0] * N
    if choices:
        assert np.max(np.abs(x[Q] - np.round(x[Q]))) < 1e-5
        selected_shifts = [choices[int(np.argmax(x[Q[i]]))] for i in range(N)]
        available, used = duties(delayed, selected_shifts)
    assert np.max(charge[~available], initial=0) < 1e-5
    assert np.max(discharge[~available], initial=0) < 1e-5
    energy_error = (x[E[:, -1]] - x[E[:, 0]]
                    - CFG["charge_efficiency"] * charge.sum(axis=1) * DT
                    + discharge.sum(axis=1) * DT / CFG["discharge_efficiency"]
                    + used.sum(axis=1))
    assert np.max(np.abs(energy_error)) < 1e-5
    summary = {
        "status": 0, "constant_export_kw": round(float(x[R]), 6),
        "service_energy_kwh": round(float(x[R]) * SERVICE.sum() * DT, 6),
        "charge_kwh": round(float(charge.sum() * DT), 6),
        "discharge_kwh": round(float(discharge.sum() * DT), 6),
        "min_soc": round(float(x[E].min() / CAP), 6),
        "min_terminal_soc": round(float(x[E[:, -1]].min() / CAP), 6),
        "max_constraint_violation": violation,
        "max_energy_balance_error_kwh": float(np.max(np.abs(energy_error))),
        "mip_gap": float(result.mip_gap),
    }
    if storage_kwh:
        assert np.max(np.abs(x[SM] - np.round(x[SM]))) < 1e-5
        storage_error = (x[SE[-1]] - x[SE[0]] - 0.95 * x[SC].sum() * DT
                         + x[SD].sum() * DT / 0.95)
        assert abs(storage_error) < 1e-5
        summary["storage"] = {
            "capacity_kwh": storage_kwh, "power_kw": storage_kw,
            "charge_kwh": float(x[SC].sum() * DT),
            "discharge_kwh": float(x[SD].sum() * DT),
            "terminal_soc": float(x[SE[-1]] / storage_kwh),
            "energy_balance_error_kwh": float(storage_error),
            "charge_kw_by_step": x[SC].tolist(),
            "discharge_kw_by_step": x[SD].tolist(),
            "soc_by_boundary": (x[SE] / storage_kwh).tolist(),
        }
    if choices:
        summary["departure_shift_minutes_by_vehicle"] = [s * DT * 60 for s in selected_shifts]
        summary["total_absolute_shift_minutes"] = sum(abs(s) for s in selected_shifts) * DT * 60
    return summary, x, available, used


def write_schedule(name, solved):
    summary, x, available, used = solved
    with (ROOT / f"{name}_schedule.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["vehicle", "hour", "available", "consumed_kwh", "charge_kw",
                         "discharge_kw", "soc_start", "soc_end"])
        for i in range(N):
            for t in range(T):
                writer.writerow([i + 1, HOURS[t], int(available[i, t]), used[i, t],
                                 round(x[C[i, t]], 6), round(x[D[i, t]], 6),
                                 round(x[E[i, t]] / CAP, 6), round(x[E[i, t + 1]] / CAP, 6)])


def main():
    summaries = {}
    for name, delayed in [("nominal", False), ("delayed", True)]:
        maximum = solve(delayed)
        assert isinstance(maximum, tuple), maximum
        # Second solve minimizes throughput while retaining maximum service.
        polished = solve(delayed, max(0, maximum[0]["constant_export_kw"] - 1e-6), True)
        assert isinstance(polished, tuple), polished
        write_schedule(name, polished)
        summaries[name] = polished[0]
    impossible = solve(True, summaries["nominal"]["constant_export_kw"] - 1e-5)
    summaries["delayed_with_nominal_commitment"] = (
        impossible[0] if isinstance(impossible, tuple) else impossible)
    no_service = solve(False, 0, True)
    assert isinstance(no_service, tuple), no_service
    assert no_service[0]["discharge_kwh"] < 1e-5
    summaries["no_service_energy_check"] = no_service[0]
    sensitivity = []
    original_delay = CFG["delay_steps"]
    for delay in range(4):
        CFG["delay_steps"] = delay
        solved = solve(True)
        assert isinstance(solved, tuple), solved
        availability = solved[2][:, SERVICE].sum(axis=0)
        sensitivity.append({
            "delay_minutes": delay * DT * 60,
            "constant_export_kw": solved[0]["constant_export_kw"],
            "available_vehicles_per_service_step": availability.tolist(),
            "connector_power_upper_kw": float(min(CFG["connectors"], availability.min())
                                                * CFG["discharge_kw_per_vehicle"]),
        })
    CFG["delay_steps"] = original_delay
    summaries["return_delay_sensitivity"] = sensitivity
    original_discharge = CFG["discharge_kw_per_vehicle"]
    CFG["discharge_kw_per_vehicle"] = 0
    unidirectional = solve()
    assert isinstance(unidirectional, tuple), unidirectional
    assert unidirectional[0]["constant_export_kw"] < 1e-5
    CFG["discharge_kw_per_vehicle"] = original_discharge
    summaries["unidirectional_export_check"] = unidirectional[0]
    summaries["interpretation"] = (
        "Synthetic fixed-duty deterministic upper bounds with assumed bidirectional hardware. "
        "Each case knows its full duties. Not an online algorithm, reserve product or market revenue. "
        "No stationary storage, PV, network voltage or task reassignment included.")
    (ROOT / "results.json").write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
