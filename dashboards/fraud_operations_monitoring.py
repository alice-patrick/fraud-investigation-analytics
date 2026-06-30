import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Fraud Operations Monitoring",
    page_icon="🚨",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"


# =========================
# Helpers
# =========================
def load_report(filename: str) -> pd.DataFrame:
    path = REPORTS_DIR / filename

    if not path.exists():
        st.warning(f"`reports/{filename}` was not found. Run the SQL report export first.")
        return pd.DataFrame()

    return pd.read_csv(path)


def money(value):
    try:
        value = float(value)
    except Exception:
        return value

    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def metric_sum(df, col):
    if df.empty or col not in df.columns:
        return 0
    return pd.to_numeric(df[col], errors="coerce").fillna(0).sum()


def metric_avg(df, col):
    if df.empty or col not in df.columns:
        return 0
    return pd.to_numeric(df[col], errors="coerce").fillna(0).mean()


def prepare_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


def show_download(df: pd.DataFrame, filename: str):
    if not df.empty:
        st.download_button(
            label=f"Download full {filename}",
            data=df.to_csv(index=False),
            file_name=filename,
            mime="text/csv",
            key=f"download_{filename}",
        )


def show_table(df: pd.DataFrame):
    st.dataframe(
        df.fillna("-"),
        width="stretch",
        hide_index=True,
    )


def bar_chart(df, x, y, title):
    if df.empty or x not in df.columns or y not in df.columns:
        return

    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=20, r=20, t=60, b=80),
        xaxis_tickangle=-90,
    )
    st.plotly_chart(fig, width="stretch")


def line_chart(df, x, y, title):
    if df.empty or x not in df.columns or y not in df.columns:
        return

    fig = px.line(df, x=x, y=y, markers=True, title=title)
    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=20, r=20, t=60, b=60),
    )
    st.plotly_chart(fig, width="stretch")


# =========================
# Sidebar
# =========================
st.sidebar.header("Dashboard Controls")

top_n = st.sidebar.slider(
    "Top Records / Chart Items",
    min_value=5,
    max_value=25,
    value=10,
    step=5,
)

st.sidebar.caption(
    "Use this control to keep the dashboard recruiter-friendly instead of flooding the screen with huge tables."
)


# =========================
# Header
# =========================
st.title("🚨 Fraud Operations Monitoring")

st.caption(
    "SQL-based fraud investigation dashboard focused on fraud operations: "
    "high-risk accounts, velocity behaviour, repeated destination accounts, "
    "cross-border exposure, and operational risk concentration."
)


# =========================
# Load reports
# =========================
top_operational_risks = load_report("top_operational_risks.csv")
high_risk_accounts = load_report("high_risk_accounts.csv")
high_velocity_transactions = load_report("high_velocity_transactions.csv")
repeated_destination_accounts = load_report("repeated_destination_accounts.csv")
cross_border_alerts = load_report("cross_border_alerts.csv")


# =========================
# Tabs
# =========================
tabs = st.tabs(
    [
        "Operational Risks",
        "High Risk Accounts",
        "High Velocity Transactions",
        "Repeated Destination Accounts",
        "Cross Border Alerts",
    ]
)


