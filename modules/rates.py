from utils import fetch_fred_series
import pandas as pd


def _fetch_30yr_mortgage_rates(start_date:str=None, end_date:str=None):
    """
    30-Year Fixed Rate Mortgage Average in the United States (MORTGAGE30US)
    """
    df = fetch_fred_series(category="rates", series_id="MORTGAGE30US", start_date=start_date, end_date=end_date)

    return df


def _fetch_15yr_mortgage_rates(start_date:str=None, end_date:str=None):
    """
    15-Year Fixed Rate Mortgage Average in the United States (MORTGAGE15US)
    """
    df = fetch_fred_series(category="rates", series_id="MORTGAGE15US", start_date=start_date, end_date=end_date)

    return df


def _fetch_all_mortgage_rates(start_date=None, end_date=None, freq:str=None):
    """
    Fetch both 30-year and 15-year mortgage rates and merge them into a single DataFrame.
    """
    df_30yr = _fetch_30yr_mortgage_rates(start_date, end_date)
    df_15yr = _fetch_15yr_mortgage_rates(start_date, end_date)
    
    df_merged = df_30yr.merge(df_15yr, on='Date', how='outer')
    
    df_merged = df_merged.sort_values(by='Date').reset_index(drop=True)
    
    return df_merged


def _fetch_sofr(start_date:str=None, end_date:str=None):
    """
    Secured Overnight Financing Rate (SOFR)
    """
    df = fetch_fred_series(category="rates", series_id="SOFR", start_date=start_date, end_date=end_date)

    return df


def _fetch_fed_funds_rate(start_date:str=None, end_date:str=None):
    """
    Federal Funds Effective Rate (FEDFUNDS)
    """
    df = fetch_fred_series(category="rates", series_id="FEDFUNDS", start_date=start_date, end_date=end_date)

    return df