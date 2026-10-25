"""Compare hypothetical storage and planned departure flexibility."""

import json

from run_baseline import CFG, ROOT, solve, write_schedule


def main():
    results = {"data_status": "synthetic_perfect_foresight_mechanism_comparisons"}
    storage_cases = []
    for capacity, power in [(0, 0), (200, 300), (500, 100), (500, 300), (2000, 100), (2000, 300)]:
        solved = solve(True, storage_kwh=capacity, storage_kw=power)
        assert isinstance(solved, tuple), solved
        polished = solve(True, required_kw=max(0, solved[0]["constant_export_kw"] - 1e-6),
                         throughput_only=True, storage_kwh=capacity, storage_kw=power)
        assert isinstance(polished, tuple), polished
        storage_cases.append({"capacity_kwh": capacity, "power_kw": power, **polished[0]})
        if capacity == 2000 and power == 300:
            write_schedule("delayed_storage_2000_300", polished)
    results["storage_cases"] = storage_cases
    original_discharge = CFG["discharge_kw_per_vehicle"]
    CFG["discharge_kw_per_vehicle"] = 0
    storage_only = []
    for power in [300, 500]:
        solved = solve(True, storage_kwh=2000, storage_kw=power)
        assert isinstance(solved, tuple), solved
        storage_only.append({"truck_discharge_kw": 0, **solved[0]})
    CFG["discharge_kw_per_vehicle"] = original_discharge
    results["storage_with_unidirectional_trucks"] = storage_only
    shift_cases = []
    for window in [0, 1, 2, 3]:
        solved = solve(True, shift_steps=window)
        assert isinstance(solved, tuple), solved
        if window:
            solved = solve(True, required_kw=max(0, solved[0]["constant_export_kw"] - 1e-6),
                           shift_steps=window, minimize_shift=True)
            assert isinstance(solved, tuple), solved
        shift_cases.append({"allowed_shift_minutes_each_way": window * 30, **solved[0]})
        if window == 2:
            write_schedule("delayed_departure_flex_60", solved)
    results["planned_departure_flexibility"] = shift_cases
    results["limitations"] = (
        "All cases know the 90-minute return delay before planning. Shifts apply only to the "
        "second trip; no task reassignment, driver cost or real customer windows. Storage has a "
        "separate converter, no truck-connector use, no other duty, and initial/terminal SOC 80%. "
        "Not an online recovery, cost comparison, real site, reserve product or outage simulation.")
    (ROOT / "comparison_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    for row in storage_cases:
        print("storage", row["capacity_kwh"], row["power_kw"], row["constant_export_kw"])
    for row in shift_cases:
        print("shift", row["allowed_shift_minutes_each_way"], row["constant_export_kw"],
              row.get("total_absolute_shift_minutes", 0), row.get("departure_shift_minutes_by_vehicle", []))
    for row in storage_only:
        print("storage_without_truck_v2g", row["storage"]["power_kw"], row["constant_export_kw"])


if __name__ == "__main__":
    main()
