"""
Module 3: Feature Engineering
Extracts datetime features and computes derived columns generically.
"""

import pandas as pd
import numpy as np
from datetime import datetime


# Common patterns for date-of-birth column names (case-insensitive)
DOB_KEYWORDS = ["dob", "birth", "birthdate", "date_of_birth", "dateofbirth"]


def is_dob_column(col_name: str) -> bool:
    """Heuristic check if a column name looks like a date-of-birth column."""
    return any(kw in col_name.lower() for kw in DOB_KEYWORDS)


def extract_datetime_features(df: pd.DataFrame, datetime_cols: list) -> pd.DataFrame:
    """
    For each detected datetime column, extract:
    year, month, day, hour, day_of_week.
    If the column looks like a DOB, also compute age.
    """
    df = df.copy()
    for col in datetime_cols:
        # Ensure column is datetime
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")

        prefix = col
        df[f"{prefix}_year"] = df[col].dt.year
        df[f"{prefix}_month"] = df[col].dt.month
        df[f"{prefix}_day"] = df[col].dt.day
        df[f"{prefix}_hour"] = df[col].dt.hour
        df[f"{prefix}_day_of_week"] = df[col].dt.dayofweek

        # Compute age if column is likely a date-of-birth
        if is_dob_column(col):
            today = pd.Timestamp(datetime.today().date())
            df[f"{prefix}_age"] = (today - df[col]).dt.days // 365

    return df


def run_feature_engineering(df: pd.DataFrame, datetime_cols: list) -> pd.DataFrame:
    """
    Main entry point: apply all feature engineering steps and return enriched DataFrame.
    """
    if datetime_cols:
        df = extract_datetime_features(df, datetime_cols)
    return df
