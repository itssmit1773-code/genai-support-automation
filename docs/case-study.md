# Where should RelayDesk automate support?

## The decision

RelayDesk, a fictional B2B platform for scheduling and sharing reports, supports customers across AMER, EMEA, and APAC. Its support lead wants agents to spend less time explaining repeatable product steps while preserving specialist capacity for account compromise, refunds, integrations, and personal-data requests. Finance wants to know how much of the time saved can actually be put to use.

The proposed decision is to run a Reporting-only pilot of agent-reviewed drafts for exporting a saved report and pausing a report schedule. Receipt and pending-invite drafts are candidates for a later expansion. The business question is where a draft makes support easier without transferring decision authority from the agent.

## What the workload showed

The synthetic January–March history contains 12,000 tickets. At an assumed loaded rate of $36/hour, active handling costs $109,131 across the three months. First-reply SLA attainment is 84.1%, and 91.3% of cases close within seven days and stay closed through day seven.

Reporting accounts for 4,484 tickets, or 37.4% of intake. Its mean handling time of 8.7 minutes makes it a plausible source of repeatable savings. Data governance averages 37.6 minutes per ticket and has the weakest category-level first-reply SLA attainment at 78.8%. That points to a need for better specialist handoffs. A faster canned reply would leave verification and retention review outstanding.

Billing and workspace access are mixed queues. A receipt request can use a macro. A payment dispute from the same queue needs a billing specialist. Eligibility therefore belongs at the intent and case level.

## What each operating model changes

| Option | What the customer receives | March evidence | Decision |
|---|---|---|---|
| Manual | An agent writes and sends every reply | 15.30 agent minutes per ticket; P90 first reply 357 min | Retain as control and fallback |
| Rules only | A macro auto-sends on a verified routine menu path | 494 sends; 23 mandatory escalations bypassed; 95.3% of sends correct and eligible | Keep rules for gating and routing; redesign the auto-send rule before any live test |
| AI assist | An agent checks the proposed article and sends or escalates | 2,100 draft offers; 1,798 correct and eligible; 73 protected cases reached review | Shadow, then controlled pilot with agent approval |
| Full automation | A matched article auto-sends whenever the classifier can score the ticket | 3,850 sends; 1,764 protected cases bypassed; 1,997 invalid sends overall | Reject under the tested design |

A rule-following shortcut can still point to the wrong article. The challenge suite includes a report scheduling request filed through a billing receipt shortcut. The rules policy sends receipt instructions. AI assist proposes the scheduling article for review. The March replay also shows that known text checks and metadata miss some protected cases. Those exceptions are why approval stays in the workflow.

The full-automation comparator raises modeled first-reply SLA attainment to 99.5%, while only 48.1% of its offers are correct and eligible. The metric rewards a fast timestamp, even when the reply triggers rework. Review first-reply SLA alongside protected-case routing and seven-day outcomes.

## What makes the investment viable

In the broader replay scenario, at 4,000 tickets per month, 85% adoption and 65% realization, AI assist yields 81 hours per month of modeled capacity at steady state. The year-one economic net is $11,709 with payback in month five. At the same volume and 25% realization, year one falls to −$548. A Reporting-only estimate needs its own volume, mix and staffing inputs. The broader financial case depends on confirming that reduced handling time survives agent review and can absorb planned workload or reduce avoidable spend.

Rules only pays back sooner in the replay and has higher percentage ROI because it costs less. It still bypasses mandatory escalation. The decision treats that control as a condition for release. Financial ranking follows the safety gate.

## What would change the decision

The March split contains new phrase families, but all examples come from an English-only synthetic generator. The prototype retrieves approved text and evaluates article fit. It cannot establish free-form answer quality, real agent catch rates, multilingual performance, customer acceptance, or actual savings. Run a labeled shadow study and a controlled agent pilot before funding any expansion. Record scope violations and specialist routing alongside minutes saved.

