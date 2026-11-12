# Financial model

All figures are illustrative USD assumptions for RelayDesk. The code runs with free local software. The model estimates what a staffed production workflow could cost.

## Inputs

| Input | Base | Interpretation |
|---|---:|---|
| Intake | 4,000 tickets/month | Three-month synthetic average. Same case mix assumed across future months. |
| Loaded labor | $36/hour | Salary, benefits and staffing overhead combined |
| Adoption | 85% | Share of all tickets flowing through the selected workflow at steady state. Outcome mix comes from replay, including fallback. |
| Capacity realization | 65% | Fraction of saved labor value converted into overtime avoided, contractor spend avoided, or forecast hiring absorbed |
| Adoption ramp | 4 months | 25%, 50%, 75%, then 100% of target adoption. Fixed costs start in month one. |
| Valid AI draft | 42% reduction in handling | Includes agent review and send. Measure against a concurrent manual cohort. |
| Invalid draft | Manual time plus 2 min | Reviewer reads and rejects or routes it |
| Valid auto-send | 0.6 min | Expected audit time across all valid auto-sends |
| Invalid auto-send | Manual time plus 8 min | Typical follow-up and correction work; severe incident losses excluded |

| Cost component | Rules only | AI assist | Full automation |
|---|---:|---:|---:|
| One-time workflow build, QA and training | $2,200 | $4,200 | $7,600 |
| Monthly platform overhead, maintenance and monitoring | $120 | $230 | $560 |
| Processing cost per adopted ticket | $0.005 | $0.035 | $0.055 |

The processing charge applies across the whole adopted queue, including fallback decisions. Review, audit, and rework are already in the labor delta. The overhead line covers recurring platform and operational overhead rather than ticket-level review. No vendor pricing, tax, revenue uplift, discounting, staff reduction, or severe incident liability is assumed. Negative labor deltas are charged in full.

## Calculation

1. Mean minutes saved = mean baseline minutes − mean replay minutes.
2. Adopted tickets in month m = intake × steady adoption × ramp fraction.
3. Recoverable hours = adopted tickets × minutes saved / 60.
4. Realized labor value = recoverable hours × loaded rate × realization for positive savings. Charge extra labor at the full loaded rate.
5. Monthly net = realized labor value − monthly overhead − adopted tickets × processing charge.
6. Year-one net = sum of months 1–12 net − setup. ROI = year-one net / (setup + year-one overhead and processing).
7. Payback is the first non-negative cumulative month that stays non-negative through the 24-month horizon. At zero implementation cost and no subsequent deficit the month is zero.
8. Steady monthly break-even = monthly fixed cost / (adoption × contribution per adopted ticket). Year-one break-even monthly volume uses (setup + 12 × fixed cost) / (adoption × contribution × sum of first-year ramp fractions). A nonpositive denominator has no finite positive-volume break-even.

## Base comparison

| Result | Rules only | AI assist | Full automation |
|---|---:|---:|---:|
| Steady monthly capacity hours | 49.9 | 81.1 | −22.5 |
| Steady monthly net | $1,031 | $1,548 | −$1,559 |
| Year-one net | $8,446 | $11,709 | −$24,805 |
| Year-one ROI | 221.2% | 142.6% | −152.3% |
| Payback | Month 4 | Month 5 | Beyond 24 months |
| Steady break-even intake, tickets/mo | 418 | 518 | No finite volume |
| Year-one break-even intake, tickets/mo | 1,205 | 1,492 | No finite volume |

Break-even counts are rounded up. Full automation can have ROI below −100% because rework makes labor value negative on top of implementation and operating spend. Safety remains a separate release gate.

## Sensitivity for AI assist

| Tickets/month | 25% realization | 65% realization | 100% realization |
|---:|---:|---:|---:|
| 2,600 | −$2,793 | $5,175 | $12,146 |
| 4,000 | −$548 | $11,709 | $22,435 |
| 6,000 | $2,657 | $21,044 | $37,132 |

At 4,000 tickets per month, first-year break-even needs approximately 27% realization with base adoption and replay efficiency. Lower adoption and realization together reduce the upside. To validate the largest drivers, have QA time agent review and correction, and have Finance identify a specific staffing or overtime cost that freed capacity could absorb. The dashboard supports changes to volume, labor rate, adoption, and realization. The evidence export includes the full grid, cash flows in JSON, and source assumptions.

