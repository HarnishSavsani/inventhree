"""
Asynchronous FastAPI Microservice for E-Commerce Inventory Management.
Handles stock deduction, SKU validation, atomic SQLite persistence,
graceful error handling, and latency/upstream failure simulation.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import List, Optional

import aiosqlite
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import DB_PATH, get_db, init_db
from schemas import (
    InventoryItem,
    InventoryUpdateRequest,
    InventoryUpdateResponse,
    StandardErrorResponse,
)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [InventoryService] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("inventory_service")


# Custom domain exceptions
class InsufficientStockException(HTTPException):
    def __init__(self, detail: str, available_stock: int, requested: int):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "message": detail,
                "error_code": "INSUFFICIENT_STOCK",
                "available_stock": available_stock,
                "requested_quantity": requested
            }
        )


class ItemNotFoundException(HTTPException):
    def __init__(self, sku: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Product item with SKU '{sku}' was not found in catalog.",
                "error_code": "ITEM_NOT_FOUND",
                "sku": sku
            }
        )


class RateLimitExceededException(HTTPException):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Too Many Requests: Inventory update rate limit exceeded.",
                "error_code": "RATE_LIMIT_EXCEEDED",
                "retry_after_seconds": retry_after
            },
            headers={"Retry-After": str(retry_after)}
        )


class UpstreamServiceException(HTTPException):
    def __init__(self, detail: str = "Upstream ERP inventory warehouse service unavailable."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": detail,
                "error_code": "UPSTREAM_SERVICE_FAILURE"
            }
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for initialization and shutdown."""
    logger.info("Initializing inventory database schema and seed data...")
    await init_db()
    logger.info("Inventory microservice startup complete and ready for traffic.")
    yield
    logger.info("Shutting down inventory microservice.")


app = FastAPI(
    title="E-Commerce Inventory Management Microservice",
    description=(
        "Production-ready asynchronous FastAPI service handling stock deductions, "
        "SKU/negative count edge case validations, latency interception, and resilient failure modes."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for frontend engineering integration and Swagger UI access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Formats Pydantic validation failures (e.g. malformed SKU or negative stock counts)
    into a structured, frontend-friendly JSON response.
    """
    errors_list = []
    for err in exc.errors():
        loc = " -> ".join(str(x) for x in err.get("loc", []))
        msg = err.get("msg", "Validation error")
        errors_list.append({"field": loc, "issue": msg})

    logger.warning(
        f"Validation error on {request.method} {request.url.path} - Details: {errors_list}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "success": False,
            "error_code": "PAYLOAD_VALIDATION_ERROR",
            "message": "The inventory update payload contains invalid or malformed data.",
            "details": errors_list
        }
    )


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Uniform envelope for all domain HTTP exceptions."""
    if isinstance(exc.detail, dict):
        error_code = exc.detail.get("error_code", "HTTP_EXCEPTION")
        message = exc.detail.get("message", str(exc.detail))
        details = exc.detail
    else:
        error_code = "HTTP_ERROR"
        message = str(exc.detail)
        details = None

    logger.warning(
        f"HTTP {exc.status_code} on {request.method} {request.url.path}: {message}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={
            "success": False,
            "error_code": error_code,
            "message": message,
            "details": details
        }
    )


@app.exception_handler(Exception)
async def general_unhandled_exception_handler(request: Request, exc: Exception):
    """Catches unhandled runtime exceptions to guarantee clean 500 JSON output."""
    logger.error(f"Unhandled error processing {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An internal error occurred while processing inventory request.",
            "details": str(exc)
        }
    )


# Middlewares for tracking latency and network delay simulation
@app.middleware("http")
async def latency_simulation_middleware(request: Request, call_next):
    """
    Simulates network latency if the x-simulate-delay-ms header is supplied,
    and logs request processing duration.
    """
    start_time = time.time()
    
    # Optional delay simulation via request header (for testing Requestly latency patterns)
    delay_ms = request.headers.get("x-simulate-delay-ms")
    if delay_ms and delay_ms.isdigit():
        delay_sec = int(delay_ms) / 1000.0
        logger.info(f"Simulating network delay: {delay_ms}ms on {request.url.path}")
        await asyncio.sleep(delay_sec)

    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(duration_ms)
    logger.info(f"{request.method} {request.url.path} responded {response.status_code} in {duration_ms}ms")
    return response


# Endpoints
@app.get("/", tags=["System"])
async def root():
    return {
        "service": "E-Commerce Inventory Microservice",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "inventory_list": "/api/v1/inventory",
            "inventory_update": "/api/v1/inventory/update",
            "health": "/api/v1/health"
        }
    }


@app.get("/api/v1/health", tags=["System"])
async def health_check(db: aiosqlite.Connection = Depends(get_db)):
    """Verifies service health and SQLite database connectivity."""
    try:
        async with db.execute("SELECT COUNT(*) FROM inventory") as cursor:
            item_count = (await cursor.fetchone())[0]
        return {
            "status": "healthy",
            "database": "connected",
            "catalog_item_count": item_count
        }
    except Exception as e:
        logger.error(f"Health check failed database check: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connectivity failed."
        )


