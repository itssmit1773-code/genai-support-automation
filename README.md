# GenAI Support Automation: Feasibility, Risk & ROI

[Open interactive dashboard](https://a8xrb8vcshwhvz3ekjqkmt.streamlit.app/) · [Read the portfolio case study](https://itssmit1773-code.github.io/portfolio/support-automation.html)

**Decision:** Start with a Reporting-only pilot of agent-reviewed drafts for report exports and paused schedules. Evaluate receipt and pending-invite drafts in a later scope review. Keep customer-facing auto-send off while measuring draft usefulness, reviewer catches, and recoverable support time.

RelayDesk is a fictional B2B SaaS reporting platform. This case study uses 12,000 transparently synthetic tickets to decide where automation earns its place in a support workflow. The local prototype selects an approved knowledge-base article, applies escalation rules, and compares four ways to handle the same cases.

| March holdout, 4,000 tickets | Manual | Rules only | AI assist | Full automation |
|---|---:|---:|---:|---:|
| Auto-sends | 0 | 494 | 0 | 3,850 |
| Drafts queued for agent review | 0 | 0 | 2,100 | 0 |
| Correct and eligible among offers | — | 95.3% | 85.6% | 48.1% |
| Mandatory escalations bypassed by auto-send | 0 | 23 | 0 | 1,764 |
| Modeled year-one incremental net value | $0 | $8,446 | $11,709 | −$24,805 |

Of the 2,100 drafts under AI assist, 73 were for cases that required escalation. Agent review is the control that prevents those drafts from going out automatically. The $11,709 estimate covers the broader replay scope and assumes 4,000 tickets per month, 85% adoption, and 65% conversion of freed capacity into economic value. All data and financial inputs are synthetic. The model is a local article-matching baseline for a possible GenAI workflow, and its measured accuracy applies to article selection in this dataset.

## Run the project

Use Python 3.12. From the extracted repository folder:

```bash
python -m venv .venv
```

Activate the environment in PowerShell with `.\.venv\Scripts\Activate.ps1` or on macOS/Linux with `source .venv/bin/activate`. If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of `python` below.

```bash
python -m pip install -r requirements.txt
python -m supportlab.study
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. The repository includes the evidence files, so the dashboard can also open directly after installation. The study generator and core tests use only Python's standard library and SQLite. Package installation requires internet access. After installation, the dashboard and analysis run locally without API keys, accounts, external model calls, or paid subscriptions.

## Review the work

- [Case study](docs/case-study.md) explains the decision and the counterfactual.
- [Business requirements and process maps](docs/requirements.md) cover stakeholders, acceptance criteria, and human escalation.
- [Evaluation protocol](docs/evaluation.md) documents split design, calibration, metrics, and challenge cases.
- [Risk register](docs/risk-register.md) records controls, owners, and residual risks.
- [Financial model](docs/financial-model.md) defines inputs, formulas, and sensitivity results.
- [Decision memo and rollout](docs/decision-memo.md) gives the sign-off gates, owners, and stop conditions.
- [Data dictionary and provenance](docs/data-dictionary.md) explains every source field and evidence file.
- [Architecture](docs/architecture.md) describes the code and how a future model could fit into the workflow.
- [Interview Q&A](docs/interview-qa.md) covers the questions a reviewer is most likely to ask.
- [Website copy and integration](docs/website.md) includes a project card, case-study introduction, and links to reuse.

This project assesses a service operations investment. It complements the portfolio’s growth and retention analysis and voice-of-customer prioritization projects by focusing on case routing, controls, and the economics of adoption.

