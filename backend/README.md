# 📦 Asynchronous FastAPI E-Commerce Inventory Microservice

A production-grade, asynchronous FastAPI microservice engineered for high-concurrency e-commerce stock management, edge-case data validation, resilient exception handling, and network fault simulation using Requestly.

---

## 🚀 Key Features

- **Asynchronous Architecture:** Built on FastAPI and `aiosqlite` for non-blocking I/O operations and high concurrent checkout throughput.
- **Strict Pydantic Validation Contracts:**
  - **SKU Pattern Enforcement:** Rejects malformed, lowercase, whitespace, or symbol-corrupted SKUs using strict regex (`^[A-Z0-9]{2,8}(-[A-Z0-9]{2,10})+$`).
  - **Negative Stock Count Prohibition:** Rejects negative quantity payloads before reaching the persistence layer.
  - **Zero Quantity Restrictions:** Rejects no-op deduction requests.
  - **Stock Limit Breach Guard:** Atomically computes available stock (`current_stock - reserved_stock`) and raises structured `422 INSUFFICIENT_STOCK` errors when orders exceed warehouse reserves.
- **Uniform Error Envelope:** All validation errors, domain exceptions, and unexpected server failures return a standardized JSON structure (`success: false`, `error_code`, `message`, `details`, `timestamp`).
- **Network & Upstream Simulation:** Native support for simulating 429 Rate Limiting, 500 Upstream ERP failures, and artificial network latency delays.
- **Exported Requestly Integration:** Ready-to-import `requestly_rules.json` configuration for testing frontend timeout and retry policies.
- **100% Test Coverage:** 15 automated asynchronous Pytest unit and integration tests covering all positive, negative, and simulated failure conditions.

---

## 📁 Project Directory Structure

```text
backend/
├── database.py              # Async SQLite connection manager & catalog seeding
├── inventory.db             # SQLite database file containing the inventory catalog
├── main.py                  # FastAPI application, exception handlers & routing
├── schemas.py               # Pydantic models & custom field/model validators
├── sample_payloads.json     # Comprehensive synthetic JSON payloads for testing
├── requestly_rules.json     # Exported Requestly network simulation rule definitions
├── test_inventory.py        # Asynchronous Pytest test suite (15 test cases)
├── test_results.txt         # Terminal execution log showing 100% test pass rate
├── README.md                # Technical documentation and API guide
└── RECORDING_GUIDE.md       # 60-minute verbal script and action plan for screen recording
```

---

## 🛠️ Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ installed with the following packages:
```bash
pip install fastapi uvicorn pydantic aiosqlite pytest httpx
```

### 2. Launching the Local API Server
Start the Uvicorn server with hot-reload enabled:
```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The service will automatically initialize `inventory.db` and seed 7 initial e-commerce products if the database is fresh.

### 3. Accessing Interactive Swagger UI
Open your browser and navigate to:
```text
http://127.0.0.1:8000/docs
```
You can also view alternative documentation via ReDoc at `http://127.0.0.1:8000/redoc`.

---

## 🔌 API Endpoints Reference