# =========================
# 1. Operational Risks
# =========================
with tabs[0]:
    st.header("Top Operational Risks")

    df = prepare_numeric(
        top_operational_risks,
        ["alerts", "confirmed_frauds", "avg_fraud_score", "total_expected_benefit"],
    )

    if not df.empty:
        df["fraud_conversion_rate"] = (
            df["confirmed_frauds"] / df["alerts"].replace(0, pd.NA) * 100
        ).fillna(0)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Alerts", f"{int(metric_sum(df, 'alerts')):,}")
        c2.metric("Confirmed Frauds", f"{int(metric_sum(df, 'confirmed_frauds')):,}")
        c3.metric(
            "Fraud Conversion Rate",
            f"{metric_sum(df, 'confirmed_frauds') / metric_sum(df, 'alerts') * 100:.2f}%",
        )
        c4.metric("Average Fraud Score", f"{metric_avg(df, 'avg_fraud_score'):.2f}")
        c5.metric("Expected Benefit / Loss", money(metric_sum(df, "total_expected_benefit")))

        st.info(
            "Purpose: summarize workload, confirmed fraud concentration, and fraud conversion by severity "
            "so analysts can prioritize operational review."
        )

        display = df.head(top_n).copy()
        display["total_expected_benefit"] = display["total_expected_benefit"].apply(money)

        st.subheader(f"Report Preview — Top {len(display)} Rows")
        show_table(display)

        show_download(df, "top_operational_risks.csv")

        severity_chart_df = (
            df.groupby("severity", as_index=False)
            .agg(
                confirmed_frauds=("confirmed_frauds", "sum"),
                fraud_conversion_rate=("fraud_conversion_rate", "mean"),
            )
        )

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                x=severity_chart_df["severity"],
                y=severity_chart_df["confirmed_frauds"],
                name="Confirmed Frauds",
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=severity_chart_df["severity"],
                y=severity_chart_df["fraud_conversion_rate"],
                mode="lines+markers",
                name="Fraud Conversion Rate (%)",
            ),
            secondary_y=True,
        )

        fig.update_layout(
            title="Fraud Performance by Severity",
            template="plotly_dark",
            height=520,
            margin=dict(l=20, r=20, t=70, b=80),
            legend_title_text="Metric",
        )

        fig.update_xaxes(title_text="Severity")
        fig.update_yaxes(title_text="Confirmed Frauds", secondary_y=False)
        fig.update_yaxes(title_text="Fraud Conversion Rate (%)", secondary_y=True)

        st.plotly_chart(fig, width="stretch")

        bar_chart(
            df,
            "severity",
            "total_expected_benefit",
            "Expected Benefit / Loss by Severity",
        )


