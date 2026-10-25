"""Request sensitivity and frozen-plan replay under the same synthetic duties."""

import json

import numpy as np

import run_online as online
from run_baseline import CFG, ROOT, N, T, DT, CAP, HOURS


EVENT = {"vehicle_index": 4, "announced_step": 16, "delay_steps": 3}


def frozen(service_cap):
    available, used = online.availability(EVENT, -1)
    scheduled = online.plan(0, np.full(N, CFG["initial_soc"] * CAP),
                            available, used, service_cap)
    actual, used = online.availability(EVENT, T)
    # Explicit baseline: cancel impossible charging, do not move or replace it.
    executed = scheduled * actual
    states = np.zeros((N, T + 1))
    states[:, 0] = CFG["initial_soc"] * CAP
    for t in range(T):
        states[:, t + 1] = (states[:, t] + CFG["charge_efficiency"] * executed[:, t] * DT
                            - used[:, t])
    grid = executed.sum(axis=0)
    error = (states[:, -1] - states[:, 0]
             - CFG["charge_efficiency"] * executed.sum(axis=1) * DT + used.sum(axis=1))
    assert np.max(np.abs(error)) < 1e-5
    assert np.max((executed > 1e-5).sum(axis=0)) <= CFG["connectors"]
    assert grid.max() <= CFG["site_import_headroom_kw"] + 1e-5
    assert grid[online.SERVICE].max() <= service_cap + 1e-5
    terminal_deficit = np.maximum(CFG["terminal_soc_min"] * CAP - states[:, -1], 0)
    return {
        "policy": "freeze_nominal_plan_cancel_unavailable_charge_no_repair",
        "charge_kwh": float(executed.sum() * DT),
        "cancelled_charge_kwh": float((scheduled - executed).sum() * DT),
        "terminal_deficit_kwh": float(terminal_deficit.sum()),
        "min_terminal_soc": float(states[:, -1].min() / CAP),
        "min_soc": float(states.min() / CAP),
        "soc_lower_violation_kwh": float(max(0, CFG["soc_min"] * CAP - states.min())),
        "soc_upper_violation_kwh": float(max(0, states.max() - CFG["soc_max"] * CAP)),
        "charge_kw_by_vehicle_step": executed.tolist(),
    }


def compact(case):
    grid = np.array(case["charge_kw_by_vehicle_step"]).sum(axis=0)
    mask = online.SERVICE
    last = np.where(mask)[0][-1]
    return {"charge_kwh": case["charge_kwh"],
            "window_charge_kwh": float(grid[mask].sum() * DT),
            "window_peak_kw": float(grid[mask].max()),
            "post_window_charge_kwh": float(grid[last + 1:].sum() * DT),
            "post_window_peak_kw": float(grid[last + 1:].max(initial=0)),
            "min_soc": case["min_soc"],
            "min_terminal_soc": case["min_terminal_soc"]}


def main():
    original = online.SERVICE.copy()
    rows, details = [], []
    try:
        for start, end in [(14, 16), (12, 18), (6, 22)]:
            online.SERVICE = (HOURS >= start) & (HOURS < end)
            unrestricted = online.replay(EVENT, 600)
            reference = compact(unrestricted)
            for cap in [0, 100, 300, 600]:
                record = {"window": [start, end], "import_cap_kw": cap,
                          "unrestricted_reference": reference}
                try:
                    rolling = online.replay(EVENT, cap)
                    fixed = frozen(cap)
                except RuntimeError as error:
                    # Preserve solver wording: infeasible and time-limit differ.
                    record.update(status="solve_failed", solver_message=str(error))
                else:
                    metrics = compact(rolling)
                    baseline = {k: v for k, v in fixed.items()
                                if k != "charge_kw_by_vehicle_step"}
                    record.update(status="verified_replay", rolling=metrics, frozen=baseline)
                    record["window_energy_reduction_vs_reference_kwh"] = (
                        reference["window_charge_kwh"] - metrics["window_charge_kwh"])
                    record["post_window_extra_charge_vs_reference_kwh"] = (
                        metrics["post_window_charge_kwh"] - reference["post_window_charge_kwh"])
                    details.append({"window": [start, end], "import_cap_kw": cap,
                                    "rolling": rolling, "frozen": fixed})
                rows.append(record)
                print(json.dumps(record), flush=True)
    finally:
        online.SERVICE = original
    result = {"data_status": "synthetic_sensitivity_not_market_baseline",
              "event": EVENT, "rows": rows, "details": details,
              "interpretation": "Frozen cancellation is a diagnostic baseline, not a strong repaired policy."}
    (ROOT / "request_scan_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