### 1. Health Check
- **Endpoint:** `GET /api/v1/health`
- **Description:** Verifies service uptime and SQLite database connectivity.
- **Sample Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected",
  "catalog_item_count": 7
}
```

### 2. List Inventory
- **Endpoint:** `GET /api/v1/inventory`
- **Description:** Fetches all products with calculated available stock (`current_stock - reserved_stock`).
- **Sample Item Response (200 OK):**
```json
[
  {
    "id": 1,
    "sku": "PROD-1001-BLK",
    "name": "Ultra Wireless Headphones - Matte Black",
    "current_stock": 50,
    "reserved_stock": 0,
    "available_stock": 50,
    "price": 149.99
  }
]
```

### 3. Get Item by SKU
- **Endpoint:** `GET /api/v1/inventory/{sku}`
- **Description:** Retrieves real-time stock and pricing for a specific SKU.
- **Error Response (404 Not Found):**
```json
{
  "success": false,
  "error_code": "ITEM_NOT_FOUND",
  "message": "Product item with SKU 'NON-EXISTENT' was not found in catalog.",
  "details": { "sku": "NON-EXISTENT" }
}
```

### 4. Update Inventory Stock (Atomic Deduction / Restock)
- **Endpoint:** `POST /api/v1/inventory/update`
- **Description:** Adjusts inventory levels atomically with strict data validation.
- **Request Body (Valid Deduction):**
```json
{
  "sku": "PROD-1001-BLK",
  "quantity": 5,
  "operation": "deduct",
  "reason": "Order #ORD-78194 fulfillment",
  "reference_id": "ORD-78194"
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "sku": "PROD-1001-BLK",
  "product_name": "Ultra Wireless Headphones - Matte Black",
  "operation": "deduct",
  "quantity_modified": 5,
  "previous_stock": 50,
  "new_stock": 45,
  "available_stock": 45,
  "message": "Stock successfully adjusted for 'PROD-1001-BLK' by 5 unit(s)."
}
```

---

## 🛡️ Edge Case Validations & Error Envelopes

### Edge Case 1: Negative Stock Count in Payload
If a client attempts to pass a negative quantity (e.g., `"quantity": -15`), Pydantic's custom validator immediately rejects it:
- **HTTP Status:** `422 Unprocessable Content`
- **Response:**
```json
{
  "success": false,
  "error_code": "PAYLOAD_VALIDATION_ERROR",
  "message": "The inventory update payload contains invalid or malformed data.",
  "details": [
    {
      "field": "body -> quantity",
      "issue": "Value error, Invalid quantity '-15'. Negative stock count values are forbidden in update payloads. Specify positive quantity and choose operation 'deduct' or 'restock'."
    }
  ]
}
```

### Edge Case 2: Malformed SKU Format
If a client passes an invalid SKU format (e.g., lowercase `"prod-1001-blk"` or symbols `"PROD$$1001!!"`):
- **HTTP Status:** `422 Unprocessable Content`
- **Response:**
```json
{
  "success": false,
  "error_code": "PAYLOAD_VALIDATION_ERROR",
  "message": "The inventory update payload contains invalid or malformed data.",
  "details": [
    {
      "field": "body -> sku",
      "issue": "Value error, Malformed SKU 'prod-1001-blk'. Must match standard pattern '^[A-Z0-9]{2,8}(-[A-Z0-9]{2,10})+$', e.g., 'PROD-1001-BLK'."
    }
  ]
}
```

### Edge Case 3: Stock Limit Breach (Over-Deduction)
If a client attempts to deduct more stock than is currently available:
- **HTTP Status:** `422 Unprocessable Content`
- **Response:**
```json
{
  "success": false,
  "error_code": "INSUFFICIENT_STOCK",
  "message": "Insufficient stock for SKU 'PROD-5500-LMT'. Available for checkout: 2, Requested deduction: 50.",
  "details": {
    "message": "Insufficient stock for SKU 'PROD-5500-LMT'. Available for checkout: 2, Requested deduction: 50.",
    "error_code": "INSUFFICIENT_STOCK",
    "available_stock": 2,
    "requested_quantity": 50
  }
}
```

---

## 🌐 Requestly Interception & Fault Simulation

The file `requestly_rules.json` contains pre-configured interceptor rules for the Requestly macOS Desktop App:

| Rule Name | Target URL | Simulation Type | Expected Behavior |
|:---|:---|:---|:---|
| **Simulate API Rate Limiting** | `/api/v1/inventory/update` | HTTP 429 Override | Returns `RATE_LIMIT_EXCEEDED` with `Retry-After: 60` header |
| **Simulate Upstream ERP Failure** | `/api/v1/inventory/update` | HTTP 500 Override | Returns `UPSTREAM_ERP_UNAVAILABLE` error payload |
| **Simulate Network Latency** | `/api/v1/inventory` | 2500ms Delay | Injects 2.5s delay to test frontend loading state & timeouts |

### Importing Rules into Requestly Desktop App:
1. Open the **Requestly macOS Desktop App**.
2. Navigate to **Rules** in the left sidebar.
3. Click **Settings / Import** and select `backend/requestly_rules.json`.
4. Toggle the desired rule to **Active** to test endpoint behavior in the Requestly API Client or your frontend application.

---

## 🧪 Running Automated Unit Tests

Execute the comprehensive test suite with Pytest:
```bash
python3 -m pytest -v -s backend/test_inventory.py
```

To export the test results log file:
```bash
python3 -m pytest -v -s backend/test_inventory.py > backend/test_results.txt
```

### Test Suite Summary:
```text
backend/test_inventory.py::test_health_check[asyncio] PASSED
backend/test_inventory.py::test_get_all_inventory[asyncio] PASSED
backend/test_inventory.py::test_get_single_inventory_item_success[asyncio] PASSED
backend/test_inventory.py::test_get_single_inventory_item_not_found[asyncio] PASSED
backend/test_inventory.py::test_successful_stock_deduction[asyncio] PASSED
backend/test_inventory.py::test_successful_restock[asyncio] PASSED
backend/test_inventory.py::test_edge_case_negative_quantity_rejected[asyncio] PASSED
backend/test_inventory.py::test_edge_case_zero_quantity_rejected[asyncio] PASSED
backend/test_inventory.py::test_edge_case_malformed_sku_lowercase[asyncio] PASSED
backend/test_inventory.py::test_edge_case_malformed_sku_special_characters[asyncio] PASSED
backend/test_inventory.py::test_edge_case_insufficient_stock_exceeded[asyncio] PASSED
backend/test_inventory.py::test_edge_case_update_nonexistent_sku[asyncio] PASSED
backend/test_inventory.py::test_upstream_simulation_rate_limit_429[asyncio] PASSED
backend/test_inventory.py::test_upstream_simulation_server_error_500[asyncio] PASSED
backend/test_inventory.py::test_latency_delay_simulation_header[asyncio] PASSED

======================== 15 passed in 0.35s ========================
```
