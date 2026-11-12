# Decision memo for Support Operations and Finance

**Decision requested**  
Authorize preparation for a shadow study and a controlled agent-review pilot in Reporting. Reserve Billing receipt and Workspace pending-invite expansion for a separate decision after the pilot. Maintain specialist handling for protected workflows and keep auto-send disabled.

**Basis for the decision**  
Reporting has the highest synthetic volume and offers two narrow tasks backed by approved articles. AI assist queued 2,100 drafts on the broader March holdout and 85.6% of offers were correct and eligible. Seventy-three offers still required escalation. The release decision depends on an agent seeing the complete thread and being able to reject the draft, with an enforced approval step at send. The broader-scope financial scenario estimates $11,709 in year-one net value. Treat this as a scale hypothesis. A reporting-only pilot has a different volume, mix, staffing profile, and economics.

**Alternatives**  
Continue manual handling as the control and fallback. Use deterministic intake checks and specialist routing throughout. Rules-only auto-send bypassed escalation on 23 protected holdout tickets and sent an incorrect receipt response in the mismatched-menu challenge. Full automation bypassed 1,764 escalations and increased modeled handling effort once rework was counted.

## Phased rollout

| Priority and phase | Owner | Work | Exit criteria |
|---|---|---|---|
| P0 · Baseline and controls | Support Ops + Privacy + Security | Approve taxonomy and English reporting scope. Set access, redaction, retention, restricted routing and on-call ownership. Test send authorization, handoff acknowledgement, duplicate prevention, timeouts, KB withdrawal, and kill switch. | Named owners sign off. Simulated failures preserve the SLA clock and lead to a single manual case. No unapproved sends. |
| P1 · Shadow | QA lead + Knowledge owner | Score at least 500 consecutive English reporting requests and a separately sampled set of at least 200 protected or ambiguous cases. Two reviewers independently label intent, eligibility and article fit. Resolve disagreements with a specialist. | At least 90% correct-and-eligible precision on offers and no failures in the critical escalation, privacy and authorization fixtures. Publish confidence intervals, denominators, reviewer disagreement and errors by case type. |
| P2 · Controlled pilot | Support PM + Frontline lead | Randomly assign eligible reporting tickets to agent assist or usual care, stratified by shift and queue. Analyze by assigned group. Log accepts, edits, overrides and handling minutes. Sample each route daily. Size the study using shadow variance and clustered agent effects. | Mean handling time falls by at least 1 minute per assigned eligible ticket with a positive lower 95% bound on the improvement. Review seven-day reopen and first-reply SLA against agreed 1- and 2-percentage-point degradation margins. Confirm protected drafts were caught and all sends had approval. |
| P3 · Scope review | Support Ops + Finance | Re-estimate savings with observed effort, staffing absorption, and workload mix. Reassess receipt and invite eligibility with their specialist owners. | Finance validates realizable capacity and positive downside economics at the proposed scope. Operations and risk owners approve each new intent. |

The numeric gates are proposed decision criteria for this fictional business. The pilot requires adequate sample sizes to assess both effort and non-inferiority on service outcomes. An inconclusive outcome extends the controlled study or ends the pilot.

## Stop conditions and recovery

Disable drafting immediately after any unapproved send, confirmed sensitive disclosure, or protected case missed by the human workflow. Pause enrollment if the agreed service guardrails deteriorate during daily review or agents lose the ability to see the original thread. The duty lead switches to manual handling, preserves the queue and original SLA deadlines, investigates affected cases, and requires risk and Support Ops approval to resume. Keep staged automation permissions independent of the UI so closing a panel cannot bypass enforcement.

