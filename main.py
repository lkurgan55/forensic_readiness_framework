import uvicorn, json, os
import pandas as pd
from datetime import datetime


from pydantic import BaseModel
from pydantic.types import PositiveInt
from fastapi.responses import RedirectResponse
from fastapi import Depends, FastAPI, APIRouter, Request
from time import time
from fastapi_utils.tasks import repeat_every

import configparser




class AccountAdd(BaseModel):
    username: str
    email: str
    phone: str
    password: str


tools_route = APIRouter()

@tools_route.get("/get_steam_2fa_code") # tools for work with accounts
def get_steam_2fa_code(UserName: str):
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

@app.on_event("startup")
@repeat_every(seconds= 6 * 60 * 60) 
def update_queue():
    pass


@app.on_event('shutdown')
def shutdown():
    pass

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="info", reload=True) # start the server
    