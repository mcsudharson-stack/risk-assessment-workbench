from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_create_change_request():
    payload = {
        "request_id": "CR-1001",
        "name": "International Payment Feature",
        "description": "Enable retail customers to make international payments.",
        "change_type": "new_feature",
        "business_unit": "Consumer Banking",
        "geography": "United States",
        "customer_segment": "Retail Customers",
        "vendor_involved": True,
        "submitted_by": "product.owner",
    }

    response = client.post(
        "/api/change-requests/",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Change request received successfully"
    assert data["request"]["request_id"] == "CR-1001"