# =========================
# 2. High Risk Accounts
# =========================
with tabs[1]:
    st.header("High Risk Accounts")

    df = prepare_numeric(
        high_risk_accounts,
        [
            "total_transactions",
            "total_alerts",
            "confirmed_frauds",
            "high_severity_alerts",
            "medium_severity_alerts",
            "avg_fraud_score",
            "max_fraud_score",
            "total_expected_loss",
            "avg_priority_score",
            "repeated_destination_events",
            "cross_border_transactions",
        ],
    )

    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Accounts", f"{len(df):,}")
        c2.metric("Total Alerts", f"{int(metric_sum(df, 'total_alerts')):,}")
        c3.metric("Confirmed Frauds", f"{int(metric_sum(df, 'confirmed_frauds')):,}")
        c4.metric("Expected Exposure", money(metric_sum(df, "total_expected_loss")))

        st.info(
            "Purpose: identify accounts with the highest expected fraud exposure "
            "for account-level investigation."
        )

        preview_cols = [
            "customer_id",
            "total_alerts",
            "confirmed_frauds",
            "high_severity_alerts",
            "avg_fraud_score",
            "max_fraud_score",
            "total_expected_loss",
            "repeated_destination_events",
            "cross_border_transactions",
        ]
        preview_cols = [c for c in preview_cols if c in df.columns]

        display = (
            df.sort_values("total_expected_loss", ascending=False)[preview_cols]
            .head(top_n)
            .copy()
        )

        if "total_expected_loss" in display.columns:
            display["total_expected_loss"] = display["total_expected_loss"].apply(money)

        st.subheader(f"Report Preview — Top {len(display)} Rows")
        show_table(display)

        show_download(df, "high_risk_accounts.csv")

        if "customer_id" in df.columns and "total_expected_loss" in df.columns:
            top_accounts = (
                df.sort_values("total_expected_loss", ascending=False)
                .head(top_n)
                .copy()
            )

            bar_chart(
                top_accounts,
                "customer_id",
                "total_expected_loss",
                f"Top {top_n} Accounts by Expected Exposure",
            )

        st.divider()
        st.subheader("Account Investigation Drill-Down")

        if "customer_id" not in df.columns:
            st.warning("No customer_id column available for account drill-down.")
        else:
            account_options = df["customer_id"].astype(str).tolist()

            selected_account = st.selectbox(
                "Investigate Account",
                account_options,
                index=0,
            )

            selected_rows = []

            source_map = {
                "High Risk Account": high_risk_accounts,
                "High Velocity Activity": high_velocity_transactions,
                "Repeated Destination": repeated_destination_accounts,
                "Cross Border Alert": cross_border_alerts,
            }

            for source_name, source_df in source_map.items():
                if source_df.empty:
                    continue

                if "customer_id" in source_df.columns:
                    temp = source_df[
                        source_df["customer_id"].astype(str) == selected_account
                    ].copy()

                    if not temp.empty:
                        temp["report_source"] = source_name
                        selected_rows.append(temp)

            if selected_rows:
                investigation_df = pd.concat(selected_rows, ignore_index=True)

                investigation_df = prepare_numeric(
                    investigation_df,
                    [
                        "avg_fraud_score",
                        "max_fraud_score",
                        "total_expected_loss",
                        "expected_loss",
                        "total_alerts",
                        "alerts",
                        "confirmed_frauds",
                        "frauds",
                        "total_transactions",
                        "high_severity_alerts",
                        "medium_severity_alerts",
                        "repeated_destination_events",
                        "cross_border_transactions",
                    ],
                )

                expected_loss_value = (
                    metric_sum(investigation_df, "total_expected_loss")
                    or metric_sum(investigation_df, "expected_loss")
                )

                alerts_value = (
                    metric_sum(investigation_df, "total_alerts")
                    or metric_sum(investigation_df, "alerts")
                )

                frauds_value = (
                    metric_sum(investigation_df, "confirmed_frauds")
                    or metric_sum(investigation_df, "frauds")
                )

                risk_score_value = max(
                    metric_avg(investigation_df, "avg_fraud_score"),
                    metric_avg(investigation_df, "max_fraud_score"),
                )

                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Risk Score", f"{risk_score_value:.2f}")
                c2.metric("Expected Loss", money(expected_loss_value))
                c3.metric("Alerts", f"{int(alerts_value):,}")
                c4.metric("Confirmed Frauds", f"{int(frauds_value):,}")
                c5.metric("Report Sources", f"{investigation_df['report_source'].nunique()}")

                st.subheader("Investigation Summary by Source")

                summary_rows = []

                for source_name, source_group in investigation_df.groupby("report_source"):
                    summary_rows.append(
                        {
                            "report_source": source_name,
                            "risk_score": max(
                                metric_avg(source_group, "avg_fraud_score"),
                                metric_avg(source_group, "max_fraud_score"),
                            ),
                            "expected_loss": (
                                metric_sum(source_group, "total_expected_loss")
                                or metric_sum(source_group, "expected_loss")
                            ),
                            "alerts": (
                                metric_sum(source_group, "total_alerts")
                                or metric_sum(source_group, "alerts")
                            ),
                            "confirmed_frauds": (
                                metric_sum(source_group, "confirmed_frauds")
                                or metric_sum(source_group, "frauds")
                            ),
                            "transactions": metric_sum(source_group, "total_transactions"),
                            "high_severity_alerts": metric_sum(source_group, "high_severity_alerts"),
                            "repeated_destination_events": metric_sum(
                                source_group,
                                "repeated_destination_events",
                            ),
                            "cross_border_transactions": metric_sum(
                                source_group,
                                "cross_border_transactions",
                            ),
                        }
                    )

                investigation_summary = pd.DataFrame(summary_rows)

                if "expected_loss" in investigation_summary.columns:
                    investigation_summary["expected_loss"] = investigation_summary[
                        "expected_loss"
                    ].apply(money)

                if "risk_score" in investigation_summary.columns:
                    investigation_summary["risk_score"] = investigation_summary[
                        "risk_score"
                    ].round(2)

                show_table(investigation_summary)

                st.subheader("Raw Linked Investigation Rows")

                raw_cols = [
                    "report_source",
                    "customer_id",
                    "total_transactions",
                    "total_alerts",
                    "confirmed_frauds",
                    "high_severity_alerts",
                    "medium_severity_alerts",
                    "avg_fraud_score",
                    "max_fraud_score",
                    "total_expected_loss",
                    "expected_loss",
                    "avg_priority_score",
                    "repeated_destination_events",
                    "cross_border_transactions",
                ]
                raw_cols = [c for c in raw_cols if c in investigation_df.columns]

                raw_display = investigation_df[raw_cols].head(top_n).copy()

                for col in ["total_expected_loss", "expected_loss"]:
                    if col in raw_display.columns:
                        raw_display[col] = raw_display[col].apply(money)

                show_table(raw_display)

                st.download_button(
                    label=f"Download investigation_{selected_account}.csv",
                    data=investigation_df.to_csv(index=False),
                    file_name=f"investigation_{selected_account}.csv",
                    mime="text/csv",
                    key=f"download_investigation_{selected_account}",
                )
            else:
                st.warning("No linked investigation rows found for this account.")


