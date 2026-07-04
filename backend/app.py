"""
ML Data Drift Detection Dashboard
Interactive Streamlit app for detecting and visualising data drift
between a Reference and a Current dataset.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ── Local modules ─────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from validation import run_validation
from preprocessing import preprocess, get_feature_types
from feature_engineering import run_feature_engineering
from eda import (
    numerical_stats, categorical_stats,
    plot_histogram, plot_kde, plot_boxplot, plot_categorical_bar,
)
from drift import run_drift_detection
from report import build_report, to_csv_bytes, to_excel_bytes


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ML Data Drift Dashboard",
    page_icon="📊",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
    .drift-badge-yes {
        background: #ffe0e0;
        color: #c0392b;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 600;
    }
    .drift-badge-no {
        background: #e0f5e0;
        color: #27ae60;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 600;
    }
    .section-header {
        font-size: 1.2em;
        font-weight: 700;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar — File Upload ─────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
    st.title("📂 Upload Datasets")

    ref_file = st.file_uploader("Reference Dataset (CSV)", type=["csv"], key="ref")
    cur_file = st.file_uploader("Current Dataset (CSV)", type=["csv"], key="cur")

    st.markdown("---")
    st.markdown("### 📌 About")
    st.markdown(
        "Upload two structured CSV datasets. "
        "The dashboard will automatically validate, preprocess, "
        "analyse, and detect data drift between them."
    )
    st.markdown("---")
    st.caption("Built with Streamlit · SciPy · Pandas")


# ── Helper: load with fallback to sample data ─────────────────────────────────
@st.cache_data
def load_df(file_obj):
    return pd.read_csv(file_obj)


def load_sample():
    base = os.path.dirname(__file__)
    ref = pd.read_csv(os.path.join(base, "data", "reference.csv"))
    cur = pd.read_csv(os.path.join(base, "data", "current.csv"))
    return ref, cur


# ── Main ──────────────────────────────────────────────────────────────────────
st.title("📊 ML Data Drift Detection Dashboard")
st.markdown(
    "Automatically validate datasets, explore features, detect statistical drift, "
    "and download drift reports — for **any structured CSV dataset**."
)

# Load data
if ref_file and cur_file:
    ref_df_raw = load_df(ref_file)
    cur_df_raw = load_df(cur_file)
    data_source = "Uploaded"
else:
    if not ref_file and not cur_file:
        st.info("👈 Upload datasets in the sidebar, or explore the **sample loan dataset** below.")
    ref_df_raw, cur_df_raw = load_sample()
    data_source = "Sample"

st.caption(f"Using: **{data_source} Dataset**")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Validation", "📈 EDA", "🚨 Drift Detection", "📥 Reports"
])


# ── TAB 1 — Data Validation ───────────────────────────────────────────────────
with tab1:
    st.header("Data Validation")

    validation = run_validation(ref_df_raw, cur_df_raw)

    # Dataset Shapes
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Reference Dataset")
        r = validation["ref_shape"]
        st.metric("Rows", r["rows"])
        st.metric("Columns", r["columns"])
        st.dataframe(ref_df_raw.head(), use_container_width=True)
    with col2:
        st.subheader("Current Dataset")
        c = validation["cur_shape"]
        st.metric("Rows", c["rows"])
        st.metric("Columns", c["columns"])
        st.dataframe(cur_df_raw.head(), use_container_width=True)

    st.markdown("---")

    # Schema Validation
    schema = validation["schema"]
    if schema["schema_valid"]:
        st.success("✅ Schema is valid — columns and data types match between datasets.")
    else:
        st.error("⚠️ Schema mismatch detected.")
        col_cmp = schema["column_comparison"]
        if col_cmp["missing_in_current"]:
            st.warning(f"Missing in Current: `{col_cmp['missing_in_current']}`")
        if col_cmp["extra_in_current"]:
            st.warning(f"Extra in Current: `{col_cmp['extra_in_current']}`")
        if not schema["dtype_mismatches"].empty:
            st.warning("Data type mismatches:")
            st.dataframe(schema["dtype_mismatches"], use_container_width=True)

    st.subheader("Data Types Comparison")
    st.dataframe(schema["dtype_comparison"], use_container_width=True)

    st.markdown("---")

    # Missing Values
    st.subheader("Missing Values")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Reference")
        if validation["ref_missing"].empty:
            st.success("No missing values in Reference dataset.")
        else:
            st.dataframe(validation["ref_missing"], use_container_width=True)
    with col2:
        st.caption("Current")
        if validation["cur_missing"].empty:
            st.success("No missing values in Current dataset.")
        else:
            st.dataframe(validation["cur_missing"], use_container_width=True)

    # Duplicate Rows
    st.subheader("Duplicate Rows")
    col1, col2 = st.columns(2)
    with col1:
        rd = validation["ref_duplicates"]
        st.metric("Reference Duplicates", rd["duplicate_rows"],
                  delta=f"{rd['duplicate_pct']}%", delta_color="inverse")
    with col2:
        cd = validation["cur_duplicates"]
        st.metric("Current Duplicates", cd["duplicate_rows"],
                  delta=f"{cd['duplicate_pct']}%", delta_color="inverse")


# ── Preprocess once (shared across tabs) ─────────────────────────────────────
@st.cache_data
def get_preprocessed(ref_raw, cur_raw):
    ref_p = preprocess(ref_raw)
    cur_p = preprocess(cur_raw)
    ref_ft = get_feature_types(ref_p)
    cur_ft = get_feature_types(cur_p)
    # Feature engineering
    ref_eng = run_feature_engineering(ref_p, ref_ft["datetime"])
    cur_eng = run_feature_engineering(cur_p, cur_ft["datetime"])
    # Refresh feature types after engineering
    ref_ft = get_feature_types(ref_eng)
    return ref_eng, cur_eng, ref_ft


ref_df, cur_df, feature_types = get_preprocessed(
    ref_df_raw.to_json(), cur_df_raw.to_json()
)
# NOTE: st.cache_data serialises args, so we convert to JSON above and re-read
ref_df = pd.read_json(ref_df_raw.to_json())
cur_df = pd.read_json(cur_df_raw.to_json())
ref_df = preprocess(ref_df)
cur_df = preprocess(cur_df)
feature_types = get_feature_types(ref_df)
num_cols = feature_types["numerical"]
cat_cols = feature_types["categorical"]


# ── TAB 2 — EDA ──────────────────────────────────────────────────────────────
with tab2:
    st.header("Exploratory Data Analysis")

    c1, c2, c3 = st.columns(3)
    c1.metric("Numerical Features", len(num_cols))
    c2.metric("Categorical Features", len(cat_cols))
    c3.metric("Datetime Features", len(feature_types["datetime"]))

    if num_cols:
        st.subheader("Numerical Features — Statistics")
        ref_num_stats = numerical_stats(ref_df, num_cols)
        cur_num_stats = numerical_stats(cur_df, num_cols)
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Reference")
            st.dataframe(ref_num_stats, use_container_width=True)
        with col2:
            st.caption("Current")
            st.dataframe(cur_num_stats, use_container_width=True)

        st.subheader("Numerical Features — Visualisations")
        selected_num = st.selectbox("Select Numerical Feature", num_cols, key="eda_num")
        if selected_num:
            v1, v2, v3 = st.columns(3)
            with v1:
                st.caption("Histogram")
                fig = plot_histogram(ref_df, cur_df, selected_num)
                st.pyplot(fig)
                plt.close(fig)
            with v2:
                st.caption("KDE Plot")
                fig = plot_kde(ref_df, cur_df, selected_num)
                st.pyplot(fig)
                plt.close(fig)
            with v3:
                st.caption("Box Plot")
                fig = plot_boxplot(ref_df, cur_df, selected_num)
                st.pyplot(fig)
                plt.close(fig)

    if cat_cols:
        st.subheader("Categorical Features — Visualisations")
        selected_cat = st.selectbox("Select Categorical Feature", cat_cols, key="eda_cat")
        if selected_cat:
            cat_s = categorical_stats(ref_df, [selected_cat])[selected_cat]
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = plot_categorical_bar(ref_df, cur_df, selected_cat)
                st.pyplot(fig)
                plt.close(fig)
            with col2:
                st.metric("Unique Values (Ref)", cat_s["unique_values"])
                st.metric("Mode (Ref)", str(cat_s["mode"]))
                st.caption("Value Counts (Reference)")
                st.dataframe(cat_s["value_counts"].head(10), use_container_width=True)


# ── TAB 3 — Drift Detection ───────────────────────────────────────────────────
with tab3:
    st.header("Data Drift Detection")

    drift_df = run_drift_detection(ref_df, cur_df, num_cols, cat_cols)

    if drift_df.empty:
        st.warning("No features to analyse drift on.")
    else:
        # Summary metrics
        total = len(drift_df)
        drifted = drift_df["drift_status"].str.contains("Drift", na=False).sum()
        no_drift = total - drifted

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Features Tested", total)
        c2.metric("Drift Detected", int(drifted), delta_color="inverse",
                  delta=f"{round(drifted/total*100, 1)}%")
        c3.metric("Stable Features", int(no_drift))

        st.markdown("---")
        st.subheader("Drift Summary Table")

        # Colour-code drift status column
        def highlight_drift(val):
            if isinstance(val, str) and "Drift Detected" in val:
                return "background-color: #ffe0e0; color: #c0392b; font-weight: 600"
            elif isinstance(val, str) and "No Drift" in val:
                return "background-color: #e0f5e0; color: #27ae60"
            elif isinstance(val, str) and "Moderate" in val:
                return "background-color: #fff3cd; color: #856404"
            elif isinstance(val, str) and "Significant" in val:
                return "background-color: #ffe0e0; color: #c0392b"
            return ""

        styled = drift_df.style.applymap(
            highlight_drift, subset=["drift_status", "psi_status"]
        ).format({
            "statistic": "{:.4f}",
            "p_value": "{:.4f}",
            "psi": lambda x: f"{x:.4f}" if x is not None else "—",
        })
        st.dataframe(styled, use_container_width=True)

        # Feature drill-down
        st.markdown("---")
        st.subheader("Feature Drill-Down")
        selected_drift_feat = st.selectbox(
            "Select Feature", drift_df["feature"].tolist(), key="drift_feat"
        )
        if selected_drift_feat:
            row = drift_df[drift_df["feature"] == selected_drift_feat].iloc[0]
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Feature Type", row["feature_type"])
            d2.metric("Method", row["method"])
            d3.metric("Statistic", f"{row['statistic']:.4f}")
            d4.metric("P-Value", f"{row['p_value']:.4f}")

            status = row["drift_status"]
            if "Drift Detected" in status:
                st.error(f"🚨 {status}")
            else:
                st.success(f"✅ {status}")

            if row["psi"] is not None:
                psi_val = row["psi"]
                psi_status = row["psi_status"]
                st.metric("PSI Score", f"{psi_val:.4f}", help="PSI: <0.1 No Drift | 0.1-0.2 Moderate | >0.2 Significant")
                if psi_status == "No Drift":
                    st.success(f"PSI Status: {psi_status}")
                elif psi_status == "Moderate Drift":
                    st.warning(f"PSI Status: {psi_status}")
                else:
                    st.error(f"PSI Status: {psi_status}")

            # Show plot for the selected feature
            if row["feature_type"] == "Numerical" and selected_drift_feat in num_cols:
                col1, col2 = st.columns(2)
                with col1:
                    fig = plot_histogram(ref_df, cur_df, selected_drift_feat)
                    st.pyplot(fig)
                    plt.close(fig)
                with col2:
                    fig = plot_kde(ref_df, cur_df, selected_drift_feat)
                    st.pyplot(fig)
                    plt.close(fig)
            elif row["feature_type"] == "Categorical" and selected_drift_feat in cat_cols:
                fig = plot_categorical_bar(ref_df, cur_df, selected_drift_feat)
                st.pyplot(fig)
                plt.close(fig)


# ── TAB 4 — Reports ──────────────────────────────────────────────────────────
with tab4:
    st.header("Drift Report")

    drift_df_report = run_drift_detection(ref_df, cur_df, num_cols, cat_cols)
    report_df = build_report(drift_df_report)

    st.dataframe(report_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Download Report")
    col1, col2 = st.columns(2)

    with col1:
        csv_bytes = to_csv_bytes(report_df)
        st.download_button(
            label="⬇️ Download CSV Report",
            data=csv_bytes,
            file_name="drift_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        excel_bytes = to_excel_bytes(report_df)
        st.download_button(
            label="⬇️ Download Excel Report",
            data=excel_bytes,
            file_name="drift_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
