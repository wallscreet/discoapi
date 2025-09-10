from utils import fetch_fred_series
import pandas as pd
from http.client import HTTPException


def _fetch_us_households(start_date:str=None, end_date:str=None):
    """
    Total Households (TTLHH) | path: /households | freq default: A
    """
    df = fetch_fred_series(category="demographics", series_id="TTLHH", start_date=start_date, end_date=end_date)

    return df


def _fetch_us_population(start_date:str=None, end_date:str=None):
    """
    Population (POPTHM) | path: /population | freq default: M
    """
    df = fetch_fred_series(category="demographics", series_id="POPTHM", start_date=start_date, end_date=end_date)

    df['US Population'] = df['US Population'] * 1000

    return df


def _fetch_us_birthrate(start_date:str=None, end_date:str=None):
    """
    Crude Birth Rate for the United States (SPDYNCBRTINUSA). Births per 1000 people. | path: /us-birthrate | freq default: A
    """
    df = fetch_fred_series(category="demographics", series_id="SPDYNCBRTINUSA", start_date=start_date, end_date=end_date)

    return df


def _fetch_birth_death_data(start_year: int | None = None, end_year: int | None = None, race: str | None = None) -> pd.DataFrame:
    """
    Births and Deaths by Race/Ethnicity 2000-2023 (CDC) | path: /us-births-deaths-by-race | freq default: A
    """
    race_map = {
        "all": "All Races/Ethnicities",
        "white": "Non-Hispanic White",
        "black": "Non-Hispanic Black",
        "hispanic": "Hispanic",
    }

    df = pd.read_csv("data/static_datasets/us_births_deaths.csv")

    if start_year is not None:
        df = df[df["Year"] >= start_year]
    if end_year is not None:
        df = df[df["Year"] <= end_year]
    if race is not None:
        race_key = race.lower()
        if race_key not in race_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid race value '{race}'. Valid options: {list(race_map.keys())}"
            )
        df = df[df["RaceEthnicity"] == race_map[race_key]]

    df["Year"] = df["Year"].astype(int)

    return df