from utils import fetch_fred_series, add_real_prices
import pandas as pd
import os
import json
from functools import reduce


def _add_real_prices(df):
    """
    """
    cpi_df = fetch_fred_series(category="inflation_and_prices", series_id="CPIAUCSL")
    merged = pd.merge(df, cpi_df, on="Date", how="left")
    df = add_real_prices(merged)
    df = df.drop(columns=["CPI"], axis=1)

    return df

def _fetch_egg_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Eggs, Grade A, Large (Cost per Dozen) in U.S. City Average (APU0000708111) | path: /egg-prices | freq default: M
    """
    eggs_df = fetch_fred_series(category="commodities", series_id="APU0000708111", start_date=start_date, end_date=end_date)
    df = _add_real_prices(eggs_df)

    return df


def _fetch_milk_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Milk, Fresh, Whole, Fortified (Cost per Gallon/3.8 Liters) in U.S. City Average (APU0000709112) | path: /milk-prices | freq default: M
    """
    milk_df = fetch_fred_series(category="commodities", series_id="APU0000709112", start_date=start_date, end_date=end_date)
    df = _add_real_prices(milk_df)

    return df


def _fetch_ground_beef_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Ground Beef, 100% Beef (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000703112) | path: /ground-beef-prices | freq default: M
    """
    ground_beef_df = fetch_fred_series(category="commodities", series_id="APU0000703112", start_date=start_date, end_date=end_date)
    df = _add_real_prices(ground_beef_df)

    return df


def _fetch_bread_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Bread, White, Pan (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000702111) | path: /bread-prices | freq default: M
    """
    bread_df = fetch_fred_series(category="commodities", series_id="APU0000702111", start_date=start_date, end_date=end_date)
    df = _add_real_prices(bread_df)

    return df


def _fetch_chicken_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Chicken Breast, Boneless (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000FF1101) | path: /chicken-prices | freq default: M
    """
    chicken_df = fetch_fred_series(category="commodities", series_id="APU0000FF1101", start_date=start_date, end_date=end_date)
    df = _add_real_prices(chicken_df)

    return df


def _fetch_gas_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Gasoline, Unleaded Regular (Cost per Gallon/3.785 Liters) in U.S. City Average (APU000074714) | path: /gas-prices | freq default: M
    """
    gas_df = fetch_fred_series(category="commodities", series_id="APU000074714", start_date=start_date, end_date=end_date)
    df = _add_real_prices(gas_df)

    return df


def _fetch_electric_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Electricity per Kilowatt-Hour in U.S. City Average (APU000072610) | path: /electric-kwh-prices | freq default: M
    """
    electric_df = fetch_fred_series(category="commodities", series_id="APU000072610", start_date=start_date, end_date=end_date)
    df = _add_real_prices(electric_df)

    return df


def _fetch_coffee_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Coffee, 100%, Ground Roast, All Sizes (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000717311) | path: /coffee-prices | freq default: M
    """
    coffee_df = fetch_fred_series(category="commodities", series_id="APU0000717311", start_date=start_date, end_date=end_date)
    df = _add_real_prices(coffee_df)

    return df


def _fetch_bacon_sliced_prices(start_date:str=None, end_date:str=None):
    """
    Average Price: Bacon, Sliced (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000704111) | path: /bacon-prices | freq default: M
    """
    bacon_df = fetch_fred_series(category="commodities", series_id="APU0000704111", start_date=start_date, end_date=end_date)
    df = _add_real_prices(bacon_df)

    return df


_COMMODITY_REGISTRY = {
        "bacon": _fetch_bacon_sliced_prices,
        "eggs": _fetch_egg_prices,
        "milk": _fetch_milk_prices,
        "bread": _fetch_bread_prices,
        "ground_beef": _fetch_ground_beef_prices,
        "coffee": _fetch_coffee_prices,
        "gas": _fetch_gas_prices,
        "electricity": _fetch_electric_prices,
        "chicken": _fetch_chicken_prices,
    }


def _fetch_all_commodity_prices(start_date:str=None, end_date:str=None):
    """
    Aggregated Dataset with all commodities | path: /all-commodity-prices | freq default: M
    """
    dfs = []
    for name, fetcher in _COMMODITY_REGISTRY.items():
        df = fetcher(start_date=start_date, end_date=end_date)
        if df is not None:
            dfs.append(df)

    if not dfs:
        return pd.DataFrame()  # empty fallback

    merged_df = reduce(
        lambda left, right: pd.merge(left, right, on="Date", how="outer"), dfs
    )

    return merged_df