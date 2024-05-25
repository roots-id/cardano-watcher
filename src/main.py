import datetime
import uvicorn
from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import FileResponse, Response, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from store import list_aids, store_aid, list_witnesses, store_witness

import os
import json

app = FastAPI()
SERVER_IP = "0.0.0.0"
SERVER_PORT = 8000
PUBLIC_URL = os.environ["PUBLIC_URL"] if "PUBLIC_URL" in os.environ  else "http://127.0.0.1:8000"

class AID(BaseModel):
    alias: str
    prefix: str
    oobi: str
    is_watched: bool = True

class Witness(BaseModel):
    alias: str
    prefix: str
    oobi: str
    provider: str

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/aids")
def get_aids():
    list_aids()
    return list_aids()

@app.post("/aids")
def add_aid(aid: AID):
    try:
        store_aid(aid.model_dump())
        return Response(status_code=200)
    except:
        return HTTPException(status_code=400, detail="Bad Request")

@app.get("/witnesses")
def get_aids():
    return list_witnesses()

@app.post("/witnesses")
def add_witness(wit: Witness):
    try:
        store_witness(wit.model_dump())
        return Response(status_code=200)
    except:
        return HTTPException(status_code=400, detail="Bad Request")

@app.get("/")
def index():
    # with open('web/index.html') as f:
    #     html_content = f.read()
    # return HTMLResponse(content=html_content, status_code=200)
    return {"message": "Watcher API active"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_IP, port=SERVER_PORT, reload=True)
