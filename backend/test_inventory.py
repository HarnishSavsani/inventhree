"""
Unit and integration test suite for the FastAPI inventory microservice.
Tests valid operations, SKU edge cases, negative counts, stock limits,
concurrency, and simulated upstream error conditions (500/429/latency).
"""

import asyncio
import os
import pytest
from httpx import ASGITransport, AsyncClient

# Ensure test DB is isolated or reset for testing
import database
from main import app


@pytest.fixture(autouse=True)
async def setup_test_database(tmp_path):
    """Point database to a temporary SQLite file for test isolation."""
    test_db_file = str(tmp_path / "test_inventory.db")
    database.DB_PATH = test_db_file
    await database.init_db()
    yield
    if os.path.exists(test_db_file):
        try:
            os.remove(test_db_file)
        except OSError:
            pass


@pytest.mark.anyio
async def test_health_check():
    """Verify health endpoint reports online status and DB connection."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert data["catalog_item_count"] > 0


@pytest.mark.anyio
async def test_get_all_inventory():
    """Verify inventory catalog listing returns expected fields and available stock."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/inventory")
        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)
        assert len(items) >= 7

        first_item = items[0]
        assert "sku" in first_item
        assert "current_stock" in first_item
        assert "reserved_stock" in first_item
        assert "available_stock" in first_item
        assert first_item["available_stock"] == first_item["current_stock"] - first_item["reserved_stock"]


@pytest.mark.anyio
async def test_get_single_inventory_item_success():
    """Verify retrieval of a single item by SKU."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/inventory/PROD-1001-BLK")
        assert response.status_code == 200
        data = response.json()
        assert data["sku"] == "PROD-1001-BLK"
        assert data["current_stock"] == 50


@pytest.mark.anyio
async def test_get_single_inventory_item_not_found():
    """Verify 404 returned for nonexistent SKU."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/inventory/NON-EXISTENT-SKU")
        assert response.status_code == 404
        data = response.json()
        assert data["error_code"] == "ITEM_NOT_FOUND"


@pytest.mark.anyio
async def test_successful_stock_deduction():
    """Verify legitimate order stock deduction decrements warehouse stock."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "sku": "PROD-1001-BLK",
            "quantity": 5,
            "operation": "deduct",
            "reason": "Order fulfillment #ORD-101",
            "reference_id": "ORD-101"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["sku"] == "PROD-1001-BLK"
        assert data["previous_stock"] == 50
        assert data["new_stock"] == 45
        assert data["quantity_modified"] == 5

        # Verify persisted state via GET
        get_res = await client.get("/api/v1/inventory/PROD-1001-BLK")
        assert get_res.json()["current_stock"] == 45


@pytest.mark.anyio
async def test_successful_restock():
    """Verify inbound inventory restock increases stock."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "sku": "PROD-2005-RGB",
            "quantity": 20,
            "operation": "restock",
            "reason": "Batch restock shipment",
            "reference_id": "RESTOCK-99"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["new_stock"] == 15 + 20  # original 15 + 20 = 35


@pytest.mark.anyio
async def test_edge_case_negative_quantity_rejected():
    """Edge case: Negative quantity in payload must be rejected with 422."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "sku": "PROD-1001-BLK",
            "quantity": -10,
            "operation": "deduct"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "PAYLOAD_VALIDATION_ERROR"
        assert any("Negative stock count values are forbidden" in str(d) for d in data["details"])


@pytest.mark.anyio
async def test_edge_case_zero_quantity_rejected():
    """Edge case: Zero quantity deduction must be rejected with 422."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "sku": "PROD-1001-BLK",
            "quantity": 0,
            "operation": "deduct"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert data["error_code"] == "PAYLOAD_VALIDATION_ERROR"


@pytest.mark.anyio
async def test_edge_case_malformed_sku_lowercase():
    """Edge case: Lowercase SKU must be rejected by custom Pydantic validator."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "sku": "prod-1001-blk",
            "quantity": 1,
            "operation": "deduct"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert data["error_code"] == "PAYLOAD_VALIDATION_ERROR"
        assert any("Malformed SKU" in str(d) for d in data["details"])


@pytest.mark.anyio
async def test_edge_case_malformed_sku_special_characters():
    """Edge case: SKU with special characters must fail validation."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "sku": "PROD#$$123*!!",
            "quantity": 2,
            "operation": "deduct"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert data["error_code"] == "PAYLOAD_VALIDATION_ERROR"


@pytest.mark.anyio
async def test_edge_case_insufficient_stock_exceeded():
    """Edge case: Deducting more stock than available triggers 422 InsufficientStockException."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # PROD-4099-PRO has 8 in stock
        payload = {
            "sku": "PROD-4099-PRO",
            "quantity": 25,
            "operation": "deduct"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "INSUFFICIENT_STOCK"
        assert "Insufficient stock" in data["message"]


@pytest.mark.anyio
async def test_edge_case_update_nonexistent_sku():
    """Edge case: Updating a formatted SKU that does not exist in DB raises 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "sku": "PROD-9999-NOTFOUND",
            "quantity": 1,
            "operation": "deduct"
        }
        response = await client.post("/api/v1/inventory/update", json=payload)
        assert response.status_code == 404
        data = response.json()
        assert data["error_code"] == "ITEM_NOT_FOUND"


@pytest.mark.anyio
async def test_upstream_simulation_rate_limit_429():
    """Simulate upstream 429 Rate Limit error condition."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/api/v1/inventory/simulate-upstream?scenario=rate_limit")
        assert response.status_code == 429
        data = response.json()
        assert data["error_code"] == "RATE_LIMIT_EXCEEDED"
        assert response.headers.get("retry-after") == "45"


@pytest.mark.anyio
async def test_upstream_simulation_server_error_500():
    """Simulate upstream 500 ERP server failure condition."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/api/v1/inventory/simulate-upstream?scenario=server_error")
        assert response.status_code == 500
        data = response.json()
        assert data["error_code"] == "UPSTREAM_SERVICE_FAILURE"


@pytest.mark.anyio
async def test_latency_delay_simulation_header():
    """Simulate network latency using x-simulate-delay-ms header."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        headers = {"x-simulate-delay-ms": "250"}
        response = await client.get("/api/v1/inventory", headers=headers)
        assert response.status_code == 200
        assert "X-Process-Time-Ms" in response.headers
        duration = float(response.headers["X-Process-Time-Ms"])
        assert duration >= 240  # delay at least ~250ms
