from utils import fetch_fred_series, merge_on_date, scale_for_inflation
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


def _fetch_used_car_prices(start_date:str=None, end_date:str=None):
    """
    CPI Used Cars and Trucks (CUSR0000SETA02). Prices calculated based on CPI index applied to reference year and price
    """
    ref_auto_cpi = 185.660
    ref_price = 28472

    # Used Auto CPI df
    used_auto_df = fetch_fred_series(category="inflation_and_prices", series_id="CUSR0000SETA02", start_date=start_date, end_date=end_date)

    # CPI
    _cpi_df = _fetch_cpi(start_date=start_date, end_date=end_date)

    used_merged = used_auto_df.merge(_cpi_df, 'inner', 'Date')

    used_merged['Used Auto Price Real'] = round(used_merged['Used Auto CPI'] * (ref_price / ref_auto_cpi),2)
    ref_cpi = used_merged['CPI'].iloc[-1]
    used_merged['Used Auto Price Nominal'] = round(used_merged['Used Auto Price Real'] * (used_merged['CPI'] / ref_cpi), 2)

    if start_date is not None:
        used_merged = used_merged[used_merged['Date'] >= start_date]
    if end_date is not None:
        used_merged = used_merged[used_merged['Date'] <= end_date]

    drop_cols = ['CPI']
    used_merged.drop(columns=drop_cols, inplace=True)

    return used_merged


def _fetch_new_car_prices(start_date:str=None, end_date:str=None):
    """
    CPI New Cars and Trucks (CUUR0000SETA01). Prices calculated based on CPI index applied to reference year and price
    """
    ref_auto_cpi = 178.001
    ref_price = 48397

    # New Auto CPI
    new_auto_df = fetch_fred_series(category="inflation_and_prices", series_id="CUUR0000SETA01", start_date=start_date, end_date=end_date)

    # CPI
    _cpi_df = _fetch_cpi(start_date=start_date, end_date=end_date)

    new_merged = new_auto_df.merge(_cpi_df, 'inner', 'Date')
    new_merged['New Auto Price Real'] = round(new_merged['New Auto CPI'] * (ref_price / ref_auto_cpi),2)
    ref_cpi = new_merged['CPI'].iloc[-1]
    new_merged['New Auto Price Nominal'] = round(new_merged['New Auto Price Real'] * (new_merged['CPI'] / ref_cpi), 2)

    if start_date is not None:
        new_merged = new_merged[new_merged['Date'] >= start_date]
    if end_date is not None:
        new_merged = new_merged[new_merged['Date'] <= end_date]

    drop_cols = ['CPI']
    
    return new_merged.drop(columns=drop_cols)


def _fetch_all_car_prices(start_date:str=None, end_date:str=None):
    """
    Merged dataset with New Car CPI (CUUR0000SETA01) and Used Car CPI (CUSR0000SETA02). Prices calculated based on CPI indices for New and Used autos applied to reference years and prices
    """
    used_df = _fetch_used_car_prices(start_date=start_date, end_date=end_date)
    new_df = _fetch_new_car_prices(start_date=start_date, end_date=end_date)

    df = merge_on_date([new_df, used_df])
    
    return df