# =========================
# 3. High Velocity Transactions
# =========================
with tabs[2]:
    st.header("High Velocity Transactions")

    df = prepare_numeric(
        high_velocity_transactions,
        [
            "step",
            "transactions_in_step",
            "alerts_in_step",
            "confirmed_frauds_in_step",
            "total_amount",
            "avg_fraud_score",
            "max_fraud_score",
            "total_expected_loss",
        ],
    )

    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(
            "Accounts",
            f"{df['customer_id'].nunique() if 'customer_id' in df.columns else len(df):,}",
        )
        c2.metric("Velocity Alerts", f"{int(metric_sum(df, 'alerts_in_step')):,}")
        c3.metric("Confirmed Frauds", f"{int(metric_sum(df, 'confirmed_frauds_in_step')):,}")
        c4.metric("Total Amount", money(metric_sum(df, "total_amount")))

        st.info(
            "Purpose: detect burst behaviour where accounts create suspicious activity "
            "within short time windows."
        )

        preview_cols = [
            "customer_id",
            "step",
            "transactions_in_step",
            "alerts_in_step",
            "confirmed_frauds_in_step",
            "total_amount",
            "avg_fraud_score",
            "max_fraud_score",
            "total_expected_loss",
        ]
        preview_cols = [c for c in preview_cols if c in df.columns]

        display = df[preview_cols].head(top_n).copy()

        for col in ["total_amount", "total_expected_loss"]:
            if col in display.columns:
                display[col] = display[col].apply(money)

        st.subheader(f"Report Preview — Top {len(display)} Rows")
        show_table(display)

        show_download(df, "high_velocity_transactions.csv")

        if "step" in df.columns and "alerts_in_step" in df.columns:
            step_df = df.groupby("step", as_index=False)["alerts_in_step"].sum()
            line_chart(step_df, "step", "alerts_in_step", "Alert Volume by Step")

        if "customer_id" in df.columns and "total_expected_loss" in df.columns:
            top_velocity = (
                df.sort_values("total_expected_loss", ascending=False)
                .head(top_n)
                .copy()
            )

            bar_chart(
                top_velocity,
                "customer_id",
                "total_expected_loss",
                f"Top {top_n} Velocity Accounts by Expected Exposure",
            )


# =========================
# 4. Repeated Destination Accounts
# =========================
with tabs[3]:
    st.header("Repeated Destination Accounts")

    df = prepare_numeric(
        repeated_destination_accounts,
        [
            "total_incoming_transactions",
            "unique_senders",
            "total_alerts",
            "confirmed_frauds",
            "high_severity_alerts",
            "avg_fraud_score",
            "max_fraud_score",
            "total_expected_loss",
            "avg_priority_score",
        ],
    )

    if not df.empty:
        if "destination_risk_index" not in df.columns:
            df["destination_risk_index"] = (
                df.get("total_alerts", 0)
                + df.get("unique_senders", 0) * 0.25
                + df.get("confirmed_frauds", 0) * 3
                + df.get("high_severity_alerts", 0) * 2
            )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Destination Accounts", f"{len(df):,}")
        c2.metric("Total Alerts", f"{int(metric_sum(df, 'total_alerts')):,}")
        c3.metric("Confirmed Frauds", f"{int(metric_sum(df, 'confirmed_frauds')):,}")
        c4.metric("Expected Exposure", money(metric_sum(df, "total_expected_loss")))

        st.info(
            "Purpose: surface repeated destination accounts that may indicate mule-account behaviour, "
            "coordinated transfers, or repeated suspicious inflows."
        )

        preview_cols = [
            "destination_account",
            "total_incoming_transactions",
            "unique_senders",
            "total_alerts",
            "confirmed_frauds",
            "high_severity_alerts",
            "avg_fraud_score",
            "max_fraud_score",
            "total_expected_loss",
            "avg_priority_score",
            "destination_risk_index",
        ]
        preview_cols = [c for c in preview_cols if c in df.columns]

        display = (
            df.sort_values("destination_risk_index", ascending=False)[preview_cols]
            .head(top_n)
            .copy()
        )

        if "total_expected_loss" in display.columns:
            display["total_expected_loss"] = display["total_expected_loss"].apply(money)

        st.subheader(f"Report Preview — Top {len(display)} Risk Destinations")
        show_table(display)

        show_download(df, "repeated_destination_accounts.csv")

        top_dest = (
            df.sort_values("destination_risk_index", ascending=False)
            .head(top_n)
            .copy()
        )

        if "destination_account" in top_dest.columns and "destination_risk_index" in top_dest.columns:
            bar_chart(
                top_dest,
                "destination_account",
                "destination_risk_index",
                f"Top {top_n} Destination Accounts by Risk Index",
            )

        if "destination_account" in top_dest.columns and "total_expected_loss" in top_dest.columns:
            bar_chart(
                top_dest.sort_values("total_expected_loss", ascending=False),
                "destination_account",
                "total_expected_loss",
                f"Top {top_n} Destination Accounts by Expected Exposure",
            )