@app.get("/api/v1/inventory", response_model=List[InventoryItem], tags=["Inventory"])
async def get_all_inventory(db: aiosqlite.Connection = Depends(get_db)):
    """Fetches all inventory records with real-time stock levels."""
    async with db.execute(
        "SELECT id, sku, name, current_stock, reserved_stock, price, created_at, updated_at FROM inventory ORDER BY id ASC"
    ) as cursor:
        rows = await cursor.fetchall()

    items = []
    for r in rows:
        available = max(0, r["current_stock"] - r["reserved_stock"])
        items.append(
            InventoryItem(
                id=r["id"],
                sku=r["sku"],
                name=r["name"],
                current_stock=r["current_stock"],
                reserved_stock=r["reserved_stock"],
                available_stock=available,
                price=r["price"],
                created_at=str(r["created_at"]),
                updated_at=str(r["updated_at"])
            )
        )
    return items


@app.get("/api/v1/inventory/{sku}", response_model=InventoryItem, tags=["Inventory"])
async def get_inventory_by_sku(sku: str, db: aiosqlite.Connection = Depends(get_db)):
    """Fetches details for a specific product SKU."""
    async with db.execute(
        "SELECT id, sku, name, current_stock, reserved_stock, price, created_at, updated_at FROM inventory WHERE sku = ?",
        (sku.strip(),)
    ) as cursor:
        row = await cursor.fetchone()

    if not row:
        raise ItemNotFoundException(sku=sku)

    available = max(0, row["current_stock"] - row["reserved_stock"])
    return InventoryItem(
        id=row["id"],
        sku=row["sku"],
        name=row["name"],
        current_stock=row["current_stock"],
        reserved_stock=row["reserved_stock"],
        available_stock=available,
        price=row["price"],
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"])
    )


@app.post(
    "/api/v1/inventory/update",
    response_model=InventoryUpdateResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": StandardErrorResponse, "description": "SKU not found"},
        422: {"model": StandardErrorResponse, "description": "Validation error or insufficient stock"},
        429: {"model": StandardErrorResponse, "description": "Rate limit exceeded (simulated via Requestly)"},
        500: {"model": StandardErrorResponse, "description": "Upstream error condition"},
    },
    tags=["Inventory"]
)
async def update_inventory_stock(
    payload: InventoryUpdateRequest,
    db: aiosqlite.Connection = Depends(get_db)
):
    """
    Ingests stock updates and atomically adjusts inventory.
    
    Edge-case protections:
    - Rejects negative quantity payloads via Pydantic validator.
    - Rejects malformed SKU format.
    - Rejects deductions exceeding available stock (raises 422 with InsufficientStockException).
    - Transactional write with SQLite isolation.
    """
    logger.info(
        f"Processing inventory update: SKU={payload.sku}, Op={payload.operation}, "
        f"Qty={payload.quantity}, Reason='{payload.reason}'"
    )

    # 1. Fetch current record
    async with db.execute(
        "SELECT id, sku, name, current_stock, reserved_stock FROM inventory WHERE sku = ?",
        (payload.sku,)
    ) as cursor:
        row = await cursor.fetchone()

    if not row:
        logger.warning(f"Inventory update rejected: SKU '{payload.sku}' not found.")
        raise ItemNotFoundException(sku=payload.sku)

    current_stock = row["current_stock"]
    reserved_stock = row["reserved_stock"]
    product_name = row["name"]
    available_stock = max(0, current_stock - reserved_stock)

    # 2. Compute stock mutation
    if payload.operation == "deduct":
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

    elif payload.operation == "restock":
        new_stock = current_stock + payload.quantity

    elif payload.operation == "set":
        new_stock = payload.quantity

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported operation '{payload.operation}'"
        )

    # 3. Commit atomic update
    await db.execute(
        """
        UPDATE inventory
        SET current_stock = ?, updated_at = CURRENT_TIMESTAMP
        WHERE sku = ?
        """,
        (new_stock, payload.sku)
    )
    await db.commit()

    new_available = max(0, new_stock - reserved_stock)
    logger.info(
        f"Stock successfully updated for '{payload.sku}': {current_stock} -> {new_stock} "
        f"(Operation: {payload.operation}, Delta: {payload.quantity})"
    )

    return InventoryUpdateResponse(
        success=True,
        sku=payload.sku,
        product_name=product_name,
        operation=payload.operation,
        quantity_modified=payload.quantity,
        previous_stock=current_stock,
        new_stock=new_stock,
        available_stock=new_available,
        message=f"Stock successfully adjusted for '{payload.sku}' by {payload.quantity} unit(s)."
    )


@app.post(
    "/api/v1/inventory/simulate-upstream",
    tags=["Testing & Requestly Simulation"],
    summary="Simulate upstream ERP/gateway failure states (500 or 429)"
)
async def simulate_upstream_call(
    scenario: Optional[str] = "success",
    db: aiosqlite.Connection = Depends(get_db)
):
    """
    Endpoint designed for validating upstream network fault tolerance.
    Supports scenarios:
    - 'rate_limit' -> raises 429 RateLimitExceededException
    - 'server_error' -> raises 500 UpstreamServiceException
    - 'delay' -> introduces artificial 3000ms delay
    - 'success' -> returns 200 OK
    """
    if scenario == "rate_limit":
        raise RateLimitExceededException(retry_after=45)
    elif scenario == "server_error":
        raise UpstreamServiceException(detail="Upstream ERP inventory sync timed out (HTTP 500).")
    elif scenario == "delay":
        await asyncio.sleep(3.0)
        return {"status": "delayed_response", "latency_simulated_seconds": 3.0}
    
    return {"status": "upstream_connected", "scenario": scenario}
