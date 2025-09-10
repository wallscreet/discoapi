from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd
from utils import sanitize_for_json
import modules.inflation_and_prices as inflation_and_prices
import modules.demographics as demographics
import modules.commodities as commodities
import modules.rates as rates
import modules.housing as housing


app = FastAPI(title="DiscoRover API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "DiscoRover API", "available_datasets": "No datasets available"}


@app.get("/cpi")
def get_cpi(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
):
    """Consumer Price Index for All Urban Consumers (CPIAUCSL)."""
    try: 
        df:pd.DataFrame = inflation_and_prices._fetch_cpi(start_date=start_date, end_date=end_date)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scale-for-inflation")
def scale_for_inflation_route(
    from_year: int = Query(1980, description="Year to scale from"),
    to_year: int = Query(2025, description="Year to scale to"),
    amount: float = Query(100.0, description="Amount to scale")
):
    """
    Scale a monetary amount from `from_year` to `to_year` using CPI data.
    """
    scaled_value = inflation_and_prices._fetch_scaled_with_cpi(from_year=from_year, to_year=to_year, amount=amount)
    return {"from_year": from_year, "to_year": to_year, "original_amount": amount, "scaled_amount": scaled_value}


@app.get("/pce")
def get_pce(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)")
):
    """Consumer Price Index for All Urban Consumers (CPIAUCSL)."""
    try: 
        df:pd.DataFrame = inflation_and_prices._fetch_pce(start_date=start_date, end_date=end_date) 

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/households")
def get_households(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)")
):
    """Total Households (TTLHH)"""
    try: 
        df:pd.DataFrame = demographics._fetch_us_households(start_date=start_date, end_date=end_date)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/population")
def get_population(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)")
):
    """Total Households (TTLHH)"""
    try: 
        df:pd.DataFrame = demographics._fetch_us_population(start_date=start_date, end_date=end_date)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/us-birthrate")
def get_us_birthrate(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
):
    """Crude Birth Rate for the United States (SPDYNCBRTINUSA)"""
    try: 
        df:pd.DataFrame = demographics._fetch_us_birthrate(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/us-births-deaths-by-race")
def get_birth_death_data(
    start_year: int | None = Query(None, description="Filter start year (e.g. 2000)"),
    end_year: int | None = Query(None, description="Filter end year (e.g. 2023)"),
    race: str | None = Query(None, description="Race/Ethnicity filter ('All', 'White', 'Black', 'Hispanic')")
):
    """Births and Deaths by Race/Ethnicity (CDC)"""
    try:
        df: pd.DataFrame = demographics._fetch_birth_death_data(start_year=start_year, end_year=end_year, race=race)
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/egg-prices")
def get_egg_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
):
    """Average Price: Eggs, Grade A, Large (Cost per Dozen) in U.S. City Average (APU0000708111)"""
    try: 
        df:pd.DataFrame = commodities._fetch_egg_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/milk-prices")
def get_milk_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Milk, Fresh, Whole, Fortified (Cost per Gallon/3.8 Liters) in U.S. City Average (APU0000709112)"""
    try: 
        df:pd.DataFrame = commodities._fetch_milk_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ground-beef-prices")
def get_ground_beef_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Ground Beef, 100% Beef (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000703112)"""
    try: 
        df:pd.DataFrame = commodities._fetch_ground_beef_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bread-prices")
def get_bread_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Bread, White, Pan (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000702111)"""
    try: 
        df:pd.DataFrame = commodities._fetch_bread_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chicken-prices")
def get_chicken_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Chicken Breast, Boneless (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000FF1101)"""
    try: 
        df:pd.DataFrame = commodities._fetch_chicken_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/gas-prices")
def get_gas_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Gasoline, Unleaded Regular (Cost per Gallon/3.785 Liters) in U.S. City Average (APU000074714)"""
    try: 
        df:pd.DataFrame = commodities._fetch_gas_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/electric-kwh-prices")
def get_electric_kwh_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Electricity per Kilowatt-Hour in U.S. City Average (APU000072610)"""
    try: 
        df:pd.DataFrame = commodities._fetch_electric_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/coffee-prices")
