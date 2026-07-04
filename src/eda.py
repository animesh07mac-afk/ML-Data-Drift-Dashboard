"""
Module 4: Exploratory Data Analysis (EDA)
Computes descriptive statistics and generates visualizations for any dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional


# ── Styling ──────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
PALETTE = {"Reference": "#4C72B0", "Current": "#DD8452"}


# ── Numerical Statistics ──────────────────────────────────────────────────────

def numerical_stats(df: pd.DataFrame, numerical_cols: list) -> pd.DataFrame:
    """
    Compute mean, median, std, variance, min, max for each numerical column.
    """
    if not numerical_cols:
        return pd.DataFrame()

    records = []
    for col in numerical_cols:
        series = df[col].dropna()
        records.append({
            "feature": col,
            "mean": round(series.mean(), 4),
            "median": round(series.median(), 4),
            "std": round(series.std(), 4),
            "variance": round(series.var(), 4),
            "min": round(series.min(), 4),
            "max": round(series.max(), 4),
            "count": len(series),
        })
    return pd.DataFrame(records)


# ── Categorical Statistics ────────────────────────────────────────────────────

def categorical_stats(df: pd.DataFrame, categorical_cols: list) -> dict:
    """
    Compute unique count, value counts, and mode for each categorical column.
    Returns a dict keyed by column name.
    """
    stats = {}
    for col in categorical_cols:
        series = df[col].dropna()
        stats[col] = {
            "unique_values": series.nunique(),
            "mode": series.mode().iloc[0] if not series.mode().empty else None,
            "value_counts": series.value_counts().reset_index().rename(
                columns={"index": col, col: "count"}
            ),
        }
    return stats


# ── Visualizations ────────────────────────────────────────────────────────────

def plot_histogram(ref_df: pd.DataFrame, cur_df: pd.DataFrame,
                   col: str, ax: Optional[plt.Axes] = None) -> plt.Figure:
    """Plot overlapping histograms for a numerical feature."""
    fig, ax = _get_ax(ax)
    ax.hist(ref_df[col].dropna(), bins=30, alpha=0.6, label="Reference",
            color=PALETTE["Reference"], edgecolor="white")
    ax.hist(cur_df[col].dropna(), bins=30, alpha=0.6, label="Current",
            color=PALETTE["Current"], edgecolor="white")
    ax.set_title(f"Histogram — {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.tight_layout()
    return fig


def plot_kde(ref_df: pd.DataFrame, cur_df: pd.DataFrame,
             col: str, ax: Optional[plt.Axes] = None) -> plt.Figure:
    """Plot KDE curves for a numerical feature."""
    fig, ax = _get_ax(ax)
    ref_series = ref_df[col].dropna()
    cur_series = cur_df[col].dropna()
    if len(ref_series) > 1:
        ref_series.plot.kde(ax=ax, label="Reference", color=PALETTE["Reference"])
    if len(cur_series) > 1:
        cur_series.plot.kde(ax=ax, label="Current", color=PALETTE["Current"])
    ax.set_title(f"KDE Plot — {col}")
    ax.set_xlabel(col)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_boxplot(ref_df: pd.DataFrame, cur_df: pd.DataFrame,
                 col: str, ax: Optional[plt.Axes] = None) -> plt.Figure:
    """Plot side-by-side box plots for a numerical feature."""
    fig, ax = _get_ax(ax)
    data = pd.concat([
        ref_df[[col]].assign(Dataset="Reference"),
        cur_df[[col]].assign(Dataset="Current"),
    ])
    sns.boxplot(data=data, x="Dataset", y=col, palette=PALETTE, ax=ax)
    ax.set_title(f"Box Plot — {col}")
    plt.tight_layout()
    return fig


def plot_categorical_bar(ref_df: pd.DataFrame, cur_df: pd.DataFrame,
                         col: str, top_n: int = 15) -> plt.Figure:
    """Plot grouped bar chart comparing category distributions."""
    ref_counts = ref_df[col].value_counts(normalize=True).rename("Reference")
    cur_counts = cur_df[col].value_counts(normalize=True).rename("Current")

    combined = pd.concat([ref_counts, cur_counts], axis=1).fillna(0).head(top_n)
    fig, ax = plt.subplots(figsize=(8, 4))
    combined.plot(kind="bar", ax=ax,
                  color=[PALETTE["Reference"], PALETTE["Current"]])
    ax.set_title(f"Category Distribution — {col}")
    ax.set_ylabel("Proportion")
    ax.set_xlabel(col)
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Dataset")
    plt.tight_layout()
    return fig


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_ax(ax):
    """Return a (fig, ax) pair, creating a new figure if ax is None."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))
        return fig, ax
    return ax.get_figure(), ax