# =========================
# 5. Cross Border Alerts
# =========================
with tabs[4]:
    st.header("Cross Border Alerts")

    df = prepare_numeric(
        cross_border_alerts,
        [
            "amount",
            "fraud_score",
            "expected_loss",
            "priority_score",
        ]
    )

    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)

        if "country" in df.columns:
            c1.metric("Countries", f"{df['country'].nunique():,}")
        else:
            c1.metric("Countries", "-")

        c2.metric("Transactions", f"{len(df):,}")

        if "expected_loss" in df.columns:
            c3.metric("Expected Exposure", money(metric_sum(df, "expected_loss")))
        else:
            c3.metric("Expected Exposure", "-")

        if "fraud_score" in df.columns:
            c4.metric("Average Fraud Score", f"{metric_avg(df, 'fraud_score'):.2f}")
        else:
            c4.metric("Average Fraud Score", "-")

        st.info("Purpose: monitor geographic, channel, and device-level fraud exposure.")

        preview_cols = [
            "transaction_id",
            "step",
            "customer_id",
            "destination_account",
            "transaction_type",
            "country",
            "device_type",
            "channel",
            "amount",
            "fraud_score",
            "expected_loss",
            "priority_score",
            "alert_severity",
            "investigation_status",
            "alert_reason",
        ]
        preview_cols = [c for c in preview_cols if c in df.columns]

        display = df[preview_cols].head(top_n).copy()
        for col in ["amount", "expected_loss"]:
            if col in display.columns:
                display[col] = display[col].apply(money)

        st.subheader(f"Report Preview — Top {len(display)} Rows")
        st.dataframe(display, use_container_width=True, hide_index=True)

        show_download(df, "cross_border_alerts.csv")

        if "country" in df.columns:
            country_df = df.groupby("country", as_index=False).agg(
                expected_loss=("expected_loss", "sum"),
                avg_fraud_score=("fraud_score", "mean"),
                transactions=("transaction_id", "count")
            )

            stacked_country = country_df.copy()

            stacked_country["expected_loss_index"] = (
                stacked_country["expected_loss"] / stacked_country["expected_loss"].max() * 100
            )

            stacked_country["avg_fraud_score_index"] = (
                stacked_country["avg_fraud_score"] / stacked_country["avg_fraud_score"].max() * 100
            )

            stacked_country["transaction_volume_index"] = (
                stacked_country["transactions"] / stacked_country["transactions"].max() * 100
            )

            melted_country = stacked_country.melt(
                id_vars="country",
                value_vars=[
                    "expected_loss_index",
                    "avg_fraud_score_index",
                    "transaction_volume_index",
                ],
                var_name="cross_border_signal",
                value_name="risk_index",
            )

            fig = px.bar(
                melted_country,
                x="country",
                y="risk_index",
                color="cross_border_signal",
                title="Cross-Border Exposure — Combined Risk Signals",
                barmode="stack",
            )

            fig.update_layout(
                template="plotly_dark",
                height=520,
                margin=dict(l=20, r=20, t=70, b=80),
                legend_title_text="Risk Signal",
            )

            st.plotly_chart(fig, use_container_width=True)

# =========================
# Footer
# =========================
st.info("Flow: SQL investigation queries → CSV reports → Fraud Operations Monitoring dashboard.")