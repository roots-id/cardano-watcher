from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Watcher API active'}

def test_get_aids():
    response = client.get("/aids")
    assert response.status_code == 200
    assert response.json() == {'message': 'Watcher API active'}