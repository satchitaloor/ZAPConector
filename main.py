from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

from zap_connector import ZAPConnector

load_dotenv()

APP_API_KEY = os.getenv("APP_API_KEY")
ZAP_BASE_URL = os.getenv("ZAP_BASE_URL")
ZAP_API_KEY = os.getenv("ZAP_API_KEY")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if not APP_API_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server API key not configured")
    if api_key != APP_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return api_key

app = FastAPI(title="ZAPConnector API")

connector = None


@app.on_event("startup")
def startup_event():
    global connector
    if not ZAP_BASE_URL:
        connector = None
        return
    connector = ZAPConnector(base_url=ZAP_BASE_URL, api_key=ZAP_API_KEY)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scan", dependencies=[Depends(verify_api_key)])
def start_scan(target: str):
    if connector is None:
        raise HTTPException(status_code=500, detail="ZAP connector not configured")
    scan_id = connector.start_scan(target)
    return {"scan_id": scan_id}


@app.get("/scan/{scan_id}/status", dependencies=[Depends(verify_api_key)])
def scan_status(scan_id: str):
    if connector is None:
        raise HTTPException(status_code=500, detail="ZAP connector not configured")
    status_val = connector.scan_status(scan_id)
    return {"status": status_val}


@app.get("/alerts", dependencies=[Depends(verify_api_key)])
def get_alerts(baseurl: str = None, start: int = 0, count: int = 50):
    if connector is None:
        raise HTTPException(status_code=500, detail="ZAP connector not configured")
    alerts = connector.get_alerts(baseurl=baseurl, start=start, count=count)
    return {"alerts": alerts}
