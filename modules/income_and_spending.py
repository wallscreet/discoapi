from utils import fetch_fred_series
import pandas as pd


def _fetch_real_disposable_personal_income(start_date:str=None, end_date:str=None):
    """
    Real Disposable Personal Income (DSPI) | path: /rdpi | default freq: 'M'
    """
    df = fetch_fred_series(category="income_and_spending", series_id="DSPI", start_date=start_date, end_date=end_date)
    df['RDPI'] = df['RDPI'] * 1000000000

    return df


def _fetch_vehicle_ins_premiums(start_date:str=None, end_date:str=None):
    """
    Expenditures: Vehicle Insurance: All Consumer Units (CXU500110LB0101M) | path: /vehicle-insurance | default freq: M
    """
    df = fetch_fred_series(category="income_and_spending", series_id="CXU500110LB0101M", start_date=start_date, end_date=end_date)

    return df


def _fetch_pce_healthcare(start_date:str=None, end_date:str=None):
    """
    PCE Services: Healthcare (DHLCRC1Q027SBEA) | path: /pce-healthcare | default freq: M
    """
    df = fetch_fred_series(category="income_and_spending", series_id="DHLCRC1Q027SBEA", start_date=start_date, end_date=end_date)
    df['PCE Healthcare'] = df['PCE Healthcare'] * 1000000000

    return df


def _fetch_houshold_ops_spend(start_date:str=None, end_date:str=None):
    """
    Expenditures: Household Operations: All Consumer Units (CXUHHOPERLB0101M) | path: /hh-ops | default freq: M
    """
    df = fetch_fred_series(category="income_and_spending", series_id="CXUHHOPERLB0101M", start_date=start_date, end_date=end_date)

    return df