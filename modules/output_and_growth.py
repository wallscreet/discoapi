from utils import fetch_fred_series
import pandas as pd


def _fetch_gdp(start_date:str=None, end_date:str=None):
    """
    Gross Domestic Product (GDP) | default freq: 'Q'
    """
    df = fetch_fred_series(category="output_and_growth", series_id="GDP", start_date=start_date, end_date=end_date)
    df['GDP'] = df['GDP'] * 1000000000

    return df