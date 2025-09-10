from utils import fetch_fred_series
import pandas as pd


def _fetch_median_home_prices(start_date:str=None, end_date:str=None):
    """
    Median Sales Price of Houses Sold for the United States (MSPUS) | path: /mspus | freq default: M
    """
    df = fetch_fred_series(category="housing", series_id="MSPUS", start_date=start_date, end_date=end_date)

    return df


def _fetch_median_home_price_new(start_date:str=None, end_date:str=None):
    """
    Median Sales Price for New Houses Sold in the United States (MSPNHSUS) | path: /mspnus | freq default:
    """
    df = fetch_fred_series(category="housing", series_id="MSPNHSUS", start_date=start_date, end_date=end_date)

    return df


def _fetch_caseshiller_home_price_index(start_date:str=None, end_date:str=None):
    """
    S&P CoreLogic Case-Shiller U.S. National Home Price Index (CSUSHPINSA) | path: /cshi | freq default:
    """
    df = fetch_fred_series(category="housing", series_id="CSUSHPINSA", start_date=start_date, end_date=end_date)

    return df


def _fetch_new_homes_ns(start_date:str=None, end_date:str=None):
    """
    New Houses for Sale by Stage of Construction, Not Started (NHFSEPNTS) | path: /new-homes-us | freq default:
    """
    df = fetch_fred_series(category="housing", series_id="NHFSEPNTS", start_date=start_date, end_date=end_date)
    df['New Homes NS'] = df['New Homes NS'] * 1000

    return df


def _fetch_new_homes_uc(start_date:str=None, end_date:str=None):
    """
    New Houses for Sale by Stage of Construction, Under Construction (NHFSEPUCS) | path: /new-homes-uc | freq default:
    """
    df = fetch_fred_series(category="housing", series_id="NHFSEPUCS", start_date=start_date, end_date=end_date)
    df['New Homes UC'] = df['New Homes UC'] * 1000

    return df


def _fetch_new_homes_comp(start_date:str=None, end_date:str=None):
    """
    New Houses for Sale by Stage of Construction, Completed (NHFSEPCS) | path: /new-homes-comp | freq default: M
    """
    df = fetch_fred_series(category="housing", series_id="NHFSEPCS", start_date=start_date, end_date=end_date)
    df['New Homes Comp'] = df['New Homes Comp'] * 1000

    return df


def _fetch_new_sf_homes_for_sale(start_date:str=None, end_date:str=None):
    """
    New One Family Houses for Sale in the United States (HNFSUSNSA) | path: /new-sf-homes-for-sale | freq defalt: M
    """
    df = fetch_fred_series(category="housing", series_id="HNFSUSNSA", start_date=start_date, end_date=end_date)
    df['New SF Homes'] = df['New SF Homes'] * 1000

    return df