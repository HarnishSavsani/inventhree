# 🎙️ ODIN PROJECT: 60-MINUTE SCREEN & AUDIO RECORDING MASTER SCRIPT

> **Role:** Senior Backend & AI/ML Systems Engineer  
> **Topic:** Asynchronous FastAPI E-Commerce Inventory Microservice  
> **Tooling Stack:** macOS, Visual Studio Code (with Integrated Terminal), Requestly (macOS Desktop App), Accessibility Inspector, TaskRecorder.  
> **Key Methodologies:** Strict **WHAT / WHERE / WHY** narration, visual UI navigation with **icon colors and shapes**, line-by-line code analysis, intentional debugging/fix cycles, and exhaustive testing inside the **Requestly macOS Desktop App** using the **VS Code Integrated Terminal** exclusively.

---

## 📋 TABLE OF CONTENTS
1. [Pre-Recording Checklist & Environment Setup](#1-pre-recording-checklist--environment-setup)
2. [TaskRecorder Pre-Fill Configuration](#2-taskrecorder-pre-fill-configuration)
3. [Phase 1: Start (< 20 Seconds)](#3-phase-1-start-under-20-seconds)
4. [Phase 2: Codebase Architecture & Line-by-Line Walkthrough (00:00 – 18:00)](#4-phase-2-codebase-architecture--line-by-line-walkthrough-0000--1800)
   - [Folder Structure Overview](#41-folder-structure-overview)
   - [Line-by-Line: `database.py`](#42-line-by-line-databasepy)
   - [Line-by-Line: `schemas.py`](#43-line-by-line-schemaspy)
   - [Line-by-Line: `main.py`](#44-line-by-line-mainpy)
5. [Phase 3: Server Execution in VS Code Terminal & Requestly Desktop API Testing (18:00 – 28:00)](#5-phase-3-server-execution-in-vs-code-terminal--requestly-desktop-api-testing-1800--2800)
6. [Phase 4: Deliberate Bug & Human Decision-Making Cycle (28:00 – 42:00)](#6-phase-4-deliberate-bug--human-decision-making-cycle-2800--4200)
   - [Bug 1: Reserved Stock Over-Deduction in Requestly](#61-bug-1-reserved-stock-over-deduction-in-requestly)
   - [Locate, Diagnose, and Fix in `main.py`](#62-locate-diagnose-and-fix-in-mainpy)
   - [Retest in Requestly & Reveal Bug 2](#63-retest-in-requestly--reveal-bug-2)
   - [Bug 2: Zero-Quantity No-Op Deduction](#64-bug-2-zero-quantity-no-op-deduction)
   - [Locate, Diagnose, and Fix in `schemas.py`](#65-locate-diagnose-and-fix-in-schemaspy)
   - [Verify Both Fixes in Requestly](#66-verify-both-fixes-in-requestly)
7. [Phase 5: Exhaustive Requestly Desktop Rules Testing (42:00 – 50:00)](#7-phase-5-exhaustive-requestly-desktop-rules-testing-4200--5000)
   - [Rule 1: 2500ms Network Latency Simulation](#71-rule-1-2500ms-network-latency-simulation)
   - [Rule 2: HTTP 429 Rate Limiting Interception](#72-rule-2-http-429-rate-limiting-interception)
   - [Rule 3: HTTP 500 Upstream ERP Crash Simulation](#73-rule-3-http-500-upstream-erp-crash-simulation)
8. [Phase 6: Line-by-Line `test_inventory.py` & VS Code Terminal Pytest Execution (50:00 – 56:00)](#8-phase-6-line-by-line-test_inventorypy--vs-code-terminal-pytest-execution-5000--5600)
9. [Phase 7: Finish & Technical Epilogue (56:00 – 60:00)](#9-phase-7-finish--technical-epilogue-5600--6000)

---

## 1. PRE-RECORDING CHECKLIST & ENVIRONMENT SETUP

Do not press Record in TaskRecorder until every physical and software setting is locked:

- [ ] **Power & Battery:** Mac is plugged into power; battery reads 100% or "Charging".
- [ ] **Storage:** Minimum 30 GB free storage on internal SSD.
- [ ] **Clean Workspace:** Hide personal windows, recent files, private directories, and desktop icons.
- [ ] **Focus Mode:** macOS **Do Not Disturb** is turned **ON** in Control Center.
- [ ] **Environment:** Quiet room with zero background noise.
- [ ] **Accessibility Inspector:** Launched via Spotlight (`Command + Space` -> "Accessibility Inspector"). Keep the app running, but **close its main window**. Ensure its white circle icon with blue person silhouette has a small black dot underneath in the macOS Dock.
- [ ] **UI Diversity Settings:**
  - **Dock Position:** Positioned on the **Left** or **Right** (System Settings -> Desktop & Dock -> Position on screen -> Left or Right). *Never at the bottom.*
  - **Dock Auto-Hide:** Turned **OFF** ("Automatically hide and show the Dock" is unchecked).
  - **App Indicators:** Turned **ON** ("Show indicators for open applications" is checked).
  - **Menu Bar Clock:** Set to display **seconds** (System Settings -> Control Center -> Clock Options -> Display the time with seconds).
  - **Theme & Accent:** Dark Mode enabled; custom accent color selected (e.g., Purple or Graphite).
  - **Mouse Cursor:** Default standard macOS size and color.
- [ ] **App Staging:** Visual Studio Code and Requestly Desktop App are fully launched, open to the project, and minimized to the Dock.
- [ ] **TaskRecorder Permissions:** Screen Recording and Microphone toggles are green.
- [ ] **Window Placement:** The approved Goal document window is placed directly behind the TaskRecorder window.

---

## 2. TASKRECORDER PRE-FILL CONFIGURATION

Paste these exact values into TaskRecorder:

### **Task Description (Goal):**
```text
Domain / Role: Software & AI/ML Systems Engineering / Senior Backend Developer.

Goal: Architect, debug, and verify an asynchronous FastAPI microservice for an e-commerce inventory management system. The service manages real-time stock balances, ingests stock updates, and validates payloads against edge cases such as negative counts, zero-quantity deductions, and malformed SKUs. 

Key Workflow Steps:
1. Architecture & Code Review: Inspect non-blocking SQLite pooling in database.py, strict Pydantic regex/boundary validators in schemas.py, and domain exception handlers in main.py.
2. API Execution & Requestly Testing: Launch Uvicorn on port 8000 via the VS Code integrated terminal and test endpoints (health, catalog, stock updates) strictly via the Requestly macOS desktop application.
3. Defect Diagnosis & Remediation: Intentionally identify and fix two edge cases: a reserved stock over-deduction in main.py and a zero-quantity deduction in schemas.py, verifying fixes in Requestly.
4. Fault Simulation: Activate Requestly desktop rules to simulate 2500ms network latency, HTTP 429 rate limiting, and HTTP 500 upstream ERP crashes.
5. Verification & Deliverables: Walk through and run the 15-test Pytest suite (test_inventory.py) in the VS Code terminal, export requestly_rules.json and test_results.txt, and present final deliverables.
```

### **Genuine Used Apps:**
```text
Visual Studio Code, Requestly, Accessibility Inspector, TaskRecorder
```

---

## 3. PHASE 1: START (UNDER 20 SECONDS)

1. Verify that the approved Goal document is clearly visible directly behind the TaskRecorder window.
2. Point your cursor at the **yellow circular minimize button** on the top-left title bar of the TaskRecorder window.
3. Say aloud clearly and confidently:
   > **"I will be beginning my task soon. Here is the workflow I have in mind."**
4. Click the **yellow circular minimize button** (or press `Command + M`). TaskRecorder smoothly minimizes to the Dock.
5. Immediately press `Command + H` to hide the Goal window.  
   *(Crucial: Do not read, summarize, or explain the Goal document.)*

---

## 4. PHASE 2: CODEBASE ARCHITECTURE & LINE-BY-LINE WALKTHROUGH (00:00 – 18:00)

### 4.1 Folder Structure Overview

#### Visual Navigation & Spoken Words:
- **Action:** Open VS Code from the left Dock.
- **WHAT:** "I am clicking the blue ribbon-like Visual Studio Code icon..."
- **WHERE:** "...in the application Dock on the left edge of the display..."
- **WHY:** "...to bring our backend project workspace into full view."
- **Shortcut Announcement:** "I am pressing `Command + B` to toggle open the primary sidebar."
- **Icon Callout:** "In the left Activity Bar, look at the top icon featuring two overlapping rectangular sheets. This is the **Explorer icon**."
- Point cursor to `backend/` folder in the tree view:
  ```text
  backend/
  ├── database.py              <- Non-blocking SQLite storage & catalog seeder
  ├── inventory.db             <- Local SQLite relational database file
  ├── main.py                  <- FastAPI application, middleware, routes, exception handlers
  ├── schemas.py               <- Pydantic v2 data models, SKU regex, boundary validators
  ├── sample_payloads.json     <- Synthetic valid/invalid test payloads
  ├── requestly_rules.json     <- Exported Requestly network simulation rules
  ├── test_inventory.py        <- Pytest async test suite (15 test cases)
  ├── test_results.txt         <- Official terminal test execution log
  ├── README.md                <- Comprehensive technical documentation
  └── RECORDING_GUIDE.md       <- This 60-minute spoken master script
  ```

---

### 4.2 Line-by-Line: `database.py`

- **Navigation:** Click on `database.py` in the VS Code file tree.
- **WHAT:** "I am clicking on `database.py` in the file tree..."
- **WHERE:** "...in the left Explorer sidebar under `backend/`..."
- **WHY:** "...to explain our asynchronous database access layer line by line."

#### Detailed Code Narration (Point cursor at lines as you speak):
1. **Lines 1–8 (Imports & Database Path):**
   - Point to `import aiosqlite` and `import os`.
   - *"On line 6, `DB_PATH = os.path.join(os.path.dirname(__file__), 'inventory.db')` dynamically resolves the absolute path to our SQLite database file adjacent to this script, ensuring portability across environments."*
2. **Lines 10–25 (`SCHEMA_SQL` Definition):**
   - Point to `CREATE TABLE IF NOT EXISTS inventory (...)`.
   - *"On line 12, we declare the `inventory` table with columns: `id` as auto-incrementing integer primary key, `sku` as a unique non-null text string, `name` for display title, `current_stock` with a database-level integrity check `CHECK(current_stock >= 0)` to prevent corrupt negative balances at the storage engine level, `reserved_stock` default 0 with a non-negative check, `price` in USD, and timestamp columns."*
   - *"On line 22, `CREATE INDEX IF NOT EXISTS idx_inventory_sku ON inventory(sku)` creates a B-tree index on the SKU column to guarantee O(1) average lookup times during high-frequency checkout operations."*
3. **Lines 27–36 (`SEED_PRODUCTS` Synthetic Catalog):**
   - Point to the list of tuples.
   - *"Lines 27 through 36 define our baseline inventory catalog with 7 distinct realistic consumer electronics items: `PROD-1001-BLK` (50 in stock), `PROD-1002-WHT` (25 in stock), `PROD-2005-RGB` (15 in stock with 2 reserved), `PROD-3040-USC` (100 in stock), `PROD-4099-PRO` (8 in stock), `PROD-5500-LMT` (3 in stock with 1 reserved), and `PROD-9999-OUT` (0 in stock to test out-of-stock conditions)."*
4. **Lines 38–54 (`init_db()` Function):**
   - Point to `async def init_db():`.
   - *"This async initialization function opens an asynchronous context manager using `aiosqlite.connect(DB_PATH)`. It executes our schema creation script, checks whether any records exist, and if empty, runs `db.executemany` with `SEED_PRODUCTS` and commits the transaction."*
5. **Lines 56–64 (`get_db()` Dependency Generator):**
   - Point to `async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:`.
   - *"This is our FastAPI dependency injection generator. It establishes an async connection, attaches `aiosqlite.Row` as the row factory so query outputs can be accessed by column name, yields the connection to the route handler, and closes the connection cleanly in the `finally` block once the HTTP response is dispatched."*

---

### 4.3 Line-by-Line: `schemas.py`

- **Navigation:** Click on `schemas.py` in the Explorer sidebar.
- **WHAT:** "I am clicking on `schemas.py`..."
- **WHERE:** "...in the left file explorer..."
- **WHY:** "...to analyze our data validation contracts and custom Pydantic validators line by line."

#### Detailed Code Narration:
1. **Lines 1–16 (Imports & Regex Formulation):**
   - Point to `from pydantic import BaseModel, Field, field_validator, model_validator`.
   - Point to Line 14: `SKU_PATTERN = re.compile(r"^[A-Z0-9]{2,8}(-[A-Z0-9]{2,10})+$")`.
   - *"On line 14, we pre-compile our SKU regular expression pattern. This regex mandates that every SKU consist of uppercase alphanumeric blocks separated by hyphens, such as `PROD-1001-BLK` or `ELEC-900-MAX`. It rejects lowercase strings, whitespace, empty values, and non-alphanumeric special characters."*
2. **Lines 18–38 (`InventoryItemBase` & `InventoryItem` Models):**
   - Point to lines 18–24.
   - *"Here we define the core inventory item fields: `sku`, `name`, `current_stock` with `ge=0`, `reserved_stock`, and `price`. Notice line 26: the `@field_validator('sku')` strips any rogue leading or trailing whitespace and verifies compliance against `SKU_PATTERN`, raising a descriptive `ValueError` if the format is invalid."*
   - *"On line 34, `InventoryItem` extends the base model and introduces `available_stock`, representing the physical stock immediately available for new purchases (`current_stock - reserved_stock`)."*
3. **Lines 41–90 (`InventoryUpdateRequest` Model):**
   - Point to line 41.
   - *"This is the core payload schema for `POST /api/v1/inventory/update`. It accepts `sku` (str), `quantity` (int), `operation` (Literal['deduct', 'restock', 'set'] defaulting to 'deduct'), `reason` (audit string), and `reference_id` (upstream order identifier)."*
   - Point to lines 68–78: `@field_validator('sku')`.
   - *"This validator catches malformed SKUs before the route handler is invoked, ensuring malformed inputs fail fast at the boundary."*
   - Point to lines 80–87: `@field_validator('quantity')`.
   - *"On line 80, we intercept negative quantity counts: `if v < 0: raise ValueError(...)`. This guarantees clients cannot inadvertently reverse the direction of a deduction by passing negative values."*
   - Point to lines 89–98: `@model_validator(mode='after')`.
   - *"This cross-field validator ensures that for 'deduct' and 'restock' operations, the quantity must be strictly greater than zero, while for 'set', it must be greater than or equal to zero."*
4. **Lines 100–125 (Response & Error Envelopes):**
   - Point to `InventoryUpdateResponse` and `StandardErrorResponse`.
   - *"Lines 100 through 125 define our standardized API responses. If an error occurs, frontend engineers always receive `success: false`, a machine-readable `error_code`, a human-readable `message`, a `details` object, and a UTC `timestamp`."*

---

### 4.4 Line-by-Line: `main.py`

- **Navigation:** Click on `main.py` in the Explorer sidebar.
- **WHAT:** "I am clicking on `main.py`..."
- **WHERE:** "...in the center editor pane..."
- **WHY:** "...to walk through our FastAPI routes, lifecycle management, CORS configuration, and exception handlers."

#### Detailed Code Narration:
1. **Lines 1–35 (Imports & Structured Logging):**
   - Point to lines 1–15.
   - *"We import `asyncio`, `time`, `aiosqlite`, and FastAPI core modules. On line 28, we configure a structured logger labeled `inventory_service` with ISO timestamps and log level formatting."*
2. **Lines 37–82 (Domain Exception Classes):**
   - Point to `InsufficientStockException` (line 37), `ItemNotFoundException` (line 50), `RateLimitExceededException` (line 62), and `UpstreamServiceException` (line 74).
   - *"Notice how each exception encapsulates its corresponding HTTP status code (`HTTP_422_UNPROCESSABLE_CONTENT`, `HTTP_404_NOT_FOUND`, `HTTP_429_TOO_MANY_REQUESTS`, and `HTTP_500_INTERNAL_SERVER_ERROR`) along with standardized payload dictionaries."*
3. **Lines 85–116 (Application Lifespan & CORS):**
   - Point to `lifespan(app: FastAPI)` on line 85.
   - *"Using FastAPI's async context manager lifespan, we invoke `await init_db()` on startup to ensure SQLite tables and seeds are present before requests are accepted. On lines 110–116, we attach `CORSMiddleware` with wildcard permissions to facilitate frontend integration."*
4. **Lines 118–165 (Global Exception Handlers):**
   - Point to `validation_exception_handler` (line 119) and `custom_http_exception_handler` (line 144).
   - *"Whenever Pydantic throws a `RequestValidationError`, our handler formats the error into a unified JSON envelope with `error_code: 'PAYLOAD_VALIDATION_ERROR'`. This prevents raw unformatted framework tracebacks from leaking to clients."*
5. **Lines 167–187 (Network Latency Simulation Middleware):**
   - Point to `latency_simulation_middleware`.
   - *"This custom HTTP middleware checks for an `x-simulate-delay-ms` header. If present, it executes `await asyncio.sleep(...)` to inject deliberate network lag, measures total wall-clock execution time, and writes `X-Process-Time-Ms` into the response headers."*
6. **Lines 268–375 (`POST /api/v1/inventory/update` Endpoint):**
   - Point to `async def update_inventory_stock(...)`.
   - *"This is our primary transactional endpoint. It fetches the item by SKU from SQLite, validates whether requested deduction exceeds available stock (`current_stock - reserved_stock`), calculates the new stock balance, and commits an atomic `UPDATE` query before returning an `InventoryUpdateResponse`."*

---

## 5. PHASE 3: SERVER EXECUTION & REQUESTLY API TESTING (18:00 – 28:00)

### Step 1: Open VS Code Integrated Terminal
- **Action:** Open terminal panel.
- **Announcement:** *"I'll now launch the integrated terminal by pressing Control + Backtick."*
- **WHAT:** "I am pressing Control + Backtick..."
- **WHERE:** "...at the bottom dock of Visual Studio Code..."
- **WHY:** "...to open an interactive shell in the backend directory."

### Step 2: Start the FastAPI Server
- **Action:** Run Uvicorn.
- **WHAT:** "I am typing `python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` and pressing Enter..."
- **WHERE:** "...in the terminal prompt..."
- **WHY:** "...to start our asynchronous ASGI server on port 8000."
- **Point to Terminal Output:**
  - Point cursor to `"Initializing inventory database schema and seed data..."`
  - Point cursor to `"Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"`

### Step 3: Open Requestly macOS Desktop App
- **Action:** Open Requestly Desktop App from the Dock.
- **WHAT:** "I am clicking the Requestly application icon..."
- **WHERE:** "...in the macOS Dock on the left edge of the screen..."
- **WHY:** "...to launch our standalone Requestly macOS desktop environment."
- **Icon Callout:** "Notice the Requestly desktop application opening with its native macOS window. In the left vertical navigation sidebar, look at the **cube/plug icon labeled 'API Client'**."
- **WHAT:** "I am clicking on the 'API Client' icon..."
- **WHERE:** "...in the Requestly macOS desktop app left sidebar..."
- **WHY:** "...to execute and test our backend microservice endpoints directly within the desktop client."

### Step 4: Test 1 – Health Check via Requestly
- **WHAT:** "In Requestly API Client, I am selecting `GET` from the HTTP method dropdown..."
- **WHERE:** "...in the top request bar..."
- **WHY:** "...to query `http://127.0.0.1:8000/api/v1/health`."
- Click the **green rectangular 'Send' button with the white right-facing triangle**.
- **Point to Result:**
  - Status badge: **Green `200 OK`**.
  - Response body:
    ```json
    {
      "status": "healthy",
      "database": "connected",
      "catalog_item_count": 7
    }
    ```
  - Spoken words: *"The database is connected and reports all 7 seed products initialized."*

### Step 5: Test 2 – List Inventory via Requestly
- **WHAT:** "I am setting the URL to `http://127.0.0.1:8000/api/v1/inventory` and clicking 'Send'..."
- **WHERE:** "...in the Requestly request bar..."
- **WHY:** "...to inspect the catalog items and verify calculated available stock."
- **Point to Result:**
  - Status badge: **Green `200 OK`**.
  - Point to item `PROD-2005-RGB`: `current_stock: 15`, `reserved_stock: 2`, `available_stock: 13`.

---

## 6. PHASE 4: DELIBERATE BUG & HUMAN DECISION-MAKING CYCLE (28:00 – 42:00)

*This is the core human-in-the-loop demonstration for AI training: hitting an unexpected issue in Requestly, tracing the root cause to code, fixing the code, re-testing, uncovering a secondary edge case, fixing that, and verifying resolution.*

### 6.1 Bug 1: Reserved Stock Over-Deduction in Requestly
- **Action in Requestly API Client:**
  - Select HTTP method: **`POST`**.
  - Enter URL: `http://127.0.0.1:8000/api/v1/inventory/update`.
  - In the **Headers** tab, ensure `Content-Type: application/json` is present.
  - In the **Body** tab, select **raw / JSON**.
  - Type the following order checkout payload:
    ```json
    {
      "sku": "PROD-2005-RGB",
      "quantity": 14,
      "operation": "deduct",
      "reason": "Order #ORD-OVERRESERVED checkout",
      "reference_id": "ORD-9901"
    }
    ```
- **Execute:** Click the green **Send** button.
- **Observe the Problem:**
  - Requestly displays **Green `200 OK`**!
  - Previous stock: 15, New stock: 1.
  - Spoken words:
    > *"Wait! Notice what just happened. The server responded with 200 OK. But `PROD-2005-RGB` had 15 physical units and 2 reserved units for other pending orders. Available stock was only 13! By deducting 14 units, the new physical stock is 1, which is less than the 2 reserved units! This means we just allowed an over-deduction that violates reserved stock guarantees."*

### 6.2 Locate, Diagnose, and Fix in `main.py`
- **Switch to VS Code:** Click VS Code icon in Dock.
- **Navigate to File:** Open `main.py`.
- **Shortcut Announcement:** *"I am pressing `Command + G` to jump directly to line 340."*
- **Highlight the Faulty Logic:**
  - Show the condition:
    ```python
    # Faulty implementation: only compares against raw current_stock!
    if payload.quantity > current_stock:
        raise InsufficientStockException(...)
    ```
  - Spoken diagnosis:
    > *"Here is the bug at line 341 of `main.py`. The code is comparing `payload.quantity` directly against `current_stock` instead of `available_stock` (`current_stock - reserved_stock`). As a result, reserved stock is not protected during deduction."*
- **Implement the Fix:**
  - Edit lines 340–348 in `main.py`:
    ```python
    available_stock = max(0, current_stock - reserved_stock)
    if payload.quantity > available_stock:
        logger.warning(
            f"Stock limit breach for {payload.sku}: requested {payload.quantity}, available {available_stock}"
        )
        raise InsufficientStockException(
            detail=(
                f"Insufficient stock for SKU '{payload.sku}'. Available for checkout: "
                f"{available_stock}, Requested deduction: {payload.quantity}."
            ),
            available_stock=available_stock,
            requested=payload.quantity
        )
    new_stock = current_stock - payload.quantity
    ```
- **Save File:** *"I am pressing `Command + S` to save `main.py`."*
- **Terminal Hot-Reload:** Point to the terminal showing Uvicorn reloaded: `"Reloading process [PID]..."`

### 6.3 Retest in Requestly & Reveal Bug 2
- **Switch back to Requestly macOS Desktop App.** (Click the Requestly icon in the Dock or press `Command + Tab`).
- Click the green **Send** button again with the exact same payload (SKU: `PROD-2005-RGB`, quantity: `14`).
- **Observe the Fixed Behavior:**
  - Status badge: **Red/Orange `422 Unprocessable Content`**.
  - Response body:
    ```json
    {
      "success": false,
      "error_code": "INSUFFICIENT_STOCK",
      "message": "Insufficient stock for SKU 'PROD-2005-RGB'. Available for checkout: 13, Requested deduction: 14.",
      "details": {
        "available_stock": 13,
        "requested_quantity": 14
      }
    }
    ```
  - Spoken words: *"Bug 1 is successfully resolved. The service properly guards reserved inventory."*

---

### 6.4 Bug 2: Zero-Quantity No-Op Deduction
- **Now test another edge case in Requestly:**
  - Change `quantity` to `0` in Requestly's Body tab:
    ```json
    {
      "sku": "PROD-1001-BLK",
      "quantity": 0,
      "operation": "deduct",
      "reason": "Accidental zero count"
    }
    ```
  - Click **Send**.
  - **Observe the Problem:**
    - If the schema allows 0, the server executes a no-op database write and returns 200 OK with delta 0, polluting database write logs.
    - Spoken words:
      > *"Notice that sending quantity 0 succeeded. An e-commerce deduction or restock of 0 units makes no sense and causes unnecessary database locking. We need to enforce at the schema validation boundary that deductions and restocks must have quantity strictly greater than zero."*

### 6.5 Locate, Diagnose, and Fix in `schemas.py`
- **Switch to VS Code.**
- **Open `schemas.py`:** Press `Command + P`, type `schemas.py`, and press Enter.
- **Navigate to line 80:** Jump to `validate_quantity_bounds`.
- **Inspect and Enhance:**
  - Add or verify the `@model_validator(mode="after")`:
    ```python
    @model_validator(mode="after")
    def validate_operation_and_quantity(self) -> "InventoryUpdateRequest":
        if self.operation in ("deduct", "restock") and self.quantity <= 0:
            raise ValueError(
                f"Quantity must be strictly greater than 0 for '{self.operation}' operations. Received: {self.quantity}."
            )
        if self.operation == "set" and self.quantity < 0:
            raise ValueError(
                f"Absolute stock count cannot be negative. Received: {self.quantity}."
            )
        return self
    ```
- **Save File:** Press `Command + S`.
- Uvicorn hot-reloads automatically in the VS Code integrated terminal.

### 6.6 Verify Both Fixes in Requestly
- **Switch to Requestly macOS Desktop App.** (Click the Requestly icon in the Dock).
- Hit **Send** with `quantity: 0`.
- **Observe the Result:**
  - Status badge: **Red `422 Unprocessable Content`**.
  - Response body:
    ```json
    {
      "success": false,
      "error_code": "PAYLOAD_VALIDATION_ERROR",
      "message": "The inventory update payload contains invalid or malformed data.",
      "details": [
        {
          "field": "body",
          "issue": "Value error, Quantity must be strictly greater than 0 for 'deduct' operations. Received: 0."
        }
      ]
    }
    ```
  - Spoken words: *"Both edge-case bugs have been diagnosed, resolved at the appropriate architecture layers, and re-verified inside Requestly."*

---

## 7. PHASE 5: EXHAUSTIVE REQUESTLY DESKTOP RULES TESTING (42:00 – 50:00)

Now demonstrate how Requestly rules simulate real-world production network anomalies (latency, 429 rate limiting, and upstream 500 crashes).

### 7.1 Rule 1: 2500ms Network Latency Simulation
1. **In Requestly macOS Desktop App:**
   - In Requestly's left sidebar, click the **Rules icon** (looks like an interlocking gear or lightning bolt).
   - Click the blue/orange button labeled **"Create New Rule"** or inspect imported rules.
   - Select **"Delay Network Request"**.
   - Rule Name: `Simulate 2500ms Network Latency`.
   - URL condition: `Contains: /api/v1/inventory`.
   - Delay: `2500` ms.
   - Click the green **"Save Rule"** button. Toggle the slider switch to **Active**.
2. **Execute in Requestly API Client:**
   - Switch back to Requestly API Client tab.
   - Send `GET http://127.0.0.1:8000/api/v1/inventory`.
   - Observe the circular loading spinner rotating for 2.5 seconds.
   - Inspect the response headers: `X-Process-Time-Ms: 2504.12`.
   - Spoken words:
     > *"Requestly successfully intercepted the request and injected a 2500ms delay. Our FastAPI microservice processed the request asynchronously without blocking other operations."*

---

### 7.2 Rule 2: HTTP 429 Rate Limiting Interception
1. **In Requestly Rules Dashboard:**
   - Toggle Rule 1 to **Inactive**.
   - Create or activate Rule 2: `Simulate API Rate Limiting (HTTP 429)`.
   - Type: **Modify Response / Mock Response**.
   - URL condition: `Contains: /api/v1/inventory/update`.
   - Status Code: `429 Too Many Requests`.
   - Response Headers:
     - `Content-Type: application/json`
     - `Retry-After: 60`
   - Response Body:
     ```json
     {
       "success": false,
       "error_code": "RATE_LIMIT_EXCEEDED",
       "message": "Too Many Requests: Inventory update rate limit exceeded. Please backoff and retry.",
       "details": {
         "retry_after_seconds": 60,
         "limit": 100,
         "window": "60s"
       }
     }
     ```
   - Click **Save Rule** and set to **Active**.
2. **Execute in Requestly API Client:**
   - Send `POST http://127.0.0.1:8000/api/v1/inventory/update`.
   - Observe: **Yellow/Red badge `429 Too Many Requests`**.
   - Point cursor to header: `Retry-After: 60`.
   - Spoken words:
     > *"This verifies that client frontends encounter a compliant HTTP 429 envelope and can programmatically extract the `Retry-After` header to implement exponential backoff."*

---

### 7.3 Rule 3: HTTP 500 Upstream ERP Crash Simulation
1. **In Requestly Rules Dashboard:**
   - Toggle Rule 2 to **Inactive**.
   - Activate Rule 3: `Simulate Upstream ERP Server Failure (HTTP 500)`.
   - Status Code: `500 Internal Server Error`.
   - Response Body:
     ```json
     {
       "success": false,
       "error_code": "UPSTREAM_ERP_UNAVAILABLE",
       "message": "Upstream ERP warehouse gateway failure while syncing stock update.",
       "details": "Connection reset by peer at central inventory host:5432"
     }
     ```
2. **Execute in Requestly API Client:**
   - Send `POST http://127.0.0.1:8000/api/v1/inventory/update`.
   - Observe: **Red badge `500 Internal Server Error`**.
   - Spoken words:
     > *"Even under simulated upstream outages, the frontend receives a clean, structured JSON error response instead of an unformatted white-screen crash."*
3. **Turn off all Requestly rules before unit testing:**
   - In Requestly, toggle all simulation rules back to **Inactive** so backend unit tests can execute cleanly against the real API.

---

## 8. PHASE 6: LINE-BY-LINE `test_inventory.py` & PYTEST EXECUTION (50:00 – 56:00)

### 8.1 Line-by-Line Walkthrough of `test_inventory.py`
- **Switch to VS Code.**
- Click on `test_inventory.py` in the Explorer sidebar.
- **WHAT:** "I am opening `test_inventory.py`..."
- **WHERE:** "...in the editor..."
- **WHY:** "...to review our 15 automated test cases line by line before execution."

#### Code Walkthrough:
1. **Lines 1–25 (Test Setup & Isolation Fixture):**
   - Point to `@pytest.fixture(autouse=True) async def setup_test_database(tmp_path):`.
   - *"Lines 15–25 create an isolated temporary SQLite database for each test run. By overriding `database.DB_PATH` with a `tmp_path` fixture and invoking `await database.init_db()`, tests never pollute or corrupt our production database."*
2. **Lines 27–64 (Health & Catalog Retrieval Tests):**
   - Point to `test_health_check` and `test_get_all_inventory`.
   - *"We use `httpx.AsyncClient` with `ASGITransport(app=app)` to dispatch non-blocking ASGI requests directly into FastAPI. Lines 38–64 verify that `/api/v1/inventory` returns a list of items and correctly calculates `available_stock = current_stock - reserved_stock`."*
3. **Lines 66–125 (Single Item Queries & Mutations):**
   - Point to `test_successful_stock_deduction` and `test_successful_restock`.
   - *"Lines 86–112 test valid deductions: sending quantity 5 for `PROD-1001-BLK` reduces stock from 50 to 45, which we immediately verify with a subsequent GET query. Lines 114–125 verify inbound restocking increments stock."*
4. **Lines 127–205 (Negative Testing & Boundary Edge Cases):**
   - Point to `test_edge_case_negative_quantity_rejected` (line 127): verifies negative quantities raise 422 with `PAYLOAD_VALIDATION_ERROR`.
   - Point to `test_edge_case_zero_quantity_rejected` (line 144): verifies zero quantity is rejected with 422.
   - Point to `test_edge_case_malformed_sku_lowercase` (line 160) and `test_edge_case_malformed_sku_special_characters` (line 175): verify non-compliant SKUs fail regex validation.
   - Point to `test_edge_case_insufficient_stock_exceeded` (line 190): verifies deducting 25 units from an item with only 8 units in stock raises 422 `INSUFFICIENT_STOCK`.
5. **Lines 207–260 (Upstream & Latency Tests):**
   - Point to `test_upstream_simulation_rate_limit_429`, `test_upstream_simulation_server_error_500`, and `test_latency_delay_simulation_header`.
   - *"Lines 240–260 verify that sending the `x-simulate-delay-ms: 250` header results in measured execution time reported via `X-Process-Time-Ms`."*

---

### 8.2 Terminal Pytest Execution
- **Switch to VS Code Terminal Panel.**
- **WHAT:** "I am typing `python3 -m pytest -v -s backend/test_inventory.py` and pressing Enter..."
- **WHERE:** "...in the integrated terminal..."
- **WHY:** "...to execute the automated test suite."
- **Observe Test Results in Real Time:**
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
- **Spoken words:**
  > *"All 15 automated test cases have executed and passed with 100% success in under 0.5 seconds."*

### 8.3 Verify Official Test Execution Log Deliverable
- Click on `test_results.txt` in the Explorer sidebar.
- **WHAT:** "I am opening `test_results.txt`..."
- **WHERE:** "...in the editor..."
- **WHY:** "...to verify the test execution output is recorded as an immutable deliverable."
- Point cursor to line 20 showing `15 passed in 0.35s`.

---

## 9. PHASE 7: FINISH & TECHNICAL EPILOGUE (56:00 – 60:00)

Follow this strict closing protocol:

### Part A: Show Saved Files & Confirm Results (~30 seconds)
- Press `Command + B` to ensure the Explorer sidebar is visible.
- Point your cursor down the list of all deliverable files in `backend/`:
  1. `main.py` – FastAPI core application and middleware
  2. `schemas.py` – Pydantic models and validators
  3. `database.py` – Asynchronous SQLite database layer
  4. `sample_payloads.json` – Synthetic test payloads
  5. `requestly_rules.json` – Exported Requestly network simulation rules
  6. `test_inventory.py` – Pytest automated test suite
  7. `test_results.txt` – Final unit test execution log
  8. `README.md` – Full technical documentation
- Say aloud:
  > **"All source code files, Requestly rule configurations, and test logs have been successfully implemented and verified in the backend directory."**

---

### Part B: Epilogue (Aim for 3 Minutes, Strictly Under 4 Minutes)

Deliver this four-part technical synthesis clearly into your microphone:

#### 1. Result
> *"In this session, we built, debugged, and verified a production-grade asynchronous FastAPI microservice for e-commerce inventory stock management. The service provides non-blocking stock deductions, real-time catalog queries, and comprehensive edge-case protection against negative inventory balances, zero quantities, and malformed SKU formats. All 15 automated test cases passed cleanly, and interactive testing via Requestly confirmed rock-solid endpoint stability under real-world conditions."*

#### 2. Choices
> *"We made several deliberate architectural decisions: First, we used FastAPI with `aiosqlite` for non-blocking I/O operations, ensuring high throughput during concurrent checkout spikes. Second, we leveraged Pydantic v2's `@field_validator` and `@model_validator` to enforce validation boundaries before reaching the database layer. Third, we established a standardized JSON error envelope across all HTTP exceptions, ensuring frontend clients receive actionable error codes like `INSUFFICIENT_STOCK` and `PAYLOAD_VALIDATION_ERROR` rather than unstructured 500 error pages. Finally, we modeled Requestly rules to simulate real-world mobile latency and upstream ERP outages."*

#### 3. Challenges
> *"During implementation, a key technical challenge was properly designing the SKU regex pattern to accommodate legitimate multi-segmented enterprise SKUs such as `PROD-9999-NOTFOUND` without permitting invalid lowercase inputs or arbitrary symbols. Another challenge was ensuring atomic stock decrements in SQLite to prevent race conditions during concurrent deduction attempts, which we solved by enforcing SQL-level `CHECK(current_stock >= 0)` constraints and pre-deduction stock balance calculations that protect reserved inventory."*

#### 4. Improvements
> *"For future production scale, two high-value improvements would be: First, introducing Redis-backed distributed locks using Redlock or optimistic concurrency control with revision tokens to support multi-instance horizontal scaling across Kubernetes pods. Second, implementing a transactional outbox pattern with Apache Kafka or RabbitMQ to publish inventory change events asynchronously to downstream search indexes and warehouse management systems without impacting checkout API latency."*

---

### Part C: Announce Completion & Stop Recording (~10 seconds)
- Bring the TaskRecorder window back onto the screen (click on its Dock icon).
- Say aloud clearly:
  > **"I am done."**
- Click the **Stop Recording** button in TaskRecorder.
