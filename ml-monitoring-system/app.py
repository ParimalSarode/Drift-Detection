import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

REPORT_PATH = BASE_DIR / "reports" / "drift_report.csv"

st.set_page_config(
    page_title="ML Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)


def load_report():
    if not REPORT_PATH.exists():
        return None

    return pd.read_csv(REPORT_PATH)


def main():

    st.title("📊 ML Monitoring Dashboard")
    st.caption("Bank Customer Churn — Data Drift Monitoring")

    report = load_report()

    if report is None:
        st.error(
            "Drift report not found. "
            "Run the monitoring pipeline first."
        )
        st.code(
            "uv run python -m src.prepare_data\n"
            "uv run python -m src.run_monitoring"
        )
        return

    total_features = len(report)
    drifted_features = int(report["ks_drift"].sum())

    if drifted_features > 0:
        status = "⚠️ DRIFT DETECTED"
    else:
        status = "✅ NO SIGNIFICANT DRIFT"

    st.subheader("Overall Status")

    st.metric(
        "Monitoring Status",
        status
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Features Monitored",
            total_features
        )

    with col2:
        st.metric(
            "Features With Drift",
            drifted_features
        )

    st.divider()

    st.subheader("Feature Drift Report")

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()