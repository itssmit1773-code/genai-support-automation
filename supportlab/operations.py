from contextlib import closing
from pathlib import Path
import sqlite3
from statistics import quantiles


DIMENSIONS = ("category", "week", "complexity", "risk", "region", "plan")
SCHEMA = {
    **dict.fromkeys(DIMENSIONS, "TEXT"),
    **dict.fromkeys(("handle_min", "first_reply_min", "sla_min", "resolution_min"), "REAL"),
    "resolved_7d": "INTEGER",
    "reopened_7d": "INTEGER",
}
SQL = Path(__file__).resolve().parents[1] / "sql" / "operations.sql"


def summarize(rows, dimension, hourly_rate):
    if dimension not in DIMENSIONS:
        raise ValueError(f"Unknown dimension: {dimension}")
    columns = ", ".join(f"{column} {kind}" for column, kind in SCHEMA.items())
    markers = ", ".join("?" for _ in SCHEMA)
    with closing(sqlite3.connect(":memory:")) as db:
        db.row_factory = sqlite3.Row
        db.execute(f"CREATE TABLE tickets ({columns})")
        db.executemany(f"INSERT INTO tickets VALUES ({markers})",
                       (tuple(row[key] for key in SCHEMA) for row in rows))
        query = SQL.read_text(encoding="utf-8").format(
            dimension=dimension, ordering="segment" if dimension == "week" else "tickets DESC, segment")
        return [dict(row) for row in db.execute(query, {"hourly_rate": hourly_rate})]


def percentile90(values):
    if len(values) < 2:
        return values[0] if values else None
    return quantiles(values, n=10, method="inclusive")[8]


def reconcile(rows, groups, hourly_rate):
    expected = {
        "tickets": len(rows),
        "sla_met": sum(row["first_reply_min"] <= row["sla_min"] for row in rows),
        "resolved_7d": sum(row["resolved_7d"] for row in rows),
    }
    for field, count in expected.items():
        if sum(row[field] for row in groups) != count:
            raise ValueError(f"SQLite and Python disagree on {field}")
    labor = sum(row["handle_min"] for row in rows) * hourly_rate / 60
    if abs(sum(row["labor_usd"] for row in groups) - labor) > .0051 * len(groups):
        raise ValueError("SQLite and Python labor totals exceed rounding tolerance")

