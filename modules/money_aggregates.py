from utils import fetch_fred_series
import pandas as pd


def _fetch_m2_supply(start_date:str=None, end_date:str=None):
    """
    M2 (M2SL) | default freq: 'M'
    """
    df = fetch_fred_series(category="money_aggregates", series_id="M2SL", start_date=start_date, end_date=end_date)
    df['M2 Supply'] = df['M2 Supply'] * 1000000000

    return df


def _fetch_m2_velocity(start_date:str=None, end_date:str=None):
    """
     Velocity of M2 Money Stock (M2V) | default freq: 'Q'
    """
    df = fetch_fred_series(category="money_aggregates", series_id="M2V", start_date=start_date, end_date=end_date)

    return df