# Data dictionary and provenance

RelayDesk, its product instructions, and every ticket are fictional. No public dataset, customer record, personal identifier, external model, or vendor estimate was imported. The input is authored Python in [the knowledge base](../supportlab/catalog.py) and [the generator](../supportlab/data.py). Random seed 731 is committed in [the scenario assumptions](../config/assumptions.json). Rebuild with `python -m supportlab.study`.

One row represents one portal ticket. The generator samples an intent from fixed weights, picks a wording family for its time partition, then adds intake signals, context, and historical outcomes. High-risk and mixed cases are assigned greater complexity. Enterprise and protected cases receive shorter SLA targets. Protected categories get faster first replies and can still miss stricter targets. Some protected signals are hidden at intake. Regional differences are authored scenario parameters and carry no claim about real teams or customers.

| Column | Type / unit | Meaning |
|---|---|---|
| ticket_id | string | Unique synthetic ticket reference |
| opened_on | ISO date | Simulated intake calendar date |
| week | ISO date | Monday starting the intake week |
| split | enum | train, calibrate, select, or test |
| family | string | Intent plus wording-family index. Disjoint across partitions. |
| region | enum | AMER, EMEA, APAC |
| plan | enum | Standard or Enterprise |
| text | string | Synthetic intake text. May include an additional issue. |
| verified | boolean | Trusted identity and role signal available at intake |
| repeat | boolean | Prior attempt or repeat issue is visible at intake |
| declared_multi | boolean | Intake flags multiple issues. Some mixed cases remain unflagged. |
| intake_signal | enum | routine, technical, payment_dispute, security, or privacy. Signals can be missing or noisy. |
| shortcut | string or empty | Trusted portal event for a macro menu selection. It can conflict with the written request. |
| intent | enum | Gold reference article ID, assigned before text is rendered |
| category | enum | Reporting, Billing, Workspace access, Integrations, or Data governance |
| risk | enum | Low, Medium, or High intrinsic intent risk. Distinct from contextual escalation. |
| complexity | enum | Simple, Moderate, or Complex, derived from intent and context |
| must_escalate | boolean | Gold label. True for nonroutine intents, missing verification, repeat cases, or any actual mixed intent. |
| handle_min | decimal minutes | Active agent work, modeled from intent, repeat, and mixed complexity |
| first_reply_min | decimal minutes | Elapsed time from creation to first substantive reply |
| sla_min | integer minutes | First-reply target. 60 high-risk, 120 Enterprise other, 480 Standard other. |
| resolution_min | decimal minutes | Elapsed time to initial closure |
| reopened_7d | boolean | Synthetic reopen flag in the seven-day outcome window |
| resolved_7d | boolean | Initial closure within 10,080 minutes and no reopen in the seven-day window |

The model uses only `text`. The policy sees the score, article ID, text, verification, repeat, declared-multiple signal, intake signal, and trusted shortcut. Historical outcomes, category, gold intent, risk, and mandatory-escalation labels are reserved for analysis and evaluation.

## Committed evidence

| File | Grain | Use |
|---|---|---|
| tickets.csv | 12,000 tickets | Source data for baseline analysis |
| operations_by_*.csv | Dimension member | SQLite aggregates for category, week, complexity, risk, region and plan |
| test_decisions.csv | Ticket × policy | 16,000 rows including predicted article, raw and calibrated confidence, final action, reason, fixed response, outcome flags and modeled effort |
| evaluation_slices.csv | Dimension member × policy | Quality and safety by risk, region and expected article |
| challenge_labels.csv | Challenge | Eleven authored stress inputs, expected article, escalation, and scenario fields. Blank gold article marks out-of-scope and empty input. |
| challenge_decisions.csv | Challenge × policy | Four policy outcomes per stress case |
| financial_sensitivity.csv | Policy × volume × realization | Year-one incremental net under 25 volume/realization combinations per policy |
| summary.json | Study | Manual baseline, threshold selection, calibration, policy totals, economics, and 24-month cash-flow equivalents |

All CSVs are UTF-8. A blank field represents an absent value or undefined ratio, such as offer accuracy when a policy makes no offers.