def get_coffee_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Coffee, 100%, Ground Roast, All Sizes (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000717311)"""
    try: 
        df:pd.DataFrame = commodities._fetch_coffee_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/bacon-prices")
def get_bacon_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Average Price: Bacon, Sliced (Cost per Pound/453.6 Grams) in U.S. City Average (APU0000704111)"""
    try: 
        df:pd.DataFrame = commodities._fetch_bacon_sliced_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/all-commodity-prices")
def get_all_commodity_prices(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Aggregated Dataset with Average Price:  All Commodities available in API"""
    try: 
        df:pd.DataFrame = commodities._fetch_all_commodity_prices(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mortgage-30yr")
def get_30yr_mortgage_rates(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('A', description="Frequency period")
):
    """
    30-Year Fixed Rate Mortgage Average in the United States (MORTGAGE30US)
    """
    try: 
        df:pd.DataFrame = rates._fetch_30yr_mortgage_rates(start_date=start_date, end_date=end_date)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mortgage-15yr")
def get_15yr_mortgage_rates(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('A', description="Frequency period")
):
    """
    15-Year Fixed Rate Mortgage Average in the United States (MORTGAGE15US)
    """
    try: 
        df:pd.DataFrame = rates._fetch_15yr_mortgage_rates(start_date=start_date, end_date=end_date)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mortgage-all")
def get_all_mortgage_rates(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('A', description="Frequency period")
):
    """
    Fetch both 30-year and 15-year mortgage rates and merge them into a single DataFrame.
    """
    try: 
        df:pd.DataFrame = rates._fetch_all_mortgage_rates(start_date=start_date, end_date=end_date, freq=freq)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sofr")
def get_sofr(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query(None, description="Frequency Period")
):
    """Secured Overnight Financing Rate (SOFR)"""
    try: 
        df:pd.DataFrame = rates._fetch_sofr(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fed-funds")
def get_fed_funds_rate(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """Federal Funds Effective Rate (FEDFUNDS)"""
    try: 
        df:pd.DataFrame = rates._fetch_fed_funds_rate(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/mspus")
def get_mspus(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)")
):
    """
    Median Sales Price of Houses Sold for the United States (MSPUS)
    """
    try: 
        df:pd.DataFrame = housing._fetch_median_home_prices(start_date=start_date, end_date=end_date)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mspnus")
def get_msp_new_homes(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)")
):
    """
    Median Sales Price for New Houses Sold in the United States (MSPNHSUS)
    """
    try: 
        df:pd.DataFrame = housing._fetch_median_home_price_new(start_date=start_date, end_date=end_date)

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cshi")
def get_caseshiller_homes_index(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
):
    """S&P CoreLogic Case-Shiller U.S. National Home Price Index (CSUSHPINSA)"""
    try: 
        df:pd.DataFrame = housing._fetch_caseshiller_home_price_index(start_date=start_date, end_date=end_date) 

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/new-homes-ns")
def get_new_homes_ns(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """New Houses for Sale by Stage of Construction, Not Started (NHFSEPNTS)"""
    try: 
        df:pd.DataFrame = housing._fetch_new_homes_ns(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/new-homes-uc")
def get_new_homes_uc(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """New Houses for Sale (Units) by Stage of Construction, Under Construction (NHFSEPUCS)"""
    try: 
        df:pd.DataFrame = housing._fetch_new_homes_uc(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/new-homes-comp")
def get_new_homes_comp(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """New Houses for Sale (Units) by Stage of Construction, Under Construction (NHFSEPUCS)"""
    try: 
        df:pd.DataFrame = housing._fetch_new_homes_comp(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/new-sf-homes-for-sale")
def get_new_sf_homes_for_sale(
    start_date: str | None = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter end date (YYYY-MM-DD)"),
    freq:str = Query('M', description="Frequency period")
):
    """New One Family Houses for Sale in the United States (HNFSUSNSA)"""
    try: 
        df:pd.DataFrame = housing._fetch_new_sf_homes_for_sale(start_date=start_date, end_date=end_date)   

        return JSONResponse(content=sanitize_for_json(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))