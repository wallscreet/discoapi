from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd


app = FastAPI(title="GovData API", version="0.1.0")


@app.get("/")
def root():
    return {"DiscoRover": "API"}