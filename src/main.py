import uvicorn
from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import FileResponse, Response, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from store import list_aids, store_aid, list_witnesses, store_witness, remove_aid, remove_witness, generate_stats, get_user, get_users, get_aid
from store import Store
from agent import Agent
from contextlib import asynccontextmanager
from poller import Poller
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.store = Store()
    app.state.agent = Agent(name='watcher', bran=WATCHER_BRAN, store=app.state.store)
    app.state.agent.initWallet()
    Poller(agent=app.state.agent, store = app.state.store).start()
    for user in app.state.store.get_users():
        if app.state.store.get_aid(user['prefix']) is None:
            if pre := app.state.agent.resolveOobi(alias = user["name"], oobi=user["oobi"]):
                aid = AID(alias=user["name"], 
                          prefix=pre, 
                          oobi=user["oobi"], 
                          watched=True, 
                          cardano=False)
                aid.prefix = pre
                app.state.store.store_aid(aid.model_dump())
            
    yield

app = FastAPI(lifespan=lifespan)
SERVER_IP = "0.0.0.0"
SERVER_PORT = 8000
WATCHER_BRAN = os.environ["WATCHER_BRAN"] if "WATCHER_BRAN" in os.environ else None
SIGNED_HEADERS_VERIFICATION = os.environ["SIGNED_HEADERS_VERIFICATION"] if "SIGNED_HEADERS_VERIFICATION" in os.environ else False

class AID(BaseModel):
    alias: str
    prefix: str
    oobi: str
    watched: bool = True
    cardano: bool = False

class Witness(BaseModel):
    alias: str
    prefix: str
    oobi: str
    provider: str
    referral: str

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
    return app.state.store.list_aids()

@app.get("/aids/{prefix}")
async def get_kel(prefix: str):
    return app.state.agent.watchAID(prefix=prefix)

@app.delete("/aids/{prefix}")
async def delete_aid(prefix: str, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        return HTTPException(status_code=401, detail="Unauthorized")
    if app.state.store.remove_aid(prefix):
        return Response(status_code=200)
    else:
        return HTTPException(status_code=404, detail="AID Not Found")

@app.post("/aids")
def add_aid(aid: AID, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        return HTTPException(status_code=401, detail="Unauthorized")
    try:
        if pre := app.state.agent.resolveOobi(alias=aid.alias,oobi=aid.oobi):
            aid.prefix = pre
            app.state.store.store_aid(aid.model_dump())
            return Response(status_code=200)
        else:
            return HTTPException(status_code=404, detail="OOBI Not Found")
    except Exception as e:
        print("Error: ", e)
        return HTTPException(status_code=400, detail="Bad Request")

@app.get("/witnesses")
def get_witnesses():
    return app.state.store.list_witnesses()

@app.delete("/witnesses/{prefix}")
async def delete_witness(prefix: str, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        return HTTPException(status_code=401, detail="Unauthorized")
    if app.state.store.remove_witness(prefix):
        return Response(status_code=200)
    else:
        return HTTPException(status_code=404, detail="Witness Not Found")

@app.post("/witnesses")
def add_witness(wit: Witness, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        return HTTPException(status_code=401, detail="Unauthorized")
    try:
        if pre := app.state.agent.resolveOobi(alias=wit.alias,oobi=wit.oobi):
            wit.prefix = pre
            app.state.store.store_witness(wit.model_dump())
            app.state.agent.createAidForWitness(witness_pre=pre)
            return Response(status_code=200)
        else:
            return HTTPException(status_code=404, detail="OOBI Not Found")
    except Exception as e:
        print("Error: ", e)
        return HTTPException(status_code=400, detail="Bad Request")
    
@app.get("/stats")
def get_stats():
    return app.state.store.generate_stats()

@app.get("/")
def index():
    return {"message": "Watcher API active"}

if __name__ == "__main__":
    
    uvicorn.run("main:app", host=SERVER_IP, port=SERVER_PORT, reload=True)
