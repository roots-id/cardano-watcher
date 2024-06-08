from fastapi.testclient import TestClient
from main import app
from store import Store
from agent import Agent

app.state.store = Store()
app.state.agent = Agent(name='watcher', bran=None, store=app.state.store)
app.state.agent.initWallet()

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Watcher API active'}

def test_aids():
    response = client.get("/aids")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/aids", json={
        "alias":"aid1",
        "prefix":"EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9",
        "watched":True,
        "cardano":False,
        "oobi":"http://127.0.0.1:5642/oobi/EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9/witness/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'OOBI Not Found'}

    response = client.post("/aids", json={
        "alias":"aid1",
        "prefix":"EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9",
        "watched":True,
        "cardano":False
        })
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': {'alias': 'aid1', 'cardano': False, 'prefix': 'EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9', 'watched': True}, 'loc': ['body', 'oobi'], 'msg': 'Field required', 'type': 'missing'}]}

    response = client.delete("/aids/EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9")
    assert response.status_code == 404
    assert response.json() == {'detail': 'AID Not Found'}
    
def test_wits():
    response = client.get("/witnesses")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/witnesses", json=
        {
            "alias":"wan",
            "prefix":"BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha",
            "provider":"local",
            "oobi":"http://127.0.0.1:5642/oobi/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha/controller",
            "referral":"local"
        })
    assert response.status_code == 204
    assert response.content == b''

    response = client.get("/witnesses")
    assert response.status_code == 200
    assert response.json() == [
        {
            'alias': 'wan',
            'oobi': 'http://127.0.0.1:5642/oobi/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha/controller',
            'prefix': 'BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha',
            'provider': 'local',
            'referral': 'local',
        }]
    
    response = client.delete("/witnesses/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha")
    assert response.status_code == 204
    assert response.content == b''

    response = client.get("/witnesses")
    assert response.status_code == 200
    assert response.json() == []

    response = client.delete("/witnesses/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Witness Not Found'}

    response = client.post("/witnesses", json={
        "alias":"witness-dev02",
        "prefix":"BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd",
        "provider": "RootsID",
        "referral": "NA"
    })
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': {'alias': 'witness-dev02', 'prefix': 'BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd', 'provider': 'RootsID', 'referral': 'NA'}, 'loc': ['body', 'oobi'], 'msg': 'Field required', 'type': 'missing'}]}

    response = client.post("/witnesses", json={
        "alias":"wan",
        "prefix":"BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha",
        "provider":"local",
        "oobi":"http://127.0.0.2:5642/oobi/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha/controller",
        "referral":"local"
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'OOBI Not Found'}
