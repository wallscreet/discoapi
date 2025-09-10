from utils import fetch_fred_series
import pandas as pd


def _fetch_median_family_income(start_date:str=None, end_date:str=None):
    """
    Median Annual Family Income in the United States (MEFAINUSA646N)
    """
    df = fetch_fred_series(category="wages_and_employment", series_id="MEFAINUSA646N", start_date=start_date, end_date=end_date)

    return df


def _fetch_real_disposable_personal_income(start_date:str=None, end_date:str=None):
    """
    Real Disposable Personal Income (DSPI) | path: /rdpi | default freq: 'M'
    """
    df = fetch_fred_series(category="income_and_spending", series_id="DSPI", start_date=start_date, end_date=end_date)
    df['RDPI'] = df['RDPI'] * 1000000000

    return df


def _fetch_unrate(start_date:str=None, end_date:str=None):
    """
    Unemployment Rate (UNRATE) | default freq: 'M'
    """
    df = fetch_fred_series(category="wages_and_employment", series_id="UNRATE", start_date=start_date, end_date=end_date)

    return df


def _fetch_unemployment_level(start_date:str=None, end_date:str=None):
    """
    Unemployment Level (UNEMPLOY)
    """
    df = fetch_fred_series(category="wages_and_employment", series_id="UNEMPLOY", start_date=start_date, end_date=end_date)
    df['Unemployed'] = df['Unemployed'] * 1000
    
    return df


def _fetch_job_openings(start_date:str=None, end_date:str=None):
    """
    Job Openings: Total Nonfarm (JTSJOL)
    """
    df = fetch_fred_series(category="wages_and_employment", series_id="JTSJOL", start_date=start_date, end_date=end_date)
    df['Job Openings'] = df['Job Openings'] * 1000
    
    return df