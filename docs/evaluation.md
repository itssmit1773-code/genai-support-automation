# Evaluation protocol

## Question and unit of analysis

A ticket enters once and each policy sees the same intake fields. The primary comparison is between the actions each policy would take and the synthetic reference labels. The article catalog and labels are authored for this project. The article text is fixed and versioned with the repository. An exact article match checks whether the chosen guidance fits the intended task. It does not score free-form claims, tone, personalization, policy hallucinations, or customer outcomes.

| Partition | Rows | Purpose |
|---|---:|---|
| January train | 4,600 | Learn token and bigram likelihoods and intent priors |
| February 1–14 calibration | 1,800 | Estimate the probability of a correct top article in each raw score bin |
| February 15–28 selection | 1,600 | Choose the review threshold once |
| March test | 4,000 | Final comparison with the threshold frozen |
| Hand-authored challenge cases | 11 | Examine specific failures outside the main benchmark |

Within each intent, wording families are disjoint across the four splits. Individual phrases repeat inside a split, sometimes with another intent appended. Test adds more mixed-intent tickets than development. All cohorts share the same synthetic generator, so the effective variety is much smaller than the row count. The challenge cases document behavior on their specific inputs and do not estimate production incidence.

## Scoring and selection

Multinomial Naive Bayes predicts the top article from English unigrams and adjacent bigrams. The raw top posterior is mapped to the observed probability of article correctness in its calibration bucket, using (correct + 1) / (count + 2). Unseen buckets receive zero. The score is global across intents. Intake safety rules run independently of it.

On the selection split, candidate thresholds from 0.50 to 0.95 are tested with the same rules and article scope. Eligible thresholds require 30 draft offers and at least 82% correct-and-eligible offers. Select the one with most offers, breaking ties toward the higher threshold. A no-pass result disables review. The selected threshold is 0.50, yielding 883 offers on selection. On March, the raw classifier scored 3,850 cases with 74.8% intent accuracy. Top-label Brier loss on scored cases fell from 0.129 to 0.115. Lower Brier loss means the estimated probabilities better match correctness on this synthetic holdout.

## Policy comparison

| Policy | Eligible action | Fallback |
|---|---|---|
| Human baseline | Agent handles every ticket | Existing specialist workflow |
| Rules only | Auto-send approved macro for trusted portal shortcut after protective checks | Human |
| AI assist | Queue an approved routine article for agent review after protective checks and threshold | Human |
| Full automation | Auto-send any matched approved article, including specialist templates, without threshold or protective checks | Human when no article scores |

Protected means a ticket needs an agent to triage or escalate. A low-risk intent can be protected when verification fails, the issue recurs, or a second issue is present. In this study, the label sees the full synthetic context. The policy sees incomplete intake signals and the message.

| Metric | Definition |
|---|---|
| Offer coverage | (Auto-send + review) / all tickets |
| Offer article accuracy | Correct article / offered tickets |
| Correct-and-eligible precision | Correct article and no mandatory escalation / offered tickets |
| Protected auto-send rate | Auto-sent protected tickets / all protected tickets |
| Invalid auto-send | Auto-send with a wrong article or mandatory escalation, counting each ticket once |
| Protected draft | Review offer on a protected ticket. This is a near miss requiring agent intervention. |
| P90 first reply | 90th percentile of modeled first-reply minutes |
| First-reply SLA attainment | Modeled first reply at or under the ticket’s SLA |
| Agent effort | Mean modeled minutes per ticket, including audit or rework where applicable |

The human baseline has no article offer score. A review offer is an intermediate action. The modeled labor assumes a reviewer catches every invalid draft and absorbs two minutes of extra review before manual handling. This is an assumption to test. Auto-reply latency uses 0.3 seconds for rules and 2.5 seconds for model workflows. Human queues keep historical latency. AI assist adds 2.5 seconds and adjusts elapsed time by the change in active handling, floored at zero before inference. This simple counterfactual ignores queue dynamics and dependency outages. Response SLA includes bad auto-sends. The project does not project future resolution or reopen performance.

Row-level test decisions, quality slices by risk, region, and intent, and illustrative Wilson intervals are in the evidence exports. Those intervals assume independent tickets, which repeated phrases violate. A production evaluation should cluster by conversation or wording family, check errors by language and plan, and include specialist agreement and reviewer catch rates.

## Challenge suite

The fixture set covers unknown identity, prior failed attempt, mixed intent, explicit security and privacy signals, prompt injection, mismatched menu selection, out-of-scope text, empty input, a routine control, and declared multi-intent. The prompt-injection case tests detection of a known phrase. The model returns a catalog ID and has no instruction-following or tool capability. A generative replacement would need separate tests for injection variants, data leakage, unsupported instructions and tool abuse.

