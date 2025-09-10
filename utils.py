import pandas as pd
from functools import reduce
import numpy as np
import matplotlib as plt
import os
import json
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv()


def pull_fred_series(series_id: str, series_name: str):
    """
    Fetch a time series from FRED by its series ID and convert it to a pandas DataFrame.
    Returns DataFrame with Date as datetime64.
    """
    try:
        fred = Fred(api_key=os.getenv("FRED_API_KEY"))
        series = fred.get_series(series_id)
        df = series.to_frame().reset_index()
        df.columns = ["Date", series_name]
        # keep Date as datetime64 here
        return df
    except Exception as e:
        print(f"Error fetching series {series_id}: {e}")
        return None


def series_to_json(series_id, category, df):
    """
    Merge new data with existing JSON (if any) and save back to disk.
    JSON always stores Date as 'YYYY-MM-DD' strings.
    """
    folder = f"data/{category}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/fred_{series_id}.json"

    if os.path.exists(path):
        with open(path, "r") as f:
            existing_data = json.load(f)
        df_existing = pd.DataFrame(existing_data)
        df_existing["Date"] = pd.to_datetime(df_existing["Date"])
        df_combined = pd.concat([df_existing, df])
    else:
        df_combined = df

    df_combined = (
        df_combined.drop_duplicates(subset=["Date"])
        .sort_values("Date")
        .reset_index(drop=True)
    )

    # save date as string for JSON
    df_combined["Date"] = df_combined["Date"].dt.strftime("%Y-%m-%d")

    df_combined.to_json(path, orient="records")
    print(f"Updated data saved to {path}")

    return True


def fetch_fred_series(category, series_id, start_date=None, end_date=None):
    """
    Load series from local JSON and optionally filter by start_date/end_date.
    Returns DataFrame with Date as datetime64.
    """
    path = f"data/{category}/fred_{series_id}.json"
    df = pd.read_json(path)

    # convert date to datetime on load
    df["Date"] = pd.to_datetime(df["Date"])

    if start_date:
        df = df[df["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["Date"] <= pd.to_datetime(end_date)]

    return df


def load_registry(path: str):
    """
    Load the series registry from JSON.
    """
    with open(path, "r") as f:
        return json.load(f)


def refresh_from_registry(path="data/registry.json"):
    """
    Pull and refresh all series defined in the registry JSON.
    """
    registry = load_registry(path)
    for entry in registry:
        sid = entry["id"]
        name = entry["name"]
        category = entry["category"]
        df = pull_fred_series(sid, name)
        if df is not None:
            series_to_json(sid, category, df)


def scale_for_inflation(cpi_df: pd.DataFrame, from_year: int, to_year: int, amount: float):
    from_year_cpi = cpi_df.loc[cpi_df['Year'] == from_year, 'CPI'].values[0]
    to_year_cpi = cpi_df.loc[cpi_df['Year'] == to_year, 'CPI'].values[0]
    adjusted_value = (amount * (to_year_cpi / from_year_cpi))
    
    return round(adjusted_value, 2)


def merge_on_date(dfs, how='inner'):
    cleaned = []
    for i, df in enumerate(dfs):
        if 'Date' not in df.columns:
            raise ValueError(f"DataFrame at index {i} is missing 'Date' column.")

        # Drop Year/Month/Day if present
        drop_cols = [c for c in ['Year', 'Month', 'Day'] if c in df.columns]
        df = df.drop(columns=drop_cols)

        cleaned.append(df)

    merged_df = reduce(lambda left, right: pd.merge(left, right, on='Date', how=how), cleaned)
    return merged_df


def merge_on_year(dfs, how='inner'):
    """
    Merge a list of dataframes on the 'Year' column.
    """
    # Safety check: make sure they all have 'Year' column
    for i, df in enumerate(dfs):
        if 'Year' not in df.columns:
            raise ValueError(f"DataFrame at index {i} is missing 'Year' column.")

    merged_df = reduce(lambda left, right: pd.merge(left, right, on='Year', how=how), dfs)
    
    return merged_df


def calc_mtg_pi_payment(principal, annual_rate, years=30):
    """
    Calculate monthly principal & interest payment for a mortgage.
    """
    monthly_rate = (annual_rate / 100) / 12
    n_payments = years * 12
    
    if monthly_rate == 0:
        return principal / n_payments
    
    payment = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / \
              ((1 + monthly_rate) ** n_payments - 1)
    
    return payment


def sanitize_for_json(df: pd.DataFrame) -> list[dict]:
    """Convert a DataFrame into JSON-safe records."""
    safe_df = df.replace({np.nan: None})
    return safe_df.to_dict(orient="records")


def add_real_prices(df):
    latest_cpi = df['CPI'].iloc[-1]
    commodity_cols = [col for col in df.columns if col not in ["Date", "CPI"]]

    # scale each nominal price into real 2025 dollars
    for col in commodity_cols:
        df[f"{col} (Real)"] = round((df[col] * (latest_cpi / df["CPI"])),2)
    
    return df
