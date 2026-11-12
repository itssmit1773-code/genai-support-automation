"""Explore RelayDesk's synthetic operations, policy evidence and financial scenarios."""
from dataclasses import replace
from math import ceil
import json
from pathlib import Path
from statistics import mean

import altair as alt
import pandas as pd
import streamlit as st

from supportlab.finance import calculate, sensitivity
from supportlab.operations import DIMENSIONS, percentile90, summarize
from supportlab.study import load_config, policy_economics
from supportlab.triage import POLICIES, metrics


EVIDENCE = Path(__file__).resolve().parent / "evidence"
COLORS = ["#61758a", "#ba7543", "#08776e", "#8d536a"]
POLICY_COLOR = alt.Color("Policy:N", scale=alt.Scale(domain=list(POLICIES), range=COLORS))


@st.cache_data
def read_evidence(revision):
    report = json.loads((EVIDENCE / "summary.json").read_text(encoding="utf-8"))
    return (report, pd.read_csv(EVIDENCE / "tickets.csv"),
            pd.read_csv(EVIDENCE / "test_decisions.csv", keep_default_na=False),
            pd.read_csv(EVIDENCE / "challenge_decisions.csv", keep_default_na=False))


def percent(value):
    return f"{value:.1%}" if value is not None else "—"


def money(value):
    return f"${value:,.0f}" if value >= 0 else f"−${abs(value):,.0f}"


def show_chart(chart):
    # A layer with inline values keeps these small aggregate datasets self-contained.
    with alt.data_transformers.enable("default", consolidate_datasets=False):
        spec = chart.to_dict()
    layer = {key: spec.pop(key) for key in ("data", "mark", "encoding")}
    spec["layer"] = [layer]
    st.vega_lite_chart(spec=spec, width="stretch")


def show_table(frame):
    table = frame.to_html(index=False, escape=True, border=0, classes="study-table")
    st.html(f'<div class="study-table-wrap" tabindex="0">{table}</div>')


def operations(tickets, config):
    st.subheader("Where support time goes")
    col1, col2, col3 = st.columns(3)
    region = col1.selectbox("Region", ["All regions", *sorted(tickets["region"].unique())])
    plan = col2.selectbox("Plan", ["All plans", *sorted(tickets["plan"].unique())])
    dimension = col3.selectbox("Group tickets by", DIMENSIONS, format_func=str.capitalize)
    if region != "All regions":
        tickets = tickets[tickets.region == region]
    if plan != "All plans":
        tickets = tickets[tickets.plan == plan]
    counts = len(tickets)
    if not counts:
        st.info("This filter has no tickets.")
        return
    kpi = st.columns(4)
    kpi[0].metric("Tickets", f"{counts:,}")
    kpi[1].metric("First-reply SLA", percent((tickets.first_reply_min <= tickets.sla_min).mean()))
    kpi[2].metric("Resolved in 7 days", percent(tickets.resolved_7d.mean()))
    kpi[3].metric("First reply, P90", f"{percentile90(tickets.first_reply_min.tolist()):.0f} min")
    rate = config["shared"]["hourly_rate"]
    groups = pd.DataFrame(summarize(tickets.to_dict("records"), dimension, rate))
    metric = st.radio("Chart measure", ["Ticket volume", "Labor cost", "SLA attainment"], horizontal=True)
    columns = {"Ticket volume": ("tickets", "Tickets"), "Labor cost": ("labor_usd", "Labor cost (USD)"),
               "SLA attainment": ("sla_pct", "First-reply SLA (%)")}
    field, label = columns[metric]
    chart = alt.Chart(groups).mark_bar(color="#08776e", cornerRadiusEnd=4).encode(
        x=alt.X(f"{field}:Q", title=label,
                scale=alt.Scale(domain=[0, 100]) if field == "sla_pct" else alt.Scale(zero=True)),
        y=alt.Y("segment:N", title=None, sort="ascending" if dimension == "week" else "-x"),
        tooltip=[alt.Tooltip("segment:N", title=dimension.capitalize()), "tickets",
                 alt.Tooltip("avg_handle_min:Q", title="Average handling (min)"),
                 alt.Tooltip("labor_usd:Q", title="Labor (USD)", format=",.0f"),
                 alt.Tooltip("sla_pct:Q", title="SLA (%)", format=".1f")],
    ).properties(height=max(240, 24 * len(groups)))
    show_chart(chart)
    show_table(groups.rename(columns={
        "segment": dimension.capitalize(), "tickets": "Tickets", "avg_handle_min": "Avg handling (min)",
        "avg_first_reply_min": "Avg first reply (min)", "avg_resolution_hours": "Avg resolution (hr)",
        "sla_met": "Within SLA", "sla_pct": "Within SLA (%)", "resolved_7d": "Resolved in 7 days",
        "resolution_pct": "Resolved in 7 days (%)", "reopen_pct": "Reopened in 7 days (%)",
        "labor_usd": "Labor (USD)",
    }))
    st.caption(f"January–March 2025, synthetic. Labor includes active handling at ${rate}/hour. "
               "Resolution counts cases closed within 7 days and still closed through day 7.")


