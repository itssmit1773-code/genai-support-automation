# Interview Q&A

**What decision did you own in this case study?**  
I evaluated whether a fictional SaaS support team should automate first replies. The evidence supported testing agent-reviewed drafts for repeatable product instructions. The pilot starts with two Reporting tasks and preserves specialist routing for sensitive work.

**How does this differ from your other portfolio projects?**  
Growth and retention asks where users drop off. Voice of customer asks what product problems to prioritize. This case asks how to redesign a service workflow, control automation risk, and decide if it is worth funding.

**Why is the dataset synthetic?**  
I needed ticket wording, trusted intake signals, escalation labels, labor time and resolution outcomes at the same grain. The generator provides those fields and makes the assumptions inspectable. The portfolio evidence demonstrates the method. Before a launch decision I would use a privacy-approved, labeled sample of real tickets.

**What would you ask the support lead first?**  
I would ask which routine issues agents resolve in one touch and which signals show that a routine-looking case needs an expert. That helps set an eligibility rule and identify examples where a shortcut fails.

**How does the offline AI work?**  
It learns word and phrase patterns that predict one approved article. I used separate samples for training, calibrating confidence, choosing the threshold, and final testing. It retrieves fixed text, so the score tests article fit. I would separately evaluate factual grounding and policy compliance for a free-form model.

**What is a calibrated score?**  
It estimates how often suggestions with similar raw scores pick the correct article. It does not determine whether the case is safe. A correctly matched receipt article is still inappropriate if the customer is disputing a payment or cannot verify their identity.

**Why did you choose agent review over rules-only?**  
The tested rules-only workflow sent macros automatically and bypassed 23 mandatory escalations in the holdout. Rules still help verify inputs and route cases. AI assist surfaced 73 protected cases for review, so I would enforce agent approval and track reviewer catches.

**Did the model really meet 99.5% SLA?**  
That is a replay estimate for the full-automation option. It counts quick replies even if they were wrong or unsafe. I would judge a pilot on the combined picture of response times, reopen rates, proper escalations, and agent effort.

**How did you calculate the $11,709?**  
I applied the replay’s average time savings to monthly volume and adoption, valued the hours at a loaded rate, then applied a 65% realization assumption. I deducted one-time and recurring costs. At 25% realization with the same intake, the first year goes slightly negative.

**What would make you stop the pilot?**  
An unapproved send, a confirmed sensitive disclosure, or a protected case missed by the human workflow triggers a return to manual handling. For routine quality and latency, I would also watch predefined pilot guardrails with a concurrent control.

**Which measurement would most affect the investment case?**  
Actual minutes saved including draft rejection, and whether the recovered hours reduce avoidable cost or absorb forecast demand. I would measure handling in the pilot and agree with Finance in advance on how capacity translates into value.

**What would you improve before adding a language or region?**  
Build a locally labeled set with the language, phrasing and specialist handoffs used there. Validate both knowledge coverage and escalation performance. Recalibrate confidence for the new cohort and verify that agents can see and route the original context.

