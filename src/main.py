import uvicorn
from fastapi import Request, FastAPI, HTTPException, status
from fastapi.responses import FileResponse, Response, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.delete("/aids/{prefix}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_aid(prefix: str, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if app.state.store.remove_aid(prefix):
        return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AID Not Found")

@app.post("/aids",status_code=status.HTTP_204_NO_CONTENT)
def add_aid(aid: AID, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if pre := app.state.agent.resolveOobi(alias=aid.alias,oobi=aid.oobi):
        aid.prefix = pre
        app.state.store.store_aid(aid.model_dump())
        return
    else:
        raise HTTPException(status_code=404, detail="OOBI Not Found")

@app.get("/witnesses")
def get_witnesses():
    return app.state.store.list_witnesses()

@app.delete("/witnesses/{prefix}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_witness(prefix: str, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if app.state.store.remove_witness(prefix):
        return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Witness Not Found")

@app.post("/witnesses", status_code=status.HTTP_204_NO_CONTENT)
def add_witness(wit: Witness, request: Request):
    if SIGNED_HEADERS_VERIFICATION and (not app.state.store.get_user(request.headers.get('Signify-Resource')) or not app.state.agent.verifyHeaders(request)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    print("Adding Witness")
    if pre := app.state.agent.resolveOobi(alias=wit.alias,oobi=wit.oobi):
        wit.prefix = pre
        print("Witness prefix", wit.prefix)
        app.state.store.store_witness(wit.model_dump())
        print("Witness stored")
        app.state.agent.createAidForWitness(witness_pre=pre)
        print("AID created for witness", pre)
        return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OOBI Not Found")
    
@app.get("/stats")
def get_stats():
    return app.state.store.generate_stats()

@app.get("/")
def index():
    return {"message": "Watcher API active"}

if __name__ == "__main__":
    
    uvicorn.run("main:app", host=SERVER_IP, port=SERVER_PORT, reload=True)