def quality(report, decisions):
    st.subheader("Draft usefulness on held-out tickets")
    field = st.selectbox("Compare across", ["All tickets", "risk", "region", "expected_article"],
                         format_func=lambda value: {"risk": "Risk", "region": "Region",
                             "expected_article": "Expected article"}.get(value, value))
    if field != "All tickets":
        value = st.selectbox("Evaluation segment", sorted(decisions[field].unique()))
        decisions = decisions[decisions[field] == value]
    rows = []
    mix = []
    for policy in POLICIES:
        score = metrics(decisions[decisions.policy == policy].to_dict("records"))
        rows.append({"Policy": policy, "Tickets": score["tickets"], "Drafts / sends": score["offered"],
                     "Article match": percent(score["offer_accuracy"]),
                     "Correct and eligible": percent(score["safe_offer_precision"]),
                     "P90 first reply (min)": round(score["reply_p90_min"], 1),
                     "Within SLA (%)": round(score["sla_pct"], 1),
                     "Agent minutes / ticket": round(score["modeled_minutes"], 2)})
        mix.extend({"Policy": policy, "Action": label, "Share": score[key] / score["tickets"]}
                   for label, key in [("Manual", "human"), ("Agent review", "review"), ("Auto-send", "auto")])
    chart = alt.Chart(pd.DataFrame(mix)).mark_bar(size=24).encode(
        x=alt.X("Share:Q", title="Share of tickets", axis=alt.Axis(format=".0%")),
        y=alt.Y("Policy:N", title=None, sort=list(POLICIES)),
        color=alt.Color("Action:N", scale=alt.Scale(
            domain=["Manual", "Agent review", "Auto-send"], range=["#a9bbcb", "#08776e", "#ba7543"])),
        tooltip=["Policy", "Action", alt.Tooltip("Share:Q", format=".1%")],
    ).properties(height=170)
    show_chart(chart)
    show_table(pd.DataFrame(rows))
    st.caption("Correct and eligible requires the expected article and permission to handle the case through the proposed route. "
               "First reply and agent effort are modeled. An instant reply can still be wrong or unsafe.")
    with st.expander("Confidence calibration and threshold selection"):
        calibration = report["test_calibration"]
        st.write(f"The frozen review threshold is **{report['fit']['threshold']:.2f}**. "
                 f"The model scored **{calibration['scored']:,}** of 4,000 tickets. "
                 f"Held-out Brier score moved from **{calibration['raw_brier']:.3f}** raw "
                 f"to **{calibration['calibrated_brier']:.3f}** calibrated. Lower is better.")
        show_table(pd.DataFrame(calibration["bins"]).round(3))
        st.caption("Test bin accuracy is descriptive. Selection below uses February only.")
        show_table(pd.DataFrame(report["fit"]["selection"]).round(3))


def risk(report, challenge):
    st.subheader("Where automatic replies bypass escalation")
    rows = []
    for policy in POLICIES:
        score = report["benchmark"][policy]
        _, high = score["unsafe_interval"]
        rows.append({"Policy": policy, "Protected cases": score["protected"],
                     "Protected auto-sends": score["unsafe_auto"],
                     "Share of protected cases": percent(score["unsafe_rate_protected"]),
                     "Wilson 95% upper bound": f"{high:.2%}" if high is not None else "—",
                     "Protected drafts queued": score["protected_review"],
                     "Any invalid auto-send": score["bad_auto"]})
    show_table(pd.DataFrame(rows))
    st.caption("Protected cases require human escalation. Wilson bounds treat tickets as independent and are illustrative "
               "because the generator repeats wording families.")
    st.subheader("Inspect a challenge case")
    case = st.selectbox("Labeled stress case", challenge["case"].drop_duplicates().tolist())
    sample = challenge[challenge.case == case]
    labels = pd.read_csv(EVIDENCE / "challenge_labels.csv", keep_default_na=False)
    ticket = labels[labels.case == case].iloc[0]
    st.info(ticket["text"] or "(Empty message)")
    st.write(f"Expected article **{ticket['intent'] or 'None'}** · Mandatory escalation "
             f"**{'Yes' if ticket['must_escalate'] else 'No'}** · Intake signal **{ticket['intake_signal']}**")
    show_table(sample[["policy", "action", "article", "reason", "unsafe_auto", "response_text"]])


