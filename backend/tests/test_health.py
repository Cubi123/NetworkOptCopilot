from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["environment"] == "development"  # Adjust if your environment is different
    
def test_database_health_check():
    response = client.get("/db-health")
    assert response.status_code == 200
    data = response.json()
    assert data["database"] == "ok"