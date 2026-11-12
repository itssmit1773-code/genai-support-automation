"""Rebuild the complete set of evidence files from seed and configuration."""
import argparse
import csv
import json
from pathlib import Path
from statistics import mean

from .data import generate, challenge_cases
from .finance import Assumptions, Unit, calculate, sensitivity
from .operations import DIMENSIONS, percentile90, reconcile, summarize
from .triage import POLICIES, evaluate, fit, metrics, reliability, replay


ROOT = Path(__file__).resolve().parents[1]


def load_config():
    return json.loads((ROOT / "config" / "assumptions.json").read_text(encoding="utf-8"))


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def policy_economics(scores, policy, config, **overrides):
    shared = config["shared"] | overrides
    cost = config["policy_costs"][policy]
    assumptions = Assumptions(**shared, setup=cost["setup"], fixed_monthly=cost["fixed_monthly"])
    unit = Unit(scores["baseline_minutes"], scores["modeled_minutes"], cost["processing_cost"])
    return unit, assumptions


def run(output):
    output.mkdir(parents=True, exist_ok=True)
    config = load_config()
    rows = generate(config["seed"])
    write_csv(output / "tickets.csv", rows)
    engine, threshold, fit_report = fit(rows)
    test = [row for row in rows if row["split"] == "test"]
    benchmark = {}
    details, challenge_results, group_results = [], [], []
    economics, grids = {}, []
    challenge = challenge_cases()
    case_names = {row["ticket_id"]: row["case"] for row in challenge}
    write_csv(output / "challenge_labels.csv", challenge)
    for policy in POLICIES:
        result = list(replay(test, engine, threshold, policy, config["replay"]))
        details.extend(result)
        scores = metrics(result)
        benchmark[policy] = scores
        for dimension in ("risk", "region", "expected_article"):
            for value in sorted({row[dimension] for row in result}):
                cohort = [row for row in result if row[dimension] == value]
                group_results.append({"policy": policy, "dimension": dimension, "segment": value,
                                      **metrics(cohort)})
        for row in replay(challenge, engine, threshold, policy, config["replay"]):
            challenge_results.append({"case": case_names[row["ticket_id"]], **row})
        unit, assumptions = policy_economics(scores, policy, config)
        economics[policy] = calculate(unit, assumptions)
        grids.extend({"policy": policy, **row} for row in sensitivity(unit, assumptions))
    write_csv(output / "test_decisions.csv", details)
    write_csv(output / "challenge_decisions.csv", challenge_results)
    write_csv(output / "evaluation_slices.csv", group_results)
    write_csv(output / "financial_sensitivity.csv", grids)
    rate = config["shared"]["hourly_rate"]
    for dimension in DIMENSIONS:
        groups = summarize(rows, dimension, rate)
        reconcile(rows, groups, rate)
        write_csv(output / f"operations_by_{dimension}.csv", groups)
    report = {
        "synthetic": True,
        "operations": {
            "tickets": len(rows), "months": 3,
            "avg_handle_min": mean(row["handle_min"] for row in rows),
            "sla_pct": 100 * mean(row["first_reply_min"] <= row["sla_min"] for row in rows),
            "resolution_pct": 100 * mean(row["resolved_7d"] for row in rows),
            "reply_p90_min": percentile90([row["first_reply_min"] for row in rows]),
            "labor_usd": sum(row["handle_min"] for row in rows) / 60 * rate,
        },
        "fit": fit_report, "test_calibration": reliability(test, engine),
        "benchmark": benchmark, "economics": economics,
    }
    write_json(output / "summary.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence")
    args = parser.parse_args()
    result = run(args.output)
    print(f"Wrote reproducible evidence for {result['operations']['tickets']:,} synthetic tickets to {args.output}")

