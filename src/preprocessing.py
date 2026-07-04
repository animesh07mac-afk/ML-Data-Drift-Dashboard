"""
Module 2: Data Preprocessing
Handles cleaning, type detection, and preparation of datasets for analysis.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the dataset."""
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    after = len(df)
    if before != after:
        print(f"  Removed {before - after} duplicate rows.")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values automatically:
    - Numerical columns: fill with median
    - Categorical columns: fill with mode
    """
    df = df.copy()
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col].fillna(df[col].median(), inplace=True)
        else:
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col].fillna(mode_val[0], inplace=True)
            else:
                df[col].fillna("Unknown", inplace=True)
    return df


def detect_numerical_features(df: pd.DataFrame) -> list:
    """Return list of numerical feature column names."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def detect_categorical_features(df: pd.DataFrame) -> list:
    """Return list of categorical/object feature column names."""
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def detect_datetime_features(df: pd.DataFrame) -> list:
    """
    Detect datetime columns by checking dtype and attempting to parse
    object columns that look like dates.
    """
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    # Try to parse object columns as datetime
    for col in df.select_dtypes(include=["object"]).columns:
        sample = df[col].dropna().head(20)
        try:
            parsed = pd.to_datetime(sample, infer_datetime_format=True, errors="coerce")
            if parsed.notna().sum() > len(sample) * 0.8:
                datetime_cols.append(col)
        except Exception:
            pass

    return list(set(datetime_cols))


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run full preprocessing pipeline:
    1. Remove duplicates
    2. Handle missing values
    Returns the cleaned DataFrame.
    """
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    return df


def get_feature_types(df: pd.DataFrame) -> dict:
    """
    Return a dictionary with lists of numerical, categorical, and datetime columns.
    """
    return {
        "numerical": detect_numerical_features(df),
        "categorical": detect_categorical_features(df),
        "datetime": detect_datetime_features(df),
    }
