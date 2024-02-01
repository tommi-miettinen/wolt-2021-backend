from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    test_lat=24.935326
    test_lng=60.155631
    
    response = client.get(f"/restaurants/discovery?lat={test_lat}&lng={test_lng}")
    assert response.status_code == 200
    assert "sections" in response.json()