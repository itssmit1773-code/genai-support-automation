# Automation risk register

The ratings are qualitative for this fictional operation. Impact describes the business consequence. The residual risk column gives the pilot decision and evidence needed.

| Risk and impact | Signal or failure observed | Control and accountable owner | Residual risk and release decision |
|---|---|---|---|
| Protected case receives a routine reply. Security, billing or privacy work may be delayed. | Intake signals miss context. AI assist surfaced 73 protected drafts on March. | Frontline lead enforces original-thread review. Specialist owners define routing and acknowledgement. Support Ops tracks missed escalations and reviewer catches. | High until shadow and pilot demonstrate reliable routing. Keep auto-send disabled. |
| Wrong approved article reaches a customer. The customer repeats the request or follows the wrong instructions. | The mismatched-menu fixture led the rules workflow to send receipt instructions for report scheduling. | Knowledge owner versions approved articles. Agent confirms intent, plan and fit, and records overrides. | Medium with agent review. Audit edits and seven-day reopens by article. |
| Draft service sees sensitive ticket content or follows hostile instructions. | The known prompt-injection case is blocked by a text rule. The local model only returns article IDs. | Security restricts access and separates input text from trusted metadata. Privacy approves minimization, retention and deletion. Any generative replacement must pass injection and leakage tests before shadow use. | High for a future generative service until tested on the intended runtime. |
| Fallback drops a case, duplicates a reply, or resets the SLA clock. | The prototype models fallback as a decision. It does not connect to a live queue. | Support engineering preserves ticket reference and deadline, enforces idempotent send, and tests retry, outage and kill switch behavior. | High until end-to-end failure drills pass in staging. |
| Savings disappear after review or staffing constraints. | The modeled year-one net turns negative at 25% realization and base volume. | Finance links recovered time to avoidable spend or forecast workload. QA measures active time including rejects. | Medium. Fund expansion only after evidence of realizable capacity. |
| English benchmark obscures poor performance in other languages or queues. | Training and holdout share an English synthetic generator. | Support PM keeps pilot language and intents narrow. QA labels new cohorts before reuse. | High outside tested scope. Require independent calibration and scope approval. |

Track protected drafts, missed human escalations, invalid sends, handoff acknowledgement, response SLA, seven-day reopens, and agent time. Report counts and rates together. A confirmed disclosure, unapproved send, or missed human escalation triggers the recovery procedure in the [decision memo](decision-memo.md).