def finance(report, config):
    st.subheader("Recoverable capacity and implementation cost")
    st.caption("This model uses the broader March replay, including billing and workspace intents. "
               "The proposed Reporting-only pilot needs its own volume, case mix, and cost estimates.")
    cols = st.columns(4)
    shared = config["shared"]
    volume = cols[0].slider("Monthly tickets", 500, 12000, shared["monthly_volume"], step=100)
    realization = cols[1].slider("Capacity converted to value", 0, 100, round(shared["realization"] * 100),
                                 format="%d%%") / 100
    adoption = cols[2].slider("Workflow adoption", 0, 100, round(shared["adoption"] * 100),
                              format="%d%%") / 100
    rate = cols[3].slider("Loaded hourly cost (USD)", 10.0, 100.0, float(shared["hourly_rate"]), step=1.0)
    scenario = dict(monthly_volume=volume, realization=realization, adoption=adoption, hourly_rate=rate)
    rows, flows = [], []
    for policy in POLICIES:
        unit, assumptions = policy_economics(report["benchmark"][policy], policy, config, **scenario)
        result = calculate(unit, assumptions)
        rows.append({"Policy": policy, "Steady hours/mo": round(result["steady_hours_monthly"], 1),
                     "Year 1 cost": money(result["year1_cost"]), "Year 1 net": money(result["year1_net"]),
                     "Year 1 ROI": percent(result["year1_roi"]),
                     "Payback (months)": str(result["payback_month"]) if result["payback_month"] is not None else "—",
                     "Year 1 break-even tickets/mo": (f"{ceil(result['year1_break_even_volume']):,}"
                                                     if result["year1_break_even_volume"] is not None else "—")})
        flows.extend({"Policy": policy, **row} for row in result["cash_flows"])
    show_table(pd.DataFrame(rows))
    show_chart(alt.Chart(pd.DataFrame(flows)).mark_line(strokeWidth=2.5).encode(
        x=alt.X("month:Q", title="Months since launch", axis=alt.Axis(tickMinStep=1, tickCount=9)),
        y=alt.Y("cumulative:Q", title="Cumulative incremental value (USD)"), color=POLICY_COLOR,
        tooltip=["Policy", "month", alt.Tooltip("cumulative:Q", format=",.0f")],
    ).properties(height=280))
    st.caption("Values are incremental to manual support. Capacity becomes economic value only at the selected realization rate. "
               "Safety incidents are evaluated separately. Payback is shown within 24 months.")
    policy = st.selectbox("Sensitivity policy", POLICIES[1:], index=1)
    unit, assumptions = policy_economics(report["benchmark"][policy], policy, config, **scenario)
    grid = pd.DataFrame(sensitivity(unit, assumptions))
    show_chart(alt.Chart(grid).mark_rect(cornerRadius=4).encode(
        x=alt.X("monthly_volume:O", title="Monthly tickets", axis=alt.Axis(format=",d")),
        y=alt.Y("realization:O", title="Value realization", axis=alt.Axis(format=".0%")),
        color=alt.Color("year1_net:Q", title="Year 1 net (USD)",
                        scale=alt.Scale(scheme="brownbluegreen", domainMid=0)),
        tooltip=["monthly_volume", alt.Tooltip("realization:Q", format=".0%"),
                 alt.Tooltip("year1_net:Q", format=",.0f")],
    ).properties(height=180))
    low = calculate(unit, replace(assumptions, adoption=adoption * .75, realization=realization * .65))
    st.write(f"With 25% lower adoption and 35% lower realization, first-year net is **{money(low['year1_net'])}**.")
    st.download_button("Download selected sensitivity CSV", grid.to_csv(index=False), "sensitivity.csv")


def main():
    st.set_page_config(page_title="RelayDesk · Support Automation", page_icon="📊", layout="wide")
    st.markdown("""
        <style>
        .block-container {max-width: 1280px; padding-top: 2.6rem; padding-bottom: 3rem;}
        [data-testid="stMetric"] {background: #fff; border: 1px solid #dce5ec;
          border-radius: 12px; padding: 12px 16px;}
        [data-testid="stTabs"] button {font-weight: 650;}
        .study-table-wrap {overflow-x: auto; margin: .35rem 0 .5rem;}
        .study-table {width: 100%; border-collapse: collapse; background: #fff; font-size: .88rem;}
        .study-table thead {background: #eaf0f5;}
        .study-table th, .study-table td {padding: .58rem .65rem; border-bottom: 1px solid #dce5ec; text-align: left;}
        .study-table tbody tr:hover {background: #eef8f6;}
        </style>
        """, unsafe_allow_html=True)
    st.title("Support automation at RelayDesk")
    st.caption("Synthetic case study · 12,000 tickets · January–March 2025")
    if not (EVIDENCE / "summary.json").exists():
        st.info("Build the evidence first with python -m supportlab.study.")
        st.stop()
    report, tickets, decisions, challenge = read_evidence((EVIDENCE / "summary.json").stat().st_mtime_ns)
    config = load_config()
    ops_tab, quality_tab, risk_tab, finance_tab = st.tabs(["Operations", "Quality", "Risk", "Financial scenarios"])
    with ops_tab:
        operations(tickets, config)
    with quality_tab:
        quality(report, decisions)
    with risk_tab:
        risk(report, challenge)
    with finance_tab:
        finance(report, config)


if __name__ == "__main__":
    main()

