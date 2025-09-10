from utils import fetch_fred_series
import pandas as pd


def _fetch_dq_credit_cards(start_date:str=None, end_date:str=None):
    """
    Delinquency Rate on Credit Card Loans, All Commercial Banks (DRCCLACBS) | path: /dq-credit-cards | freq default: Q | freq available: M | range: 1991-current
    """
    df = fetch_fred_series(category="delinquency", series_id="DRCCLACBS", start_date=start_date, end_date=end_date)

    return df


def _fetch_dq_consumer_loans(start_date:str=None, end_date:str=None):
    """
    Delinquency Rate on Consumer Loans, All Commercial Banks (DRCLACBS) | path: /dq-consumer-loans | freq default: Q | freq available: M | range: 1987-current
    """
    df = fetch_fred_series(category="delinquency", series_id="DRCLACBS", start_date=start_date, end_date=end_date)

    return df


def _fetch_dq_sfr_mortgages(start_date:str=None, end_date:str=None):
    """
    Delinquency Rate on Single-Family Residential Mortgages, Booked in Domestic Offices, All Commercial Banks (DRSFRMACBS) | path: /dq-sfr-mtg | freq default: Q | freq available: M | range: 1991-current
    """
    df = fetch_fred_series(category="delinquency", series_id="DRSFRMACBS", start_date=start_date, end_date=end_date)

    return df


def _fetch_dq_all_loans(start_date:str=None, end_date:str=None):
    """
    Delinquency Rate on All Loans, All Commercial Banks (DRALACBS) | path: /dq-all-loans | freq default: Q | range: 1985-current
    """
    df = fetch_fred_series(category="delinquency", series_id="DRALACBS", start_date=start_date, end_date=end_date)

    return df