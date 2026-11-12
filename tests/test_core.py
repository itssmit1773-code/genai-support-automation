import unittest
from dataclasses import replace

from supportlab.data import generate, challenge_cases
from supportlab.finance import Assumptions, Unit, calculate
from supportlab.operations import summarize
from supportlab.triage import Proposal, fit, decide, evaluate


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = generate()

    def test_replay_and_partition_isolation(self):
        self.assertEqual(self.rows, generate())
        self.assertEqual(len({row["ticket_id"] for row in self.rows}), 12000)
        splits_by_family = {}
        for row in self.rows:
            splits_by_family.setdefault(row["family"], set()).add(row["split"])
        self.assertTrue(all(len(splits) == 1 for splits in splits_by_family.values()))

    def test_sql_reconciles_and_counts_sla_boundary(self):
        rows = self.rows[:2]
        rows = [dict(row, first_reply_min=reply, sla_min=60)
                for row, reply in zip(rows, [60, 61])]
        grouped = summarize(rows, "category", hourly_rate=60)
        self.assertEqual(sum(row["tickets"] for row in grouped), 2)
        self.assertEqual(sum(row["sla_met"] for row in grouped), 1)
        self.assertAlmostEqual(sum(row["labor_usd"] for row in grouped),
                               sum(row["handle_min"] for row in rows), places=2)

    def test_every_dimension_reconciles(self):
        for dimension in ("category", "week", "complexity", "risk", "region", "plan"):
            groups = summarize(self.rows, dimension, 36)
            self.assertEqual(sum(row["tickets"] for row in groups), len(self.rows))


class PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = generate()
        cls.engine, cls.threshold, _ = fit(cls.rows)

    def test_sensitive_metadata_overrides_high_confidence(self):
        ticket = dict(challenge_cases()[0], verified=False)
        self.assertEqual(decide(ticket, Proposal("export", 1), "AI assist", .5).action,
                         "human")

    def test_low_confidence_and_unknown_answer_abstain(self):
        ticket = dict(challenge_cases()[0], verified=True)
        self.assertEqual(decide(ticket, Proposal("export", .49), "AI assist", .5).action,
                         "human")
        self.assertEqual(decide(ticket, Proposal("invented", 1), "Full automation", .5).action,
                         "human")

    def test_full_auto_exposes_protected_cases(self):
        cases = challenge_cases()
        for policy, expected in [("AI assist", 0), ("Rules only", 0), ("Full automation", 1)]:
            result = evaluate(cases, self.engine, self.threshold, policy)
            if expected:
                self.assertGreater(result["unsafe_auto"], 0)
            else:
                self.assertEqual(result["unsafe_auto"], 0)

    def test_misdirected_shortcut_exposes_invalid_automatic_reply(self):
        case = next(row for row in challenge_cases() if row["case"] == "Misdirected shortcut")
        rules = evaluate([case], self.engine, self.threshold, "Rules only")
        assist = evaluate([case], self.engine, self.threshold, "AI assist")
        self.assertEqual(rules["bad_auto"], 1)
        self.assertEqual(rules["unsafe_auto"], 0)
        self.assertEqual(assist["safe_offer_precision"], 1)

    def test_policy_does_not_read_reference_labels(self):
        ticket = dict(challenge_cases()[-2])
        proposal = Proposal("export", 1)
        initial = decide(ticket, proposal, "AI assist", .5)
        changed = dict(ticket, intent="takeover", must_escalate=True, risk="High")
        self.assertEqual(decide(changed, proposal, "AI assist", .5), initial)

    def test_metrics_count_all_test_rows(self):
        test = [row for row in self.rows if row["split"] == "test"]
        result = evaluate(test, self.engine, self.threshold, "AI assist")
        self.assertEqual(result["tickets"], len(test))
        self.assertEqual(result["review"] + result["human"] + result["auto"], len(test))
        self.assertGreater(result["review"], 0)


class FinanceTests(unittest.TestCase):
    def test_hand_calculation_and_payback(self):
        assumptions = Assumptions(monthly_volume=100, hourly_rate=60, realization=.5,
                                  adoption=1, setup=120, fixed_monthly=10, ramp_months=0)
        result = calculate(Unit(10, 6, .2), assumptions)
        self.assertEqual(result["steady_net_monthly"], 170)
        self.assertEqual(result["year1_net"], 1920)
        self.assertEqual(result["payback_month"], 1)
        self.assertAlmostEqual(result["year1_break_even_volume"], 100 / 9)

    def test_non_positive_unit_margin_has_no_break_even(self):
        assumptions = Assumptions(realization=0)
        result = calculate(Unit(10, 6, .2), assumptions)
        self.assertIsNone(result["payback_month"])
        self.assertIsNone(result["year1_break_even_volume"])

    def test_ramp_reduces_first_year_value(self):
        base = Assumptions(adoption=1, realization=1)
        unit = Unit(10, 5, .02)
        self.assertLess(calculate(unit, base)["year1_net"],
                        calculate(unit, replace(base, ramp_months=0))["year1_net"])

