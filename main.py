import uvicorn, json, os
import pandas as pd
import boto3
from datetime import datetime


from time import time
from datetime import datetime
from fastapi_utils.tasks import repeat_every

from src.functions import create_s3_bucket
from src.functions import configure_cloudtrail
from src.functions import create_directory
from src.functions import download_logs

import configparser

tools_route = APIRouter()

@tools_route.get("/analyze_log")
def analyze_log(log_path: str):
    pass

@tools_route.get("/generate_report")
def generate_report(date: str):
    pass

@tools_route.post("/register_log")
def register_log(log: str):
    pass

    
app = FastAPI()
app.include_router(tools_route, prefix="/tools", tags=['tools'])

@app.get("/")
def docs_page():
    return RedirectResponse("/docs")

@app.on_event('startup')
def startup():
    config = configparser.ConfigParser()
    config.read('config.ini')

    app.aws_config = config['AWS']
    app.aws_cloudtrail = config['CLOUDTRAIL']

    create_directory('aws_logs')
    create_s3_bucket(app.aws_cloudtrail['bucket_name'], **app.aws_config)
    download_logs(app.aws_cloudtrail['bucket_name'], 'aws_logs',  '', **app.aws_config)
    return
    configure_cloudtrail(
        app.aws_cloudtrail['trail_name'],
        app.aws_cloudtrail['bucket_name'],
        **app.aws_config
    )

@app.on_event("startup")
@repeat_every(seconds = app.aws_cloudtrail['period_get_logs']) 
def checks_aws_logs():
    pass



@app.on_event('shutdown')
def shutdown():
    pass

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="info", reload=True) # start the server
    