# Portfolio website integration

## Project card

**Title**  
GenAI Support Automation: Feasibility, Risk & ROI

**Description**  
I evaluated four ways to handle SaaS support tickets and designed an agent-reviewed pilot for routine requests. The case study combines SQL operations analysis, an offline triage benchmark, human escalation rules, and a 24-month financial model.

**Tags**  
Business analysis · Support operations · AI evaluation · SQL · Python · Streamlit

**Evidence caption**  
12,000 synthetic tickets. All financial estimates are illustrative.

**Links**  
Use the uploaded repository URL for “View source.” Point “Read case study” to the rendered case-study Markdown. Add “Explore dashboard” if you deploy the Streamlit app. The ZIP includes the complete dashboard and its inputs.

## Dashboard images

The ZIP includes the [Operations preview](../assets/operations-preview.png) and the [Financial scenarios preview](../assets/finance-preview.png). Suggested alt text for the financial image is “Comparison of four support policies with first-year ROI, cumulative value, and a sensitivity grid for ticket volume and value realization.”

## Detail-page introduction

RelayDesk had a practical question. Which support requests could AI speed up while keeping sensitive decisions with agents? I analyzed a synthetic queue of 12,000 tickets, then replayed manual support, rules-only auto-send, AI assist, and full automation on the same 4,000 labeled holdout cases. The recommended first step is a controlled pilot for agent-reviewed Reporting drafts. The full-scope financial scenario estimates $11,709 in year-one incremental value at 65% capacity realization. Both the rollout gates and the downside assumptions are part of the case study.

## Page structure

1. Lead with the decision and the synthetic-data note.
2. Show the four-policy comparison from the README or embed the Risk view.
3. Summarize the current workflow, review step, and escalation owners.
4. Show the financial sensitivity grid with the base and downside assumptions visible.
5. Link the case study, repository, and dashboard. Use the decision memo for rollout details.

For an optional Streamlit deployment, use `app.py` as the entry point, Python 3.12, and the repository’s `requirements.txt`. Keep the committed `evidence/` directory with the app. The dashboard needs no secrets or API keys.

