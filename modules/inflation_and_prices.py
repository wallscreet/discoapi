from utils import fetch_fred_series, scale_for_inflation
import pandas as pd


def _fetch_cpi(start_date:str=None, end_date:str=None):
    """
    """
    df = fetch_fred_series(category="inflation_and_prices", series_id="CPIAUCSL", start_date=start_date, end_date=end_date)

    return df


def _fetch_scaled_with_cpi(from_year:int=1980, to_year:int=2025, amount:float=100.0):
    cpi_df = _fetch_cpi()
    cpi_df['Date'] = pd.to_datetime(cpi_df['Date'])
    cpi_df.set_index('Date', inplace=True)
    # Resample annually (year-end) and take the mean
    cpi_df = cpi_df.resample('YE').mean()
    cpi_df['Year'] = cpi_df.index.year
    
    val = scale_for_inflation(cpi_df=cpi_df, from_year=from_year, to_year=to_year, amount=amount)

    return val


def _fetch_pce(start_date:str=None, end_date:str=None):
    """
    """
    df = fetch_fred_series(category="inflation_and_prices", series_id="PCE", start_date=start_date, end_date=end_date)

    return df