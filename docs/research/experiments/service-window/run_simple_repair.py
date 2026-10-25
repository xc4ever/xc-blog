"""Repay cancelled charging using spare capacity, without online optimization."""

import json

import numpy as np

import run_online as online
from run_baseline import CFG, ROOT, N, T, DT, CAP, HOURS
from run_request_scan import EVENT, compact


def repair(event, cap):
    nominal, used = online.availability(event, -1)
    scheduled = online.plan(0, np.full(N, CFG["initial_soc"] * CAP), nominal, used, cap)
    actual, _ = online.availability(event, T)
    energy = np.full(N, CFG["initial_soc"] * CAP)
    debt = np.zeros(N)  # Cancelled AC-side energy, kWh.
    states, actions, debts = [energy.copy()], [], []
    for t in range(T):
        known, _ = online.availability(event, t)
        assert np.array_equal(known[:, t], actual[:, t])
        limit = cap if online.SERVICE[t] else CFG["site_import_headroom_kw"]
        headroom_kw = np.maximum(0, (CFG["soc_max"] * CAP - energy + used[:, t])
                                  / (CFG["charge_efficiency"] * DT))
        action = np.minimum(scheduled[:, t] * known[:, t], headroom_kw)
        action[action < 1e-7] = 0
        debt += (scheduled[:, t] - action) * DT
        debt = np.maximum(debt, 0)
        # Preserve scheduled charging first. Largest accumulated loss has priority;
        # vehicle index breaks ties. This uses no future event information.
        for i in sorted(range(N), key=lambda i: (-debt[i], i)):
            if not known[i, t] or debt[i] < 1e-7:
                continue
            if action[i] < 1e-7 and (action > 1e-7).sum() >= CFG["connectors"]:
                continue
            extra = max(0, min(debt[i] / DT, limit - action.sum(),
                               CFG["charge_kw_per_vehicle"] - action[i],
                               headroom_kw[i] - action[i]))
            action[i] += extra
            debt[i] = max(0, debt[i] - extra * DT)
        energy = energy + CFG["charge_efficiency"] * action * DT - used[:, t]
        actions.append(action.copy())
        states.append(energy.copy())
        debts.append(debt.copy())
    charge, states = np.array(actions).T, np.array(states).T
    grid = charge.sum(axis=0)
    assert np.max(charge[~actual], initial=0) < 1e-5
    assert charge.min() >= -1e-5
    assert charge.max() <= CFG["charge_kw_per_vehicle"] + 1e-5
    assert (charge > 1e-5).sum(axis=0).max() <= CFG["connectors"]
    assert grid.max() <= CFG["site_import_headroom_kw"] + 1e-5
    assert grid[online.SERVICE].max() <= cap + 1e-5
    error = (states[:, -1] - states[:, 0]
             - CFG["charge_efficiency"] * charge.sum(axis=1) * DT + used.sum(axis=1))
    assert np.max(np.abs(error)) < 1e-5
    deficit = np.maximum(0, CFG["terminal_soc_min"] * CAP - states[:, -1])
    lower = float(max(0, CFG["soc_min"] * CAP - states.min()))
    upper = float(max(0, states.max() - CFG["soc_max"] * CAP))
    return {"policy": "nominal_plan_then_largest_charge_debt_first",
            "charge_kwh": float(charge.sum() * DT),
            "min_soc": float(states.min() / CAP),
            "min_terminal_soc": float(states[:, -1].min() / CAP),
            "terminal_deficit_kwh": float(deficit.sum()),
            "unrepaid_charge_kwh": float(debt.sum()),
            "soc_lower_violation_kwh": lower, "soc_upper_violation_kwh": upper,
            "feasible": bool(deficit.max() < 1e-5 and lower < 1e-5 and upper < 1e-5),
            "max_energy_balance_error_kwh": float(np.max(np.abs(error))),
            "charge_kw_by_vehicle_step": charge.tolist(),
            "soc_by_vehicle_boundary": (states / CAP).tolist(),
            "charge_debt_kwh_by_step": np.array(debts).tolist()}


def main():
    scan = json.loads((ROOT / "request_scan_results.json").read_text())
    rows, details = [], []
    original = online.SERVICE.copy()
    try:
        for previous in scan["rows"]:
            if previous["status"] != "verified_replay":
                continue  # Same nominal planning infeasibility, not a rule failure.
            start, end = previous["window"]
            cap = previous["import_cap_kw"]
            online.SERVICE = (HOURS >= start) & (HOURS < end)
            case = repair(EVENT, cap)
            metrics = compact(case)
            for key in ["feasible", "terminal_deficit_kwh", "unrepaid_charge_kwh",
                        "soc_lower_violation_kwh", "soc_upper_violation_kwh"]:
                metrics[key] = case[key]
            row = {"window": [start, end], "import_cap_kw": cap,
                   "simple_repair": metrics, "rolling": previous["rolling"]}
            rows.append(row)
            details.append({"window": [start, end], "import_cap_kw": cap, "repair": case})
            print(json.dumps(row), flush=True)
        online.SERVICE = (HOURS >= 14) & (HOURS < 16)
        long = repair(EVENT, 300)
        short = repair(dict(EVENT, delay_steps=1), 300)
        a, b = [np.array(x["charge_kw_by_vehicle_step"]) for x in [long, short]]
        prefix = float(np.max(np.abs(a[:, :16] - b[:, :16])))
        assert prefix < 1e-5
    finally:
        online.SERVICE = original
    result = {"rows": rows, "details": details,
              "nonanticipation_prefix_max_difference_kw": prefix,
              "limitations": ["one nominal MILP, no online optimization",
                              "repays lost charge, does not adapt tasks or energy forecasts",
                              "fixed vehicle ordering can affect peak and timing"]}
    (ROOT / "simple_repair_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("feasible", sum(x["simple_repair"]["feasible"] for x in rows), "/", len(rows))


if __name__ == "__main__":
    main()
