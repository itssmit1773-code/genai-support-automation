"""Incremental economics relative to continuing manual support, in USD."""
from dataclasses import dataclass, replace
from math import ceil, isfinite


@dataclass(frozen=True)
class Unit:
    baseline_minutes: float
    modeled_minutes: float
    processing_cost: float


@dataclass(frozen=True)
class Assumptions:
    monthly_volume: int = 4000
    hourly_rate: float = 36
    realization: float = .65
    adoption: float = .85
    setup: float = 4200
    fixed_monthly: float = 230
    ramp_months: int = 4


def calculate(unit, assumptions):
    a = assumptions
    nonnegative = (a.monthly_volume, a.hourly_rate, a.setup, a.fixed_monthly, a.ramp_months,
                   unit.baseline_minutes, unit.modeled_minutes, unit.processing_cost)
    if any(not isfinite(value) or value < 0 for value in nonnegative):
        raise ValueError("Volume, time and cost inputs must be finite and nonnegative")
    if not 0 <= a.adoption <= 1 or not 0 <= a.realization <= 1:
        raise ValueError("Adoption and realization must be fractions between zero and one")
    minutes_saved = unit.baseline_minutes - unit.modeled_minutes
    gross_per_ticket = minutes_saved * a.hourly_rate / 60
    # Additional labor is charged in full. Only saved capacity receives the haircut.
    benefit_per_ticket = gross_per_ticket * a.realization if gross_per_ticket > 0 else gross_per_ticket
    margin = benefit_per_ticket - unit.processing_cost
    cash_flows = [{"month": 0, "adopted_tickets": 0, "capacity_hours": 0,
                   "realized_value": 0, "run_cost": 0, "net": -a.setup, "cumulative": -a.setup}]
    cumulative = -a.setup
    payback = 0 if not a.setup else None
    for month in range(1, 25):
        ramp = min(1, month / a.ramp_months) if a.ramp_months else 1
        tickets = a.monthly_volume * a.adoption * ramp
        benefit = tickets * benefit_per_ticket
        cost = a.fixed_monthly + tickets * unit.processing_cost
        net = benefit - cost
        cumulative += net
        if cumulative < 0:
            payback = None
        elif payback is None:
            payback = month
        cash_flows.append({"month": month, "adopted_tickets": tickets,
                           "capacity_hours": tickets * minutes_saved / 60,
                           "realized_value": benefit, "run_cost": cost, "net": net,
                           "cumulative": cumulative})
    year = cash_flows[1:13]
    year1_cost = a.setup + sum(row["run_cost"] for row in year)
    ramp_total = sum(min(1, month / a.ramp_months) if a.ramp_months else 1 for month in range(1, 13))
    contribution = margin * a.adoption
    return {
        "steady_net_monthly": a.monthly_volume * contribution - a.fixed_monthly,
        "steady_hours_monthly": a.monthly_volume * a.adoption * minutes_saved / 60,
        "steady_break_even_volume": a.fixed_monthly / contribution if contribution > 0 else None,
        "year1_break_even_volume": (a.setup + a.fixed_monthly * 12) / (contribution * ramp_total)
        if contribution > 0 else None,
        "year1_cost": year1_cost, "year1_value": sum(row["realized_value"] for row in year),
        "year1_net": year[-1]["cumulative"],
        "year1_roi": year[-1]["cumulative"] / year1_cost if year1_cost else None,
        "year2_cumulative": cumulative, "payback_month": payback, "cash_flows": cash_flows,
    }


def sensitivity(unit, assumptions):
    return [
        {"monthly_volume": ceil(assumptions.monthly_volume * scale),
         "realization": realization,
         "year1_net": calculate(unit, replace(assumptions, realization=realization,
                                              monthly_volume=ceil(assumptions.monthly_volume * scale)))["year1_net"]}
        for scale in (.65, .85, 1, 1.2, 1.5)
        for realization in (.25, .45, .65, .85, 1)
    ]

