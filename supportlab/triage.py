"""Offline article matching, empirical confidence calibration and policy replay."""
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
import math
import re
from statistics import mean

from .catalog import CATALOG
from .operations import percentile90


POLICIES = ("Human baseline", "Rules only", "AI assist", "Full automation")
SHORTCUTS = {article.shortcut: key for key, article in CATALOG.items() if article.shortcut}
BLOCKERS = re.compile(
    r"unknown sign-in|someone else|credentials|compromis|hijack|fraud|chargeback|"
    r"refund|charged twice|erase|erasure|personal (?:data|records)|"
    r"ignore (?:all |previous )?instructions|system prompt", re.I)
STOPWORDS = set("a an and as about can could do for from get help hi how i is it me my of on or our please team that the this to we way where with you".split())
BINS = (0, .15, .35, .60, .80, .95)
TARGET_PRECISION = .82


@dataclass(frozen=True)
class Proposal:
    article: str
    confidence: float


@dataclass(frozen=True)
class Decision:
    action: str
    article: str
    reason: str


def tokens(text):
    words = [word for word in re.findall(r"[a-z]+", text.lower()) if word not in STOPWORDS]
    return words + [f"{left}_{right}" for left, right in zip(words, words[1:])]


def confidence_bin(score):
    return max(i for i, bound in enumerate(BINS) if score >= bound)


class OfflineTriage:
    """Multinomial Naive Bayes predicts an approved article ID from intake text."""

    def __init__(self, train):
        counts = defaultdict(Counter)
        priors = Counter()
        for row in train:
            priors[row["intent"]] += 1
            counts[row["intent"]].update(tokens(row["text"]))
        self.vocabulary = set().union(*(counts[key] for key in counts))
        self.log_priors = {key: math.log(count / len(train)) for key, count in priors.items()}
        self.weights = {}
        for key, counter in counts.items():
            denominator = counter.total() + len(self.vocabulary)
            self.weights[key] = {word: math.log((counter[word] + 1) / denominator)
                                 for word in self.vocabulary}
        self.calibration = {}

    @lru_cache(maxsize=4096)
    def raw(self, text):
        words = [word for word in tokens(text) if word in self.vocabulary]
        if not words:
            return Proposal("", 0)
        scores = {key: prior + sum(self.weights[key][word] for word in words)
                  for key, prior in self.log_priors.items()}
        top = max(scores, key=scores.get)
        probability = 1 / sum(math.exp(score - scores[top]) for score in scores.values())
        return Proposal(top, probability)

    def calibrate(self, rows):
        counts = defaultdict(list)
        for row in rows:
            proposal = self.raw(row["text"])
            if proposal.article:
                counts[confidence_bin(proposal.confidence)].append(proposal.article == row["intent"])
        # Beta(1,1) smoothing prevents certainty in sparse bins. Empty bins fail closed.
        self.calibration = {index: (sum(values) + 1) / (len(values) + 2)
                            for index, values in counts.items()}
        return [{"raw_lower_bound": bound, "n": len(counts[index]),
                 "empirical_accuracy": mean(counts[index]) if counts[index] else None,
                 "calibrated_score": self.calibration.get(index, 0)}
                for index, bound in enumerate(BINS)]

    def propose(self, text):
        raw = self.raw(text)
        return Proposal(raw.article, self.calibration.get(confidence_bin(raw.confidence), 0)
                        if raw.article else 0)


def decide(ticket, proposal, policy, threshold):
    if policy not in POLICIES:
        raise ValueError(f"Unknown policy: {policy}")
    if policy == "Human baseline":
        return Decision("human", "", "manual_baseline")
    if policy == "Full automation":
        if proposal.article in CATALOG:
            return Decision("auto", proposal.article, "unrestricted_comparator")
        return Decision("human", "", "no_approved_article")

    if not ticket["verified"]:
        return Decision("human", "", "unverified")
    if ticket["repeat"] or ticket["declared_multi"]:
        return Decision("human", "", "repeat_or_multiple")
    if ticket["intake_signal"] != "routine" or BLOCKERS.search(ticket["text"]):
        return Decision("human", "", "risk_signal")
    if policy == "Rules only":
        article = SHORTCUTS.get(ticket["shortcut"])
        return Decision("auto", article, "trusted_menu") if article else Decision("human", "", "no_rule")
    article = CATALOG.get(proposal.article)
    if article is None or article.risk != "Low":
        return Decision("human", "", "outside_review_scope")
    if proposal.confidence < threshold:
        return Decision("human", "", "low_confidence")
    return Decision("review", proposal.article, "agent_approval_required")


def fit(rows):
    partitions = {name: [row for row in rows if row["split"] == name]
                  for name in ("train", "calibrate", "select")}
    engine = OfflineTriage(partitions["train"])
    calibration = engine.calibrate(partitions["calibrate"])
    selection = []
    for threshold in (.50, .60, .70, .75, .80, .85, .90, .95):
        reviews = []
        for row in partitions["select"]:
            decision = decide(row, engine.propose(row["text"]), "AI assist", threshold)
            if decision.action == "review":
                reviews.append(decision.article == row["intent"] and not row["must_escalate"])
        precision = mean(reviews) if reviews else None
        selection.append({"threshold": threshold, "reviews": len(reviews), "safe_precision": precision,
                          "eligible": len(reviews) >= 30 and precision >= TARGET_PRECISION if reviews else False})
    eligible = [row for row in selection if row["eligible"]]
    threshold = max(eligible, key=lambda row: (row["reviews"], row["threshold"]))["threshold"] if eligible else 1.01
    return engine, threshold, {"calibration": calibration, "selection": selection, "threshold": threshold}


