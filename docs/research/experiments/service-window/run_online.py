"""Causal, charge-only synthetic replay; no market revenue or learned policy."""

import json

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

from run_baseline import CFG, ROOT, N, T, DT, CAP, SERVICE, duties


def availability(event, known_at):
    available, used = duties(False)
    if known_at >= event["announced_step"]:
        i = event["vehicle_index"]
        end = (CFG["trip_start_steps"][1] + i % CFG["vehicle_offset_modulo"]
               + CFG["trip_duration_steps"])
        available[i, end:end + event["delay_steps"]] = False
    return available, used


def plan(now, energy, available, used, service_cap):
    horizon = T - now
    c, on = np.arange(2 * N * horizon).reshape(2, N, horizon)
    e = np.arange(2 * N * horizon,
                  2 * N * horizon + N * (horizon + 1)).reshape(N, horizon + 1)
    size = int(e.max() + 1)
    lb, ub = np.zeros(size), np.full(size, np.inf)
    ub[c] = CFG["charge_kw_per_vehicle"] * available[:, now:]
    ub[on] = available[:, now:]
    lb[e], ub[e] = CFG["soc_min"] * CAP, CFG["soc_max"] * CAP
    lb[e[:, 0]] = ub[e[:, 0]] = energy
    lb[e[:, -1]] = CFG["terminal_soc_min"] * CAP
    rows, cols, values, lo, hi = [], [], [], [], []

    def add(terms, lower=-np.inf, upper=np.inf):
        row = len(lo)
        for index, value in terms:
            rows.append(row)
            cols.append(int(index))
            values.append(value)
        lo.append(lower)
        hi.append(upper)

    for i in range(N):
        for k in range(horizon):
            add([(e[i, k + 1], 1), (e[i, k], -1),
                 (c[i, k], -CFG["charge_efficiency"] * DT)],
                -used[i, now + k], -used[i, now + k])
            add([(c[i, k], 1),
                 (on[i, k], -CFG["charge_kw_per_vehicle"])], upper=0)
    for k in range(horizon):
        t = now + k
        limit = service_cap if SERVICE[t] else CFG["site_import_headroom_kw"]
        add([(c[i, k], 1) for i in range(N)], upper=limit)
        add([(on[i, k], 1) for i in range(N)], upper=CFG["connectors"])
    matrix = coo_matrix((values, (rows, cols)), shape=(len(lo), size)).tocsc()
    objective = np.zeros(size)
    # Synthetic preference for earlier replenishment, not an electricity tariff.
    objective[c] = DT * (1 + np.arange(now, T) / T)
    integer = np.zeros(size)
    integer[on] = 1
    result = milp(objective, integrality=integer, bounds=Bounds(lb, ub),
                  constraints=LinearConstraint(matrix, lo, hi),
                  options={"time_limit": 20, "mip_rel_gap": 1e-7})
    if result.status != 0:
        raise RuntimeError(f"step {now}: {result.message}")
    return result.x[c]


def replay(event, service_cap, foresight=False):
    actual_available, actual_used = availability(event, T)
    energy = np.full(N, CFG["initial_soc"] * CAP)
    states, actions, observed = [energy.copy()], [], []
    for now in range(T):
        known_at = T if foresight else now
        predicted_available, predicted_used = availability(event, known_at)
        action = plan(now, energy, predicted_available, predicted_used, service_cap)[:, 0]
        # Execute only the current action. Past actions are never re-solved.
        assert np.max(action[~actual_available[:, now]], initial=0) < 1e-5
        energy = energy + CFG["charge_efficiency"] * action * DT - actual_used[:, now]
        actions.append(action)
        states.append(energy.copy())
        observed.append(foresight or now >= event["announced_step"])
    charge, states = np.array(actions).T, np.array(states).T
    grid = charge.sum(axis=0)
    # Independent replay checks against actual duties and hardware.
    assert states.min() >= CFG["soc_min"] * CAP - 1e-5
    assert states.max() <= CFG["soc_max"] * CAP + 1e-5
    assert states[:, -1].min() >= CFG["terminal_soc_min"] * CAP - 1e-5
    assert np.max(charge) <= CFG["charge_kw_per_vehicle"] + 1e-5
    assert np.max((charge > 1e-5).sum(axis=0)) <= CFG["connectors"]
    assert grid.max() <= CFG["site_import_headroom_kw"] + 1e-5
    assert grid[SERVICE].max() <= service_cap + 1e-5
    error = (states[:, -1] - states[:, 0]
             - CFG["charge_efficiency"] * charge.sum(axis=1) * DT
             + actual_used.sum(axis=1))
    assert np.max(np.abs(error)) < 1e-5
    return {
        "event": event, "perfect_foresight": foresight,
        "service_import_cap_kw": service_cap,
        "charge_kwh": float(charge.sum() * DT),
        "service_charge_kwh": float(grid[SERVICE].sum() * DT),
        "post_service_charge_kwh": float(grid[np.where(SERVICE)[0][-1] + 1:].sum() * DT),
        "peak_import_kw": float(grid.max()),
        "min_soc": float(states.min() / CAP),
        "min_terminal_soc": float(states[:, -1].min() / CAP),
        "max_energy_balance_error_kwh": float(np.max(np.abs(error))),
        "charge_kw_by_vehicle_step": charge.tolist(),
        "soc_by_vehicle_boundary": (states / CAP).tolist(),
        "event_known_by_step": observed,
    }


def main():
    # Vehicle 5's second trip normally returns at step 17 (14:30).
    # At step 16 (14:00), a revised return is announced. No extra traction
    # energy is assumed; this is a stationary waiting delay, with existing aux.
    event = {"vehicle_index": 4, "announced_step": 16, "delay_steps": 3}
    alternative = dict(event, delay_steps=1)
    online = replay(event, 300)
    paired = replay(alternative, 300)
    a = np.array(online["charge_kw_by_vehicle_step"])
    b = np.array(paired["charge_kw_by_vehicle_step"])
    prefix_error = float(np.max(np.abs(a[:, :event["announced_step"]]
                                           - b[:, :event["announced_step"]])))
    assert prefix_error < 1e-5
    # This event changes only future availability when it becomes known.
    nominal, _ = duties(False)
    actual, _ = availability(event, T)
    assert np.array_equal(nominal[:, :16], actual[:, :16])
    result = {
        "data_status": "synthetic_causality_check_not_research_validation",
        "objective": "earlier_charge_preference_not_money",
        "online": online,
        "paired_short_delay": paired,
        "unrestricted_online": replay(event, CFG["site_import_headroom_kw"]),
        "perfect_foresight_reference": replay(event, 300, True),
        "nonanticipation_prefix_max_difference_kw": prefix_error,
        "limitations": ["fixed trips, no task reassignment", "no battery swapping or V2G",
                        "known delay duration after announcement", "no extra driving energy",
                        "no infeasibility recovery or statistical reliability claim"],
    }
    (ROOT / "online_results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({name: {key: case[key] for key in (
        "charge_kwh", "service_charge_kwh", "post_service_charge_kwh",
        "min_soc", "min_terminal_soc")} for name, case in result.items()
        if isinstance(case, dict)}, indent=2))
    print("nonanticipation_prefix_max_difference_kw", prefix_error)


if __name__ == "__main__":
    main()
