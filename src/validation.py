"""
Module 1: Data Validation
Validates reference and current datasets before analysis.
"""

import pandas as pd
import numpy as np


def load_dataset(filepath: str) -> pd.DataFrame:
    """Load a CSV dataset from the given filepath."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise ValueError(f"Failed to load dataset from {filepath}: {e}")


def get_shape_info(df: pd.DataFrame, name: str = "Dataset") -> dict:
    """Return shape information for the dataset."""
    return {
        "name": name,
        "rows": df.shape[0],
        "columns": df.shape[1],
    }


def compare_columns(ref_df: pd.DataFrame, cur_df: pd.DataFrame) -> dict:
    """
    Compare column names between reference and current datasets.
    Returns missing and extra columns in current vs reference.
    """
    ref_cols = set(ref_df.columns)
    cur_cols = set(cur_df.columns)

    return {
        "common_columns": sorted(ref_cols & cur_cols),
        "missing_in_current": sorted(ref_cols - cur_cols),
        "extra_in_current": sorted(cur_cols - ref_cols),
        "columns_match": ref_cols == cur_cols,
    }


def compare_dtypes(ref_df: pd.DataFrame, cur_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare data types of common columns across both datasets.
    Returns a DataFrame with dtype comparison.
    """
    common_cols = list(set(ref_df.columns) & set(cur_df.columns))
    dtype_comparison = pd.DataFrame({
        "column": common_cols,
        "ref_dtype": [str(ref_df[c].dtype) for c in common_cols],
        "cur_dtype": [str(cur_df[c].dtype) for c in common_cols],
    })
    dtype_comparison["dtype_match"] = dtype_comparison["ref_dtype"] == dtype_comparison["cur_dtype"]
    return dtype_comparison.sort_values("column").reset_index(drop=True)


def missing_values_summary(df: pd.DataFrame, name: str = "Dataset") -> pd.DataFrame:
    """Return a summary of missing values per column."""
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    summary = pd.DataFrame({
        "column": missing.index,
        "missing_count": missing.values,
        "missing_pct": pct.values,
    })
    summary = summary[summary["missing_count"] > 0].reset_index(drop=True)
    summary["dataset"] = name
    return summary


def duplicate_rows_summary(df: pd.DataFrame, name: str = "Dataset") -> dict:
    """Return count of duplicate rows."""
    dup_count = df.duplicated().sum()
    return {
        "dataset": name,
        "total_rows": len(df),
        "duplicate_rows": int(dup_count),
        "duplicate_pct": round(dup_count / len(df) * 100, 2),
    }


def validate_schema(ref_df: pd.DataFrame, cur_df: pd.DataFrame) -> dict:
    """
    Perform full schema validation between reference and current datasets.
    Returns a consolidated validation report.
    """
    col_comparison = compare_columns(ref_df, cur_df)
    dtype_comparison = compare_dtypes(ref_df, cur_df)
    dtype_mismatches = dtype_comparison[~dtype_comparison["dtype_match"]]

    schema_valid = (
        col_comparison["columns_match"]
        and dtype_mismatches.empty
    )

    return {
        "schema_valid": schema_valid,
        "column_comparison": col_comparison,
        "dtype_comparison": dtype_comparison,
        "dtype_mismatches": dtype_mismatches,
    }


def run_validation(ref_df: pd.DataFrame, cur_df: pd.DataFrame) -> dict:
    """
    Run all validation checks and return a complete validation report dict.
    """
    report = {
        "ref_shape": get_shape_info(ref_df, "Reference"),
        "cur_shape": get_shape_info(cur_df, "Current"),
        "schema": validate_schema(ref_df, cur_df),
        "ref_missing": missing_values_summary(ref_df, "Reference"),
        "cur_missing": missing_values_summary(cur_df, "Current"),
        "ref_duplicates": duplicate_rows_summary(ref_df, "Reference"),
        "cur_duplicates": duplicate_rows_summary(cur_df, "Current"),
    }
    return report
