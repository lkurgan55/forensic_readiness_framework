import uvicorn, json, os
import pandas as pd
import boto3
from datetime import datetime


from pydantic import BaseModel
from pydantic.types import PositiveInt
from fastapi.responses import RedirectResponse
from fastapi import Depends, FastAPI, APIRouter, Request
from time import time
from datetime import datetime
from fastapi_utils.tasks import repeat_every

from src.functions import create_s3_bucket
from src.functions import configure_cloudtrail

import configparser

tools_route = APIRouter()

@tools_route.get("/analyze_log")
def get_steam_2fa_code(log_path: str):
    pass

@tools_route.get("/generate_report")
def get_steam_2fa_code(date: str):
    pass

    
app = FastAPI()
app.include_router(tools_route, prefix="/tools", tags=['tools'])

@app.get("/") # create auto-redirect to docs
def docs_page():
    return RedirectResponse("/docs")

@app.on_event('startup')
def startup():
    config = configparser.ConfigParser()
    config.read('config.ini')

    app.aws_config = config['AWS']
    app.aws_cloudtrail = config['CLOUDTRAIL']

    create_s3_bucket(app.aws_cloudtrail['bucket_name'], **app.aws_config)
    configure_cloudtrail(
        app.aws_cloudtrail['trail_name'],
        app.aws_cloudtrail['bucket_name'],
        **app.aws_config
    )

@app.on_event("startup")
@repeat_every(seconds= 6 * 60 * 60) 
def set_up():
    pass



@app.on_event('shutdown')
def shutdown():
    pass

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="info", reload=True) # start the server
    