def wilson(successes, n):
    if not n:
        return None, None
    z = 1.95996398454
    p = successes / n
    scale = 1 + z * z / n
    center = (p + z * z / (2 * n)) / scale
    radius = z / scale * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    return max(0, center - radius), min(1, center + radius)


def replay(rows, engine, threshold, policy, settings):
    for row in rows:
        raw = engine.raw(row["text"])
        proposal = engine.propose(row["text"])
        decision = decide(row, proposal, policy, threshold)
        offered = decision.action != "human"
        correct = offered and decision.article == row["intent"]
        valid = correct and not row["must_escalate"]
        base = row["handle_min"]
        minutes = base
        if decision.action == "review":
            minutes = base * (1 - settings["review_speedup"]) if valid else base + settings["bad_review_minutes"]
        if decision.action == "auto":
            minutes = settings["auto_audit_minutes"] if valid else base + settings["bad_auto_minutes"]
        response = row["first_reply_min"]
        if decision.action == "auto":
            response = settings["automation_seconds"][policy] / 60
        elif decision.action == "review":
            response = max(0, response + minutes - base) + settings["automation_seconds"][policy] / 60
        yield {
            "ticket_id": row["ticket_id"], "policy": policy, "risk": row["risk"], "region": row["region"],
            "expected_article": row["intent"], "predicted_article": proposal.article,
            "raw_confidence": raw.confidence, "confidence": proposal.confidence,
            "must_escalate": row["must_escalate"], "action": decision.action, "article": decision.article,
            "response_text": CATALOG[decision.article].text if offered else "",
            "reason": decision.reason, "correct_offer": correct, "valid_offer": valid,
            "unsafe_auto": decision.action == "auto" and row["must_escalate"],
            "bad_auto": decision.action == "auto" and not valid,
            "protected_review": decision.action == "review" and row["must_escalate"],
            "baseline_minutes": base, "modeled_minutes": minutes,
            "modeled_first_reply_min": response, "modeled_sla_met": response <= row["sla_min"],
        }


DEFAULT_SETTINGS = {
    "review_speedup": .42, "bad_review_minutes": 2, "auto_audit_minutes": .6, "bad_auto_minutes": 8,
    "automation_seconds": {"Human baseline": 0, "Rules only": .3, "AI assist": 2.5, "Full automation": 2.5},
}


def metrics(replays):
    n = len(replays)
    if n == 0:
        raise ValueError("Cannot evaluate an empty cohort")
    counts = Counter(row["action"] for row in replays)
    offered = counts["auto"] + counts["review"]
    correct = sum(row["correct_offer"] for row in replays)
    valid = sum(row["valid_offer"] for row in replays)
    protected = sum(row["must_escalate"] for row in replays)
    unsafe = sum(row["unsafe_auto"] for row in replays)
    bad_auto = sum(row["bad_auto"] for row in replays)
    return {
        "tickets": n, "auto": counts["auto"], "review": counts["review"], "human": counts["human"],
        "offered": offered, "offer_accuracy": correct / offered if offered else None,
        "safe_offer_precision": valid / offered if offered else None,
        "offer_precision_interval": wilson(valid, offered), "protected": protected,
        "unsafe_auto": unsafe, "unsafe_rate_protected": unsafe / protected if protected else None,
        "unsafe_interval": wilson(unsafe, protected), "bad_auto": bad_auto,
        "protected_review": sum(row["protected_review"] for row in replays),
        "baseline_minutes": mean(row["baseline_minutes"] for row in replays),
        "modeled_minutes": mean(row["modeled_minutes"] for row in replays),
        "reply_p90_min": percentile90([row["modeled_first_reply_min"] for row in replays]),
        "sla_pct": 100 * mean(row["modeled_sla_met"] for row in replays),
    }


def evaluate(rows, engine, threshold, policy, settings=DEFAULT_SETTINGS):
    return metrics(list(replay(rows, engine, threshold, policy, settings)))


def reliability(rows, engine):
    predictions = [(engine.raw(row["text"]), engine.propose(row["text"]), row["intent"])
                   for row in rows]
    report = []
    for index, bound in enumerate(BINS):
        bucket = [(raw, calibrated, label) for raw, calibrated, label in predictions
                  if raw.article and confidence_bin(raw.confidence) == index]
        if bucket:
            report.append({"raw_lower_bound": bound, "n": len(bucket),
                           "mean_raw": mean(raw.confidence for raw, _, _ in bucket),
                           "mean_calibrated": mean(calibrated.confidence for _, calibrated, _ in bucket),
                           "accuracy": mean(raw.article == label for raw, _, label in bucket)})
    scored = [(raw, calibrated, label) for raw, calibrated, label in predictions if raw.article]
    return {
        "scored": len(scored), "unscored": len(predictions) - len(scored),
        "intent_accuracy": mean(raw.article == label for raw, _, label in scored),
        "raw_brier": mean((raw.confidence - (raw.article == label)) ** 2 for raw, _, label in scored),
        "calibrated_brier": mean((calibrated.confidence - (raw.article == label)) ** 2
                                 for raw, calibrated, label in scored),
        "bins": report,
    }

