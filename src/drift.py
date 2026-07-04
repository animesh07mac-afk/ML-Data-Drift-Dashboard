"""
Module 5: Data Drift Detection
Implements KS Test + PSI for numerical features and Chi-Square Test for categorical features.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Tuple


# ── PSI Helper ────────────────────────────────────────────────────────────────

def _compute_psi(reference: np.ndarray, current: np.ndarray,
                 buckets: int = 10) -> float:
    """
    Compute the Population Stability Index (PSI) between two distributions.
    PSI < 0.1  → No significant change
    PSI 0.1-0.2 → Moderate change
    PSI > 0.2  → Significant change
    """
    # Build bin edges on the reference distribution
    breakpoints = np.percentile(reference, np.linspace(0, 100, buckets + 1))
    breakpoints = np.unique(breakpoints)  # remove duplicate edges

    if len(breakpoints) < 2:
        return 0.0  # degenerate distribution

    ref_counts, _ = np.histogram(reference, bins=breakpoints)
    cur_counts, _ = np.histogram(current, bins=breakpoints)

    # Convert to proportions, clip zeros to avoid log(0)
    eps = 1e-6
    ref_pct = ref_counts / (len(reference) + eps)
    cur_pct = cur_counts / (len(current) + eps)
    ref_pct = np.clip(ref_pct, eps, None)
    cur_pct = np.clip(cur_pct, eps, None)

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return round(float(psi), 6)


# ── Drift Labels ──────────────────────────────────────────────────────────────

def _ks_drift_label(p_value: float, threshold: float = 0.05) -> str:
    return "Drift Detected" if p_value < threshold else "No Drift"


def _psi_drift_label(psi: float) -> str:
    if psi < 0.1:
        return "No Drift"
    elif psi < 0.2:
        return "Moderate Drift"
    else:
        return "Significant Drift"


def _chi2_drift_label(p_value: float, threshold: float = 0.05) -> str:
    return "Drift Detected" if p_value < threshold else "No Drift"


# ── Numerical Drift ───────────────────────────────────────────────────────────

def detect_numerical_drift(ref_df: pd.DataFrame, cur_df: pd.DataFrame,
                            numerical_cols: list) -> pd.DataFrame:
    """
    Run KS Test and PSI for each numerical feature.
    Returns a DataFrame with drift results.
    """
    records = []
    for col in numerical_cols:
        ref_vals = ref_df[col].dropna().values
        cur_vals = cur_df[col].dropna().values

        if len(ref_vals) == 0 or len(cur_vals) == 0:
            continue

        # KS Test
        ks_stat, ks_p = stats.ks_2samp(ref_vals, cur_vals)

        # PSI
        psi_score = _compute_psi(ref_vals, cur_vals)

        records.append({
            "feature": col,
            "feature_type": "Numerical",
            "method": "KS Test",
            "statistic": round(ks_stat, 6),
            "p_value": round(ks_p, 6),
            "psi": psi_score,
            "drift_status": _ks_drift_label(ks_p),
            "psi_status": _psi_drift_label(psi_score),
        })

    return pd.DataFrame(records)


# ── Categorical Drift ─────────────────────────────────────────────────────────

def detect_categorical_drift(ref_df: pd.DataFrame, cur_df: pd.DataFrame,
                              categorical_cols: list) -> pd.DataFrame:
    """
    Run Chi-Square Test for each categorical feature.
    Returns a DataFrame with drift results.
    """
    records = []
    for col in categorical_cols:
        ref_series = ref_df[col].dropna().astype(str)
        cur_series = cur_df[col].dropna().astype(str)

        all_cats = sorted(set(ref_series.unique()) | set(cur_series.unique()))
        if not all_cats:
            continue

        ref_counts = ref_series.value_counts().reindex(all_cats, fill_value=0)
        cur_counts = cur_series.value_counts().reindex(all_cats, fill_value=0)

        # Chi-square test requires at least 2 categories
        if len(all_cats) < 2:
            chi2, p_val = 0.0, 1.0
        else:
            # Combine counts into a contingency table
            contingency = np.array([ref_counts.values, cur_counts.values])
            # Drop columns where both rows are 0 to avoid issues
            mask = contingency.sum(axis=0) > 0
            contingency = contingency[:, mask]
            if contingency.shape[1] < 2:
                chi2, p_val = 0.0, 1.0
            else:
                chi2, p_val, _, _ = stats.chi2_contingency(contingency)

        records.append({
            "feature": col,
            "feature_type": "Categorical",
            "method": "Chi-Square Test",
            "statistic": round(float(chi2), 6),
            "p_value": round(float(p_val), 6),
            "psi": None,
            "drift_status": _chi2_drift_label(p_val),
            "psi_status": None,
        })

    return pd.DataFrame(records)


# ── Combined Drift Report ─────────────────────────────────────────────────────

def run_drift_detection(ref_df: pd.DataFrame, cur_df: pd.DataFrame,
                        numerical_cols: list, categorical_cols: list) -> pd.DataFrame:
    """
    Run all drift detection tests and return a unified results DataFrame.
    """
    num_drift = detect_numerical_drift(ref_df, cur_df, numerical_cols)
    cat_drift = detect_categorical_drift(ref_df, cur_df, categorical_cols)
    return pd.concat([num_drift, cat_drift], ignore_index=True)
