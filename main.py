from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd
import inspect
from dataclasses import dataclass, asdict


app = FastAPI(title="DiscoRover API", version="0.1.0")


modules = {

}


@app.get("/")
def root():
    if len(modules) > 0:
        categorized = {}
        for name, module in modules.items():
            categorized[name] = []
            for fn_name, fn in module.__dict__.items():
                if callable(fn) and fn_name.startswith("_fetch"):
                    categorized[name].append({
                        "name": fn_name.replace("_fetch_", ""),
                        "description": inspect.getdoc(fn) or ""
                    })
        return {"message": "DiscoRover API", "available_datasets": categorized}

    else:
        return {"message": "DiscoRover API", "available_datasets": "No datasets available"}