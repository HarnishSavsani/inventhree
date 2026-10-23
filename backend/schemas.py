"""
Pydantic schemas and custom validation rules for e-commerce inventory management.
Handles strict SKU format validation and prevents negative or invalid stock payloads.
"""

from datetime import datetime, timezone
import re
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


# Regular expression for valid SKU format: uppercase alphanumeric segments separated by hyphens
# Supports e.g. PROD-1001-BLK, SKU-4920-XL, ELEC-900-MAX, PROD-9999-NONE
SKU_PATTERN = re.compile(r"^[A-Z0-9]{2,8}(-[A-Z0-9]{2,10})+$")


class InventoryItemBase(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit (SKU) identifier", json_schema_extra={"example": "PROD-1001-BLK"})
    name: str = Field(..., description="Display name of the product", json_schema_extra={"example": "Ultra Wireless Headphones - Matte Black"})
    current_stock: int = Field(..., ge=0, description="Total physical inventory in warehouse", json_schema_extra={"example": 50})
    reserved_stock: int = Field(default=0, ge=0, description="Stock reserved for pending checkouts", json_schema_extra={"example": 0})
    price: float = Field(default=0.0, ge=0.0, description="Unit retail price in USD", json_schema_extra={"example": 149.99})

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("SKU cannot be empty or whitespace only.")
        if not SKU_PATTERN.match(trimmed):
            raise ValueError(
                f"Malformed SKU format '{v}'. Expected uppercase alphanumeric segments separated by hyphens, e.g., 'PROD-1001-BLK' or 'ELEC-200-WHT'."
            )
        return trimmed


class InventoryItem(InventoryItemBase):
    id: int = Field(..., description="Primary database identifier")
    available_stock: int = Field(..., description="Stock immediately available for purchase (current_stock - reserved_stock)")
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class InventoryUpdateRequest(BaseModel):
    """
    Payload for POST /api/v1/inventory/update.
    Validates SKU pattern, prevents negative stock updates, and restricts edge-case deductions.
    """
    sku: str = Field(
        ...,
        description="Target Product SKU identifier",
        json_schema_extra={"example": "PROD-1001-BLK"}
    )
    quantity: int = Field(
        ...,
        description="Amount to adjust or deduct. Must be a positive integer for deduct/restock.",
        json_schema_extra={"example": 5}
    )
    operation: Literal["deduct", "restock", "set"] = Field(
        default="deduct",
        description="Inventory operation type: 'deduct' (default), 'restock', or 'set'"
    )
    reason: Optional[str] = Field(
        default="Order fulfillment checkout",
        max_length=255,
        description="Audit reason for stock modification"
    )
    reference_id: Optional[str] = Field(
        default=None,
        description="Optional upstream order ID or batch tracking number",
        json_schema_extra={"example": "ORD-2026-98124"}
    )

    @field_validator("sku")
    @classmethod
    def validate_sku_format(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("SKU cannot be empty.")
        if not SKU_PATTERN.match(trimmed):
            raise ValueError(
                f"Malformed SKU '{v}'. Must match standard pattern '^[A-Z0-9]{{2,8}}(-[A-Z0-9]{{2,10}})+$', e.g., 'PROD-1001-BLK'."
            )
        return trimmed

    @field_validator("quantity")
    @classmethod
    def validate_quantity_bounds(cls, v: int) -> int:
        if v < 0:
            raise ValueError(
                f"Invalid quantity '{v}'. Negative stock count values are forbidden in update payloads. Specify positive quantity and choose operation 'deduct' or 'restock'."
            )
        return v

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


class InventoryUpdateResponse(BaseModel):
    """Successful inventory update transaction response."""
    success: bool = True
    sku: str
    product_name: str
    operation: str
    quantity_modified: int
    previous_stock: int
    new_stock: int
    available_stock: int
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    message: str


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: str


class StandardErrorResponse(BaseModel):
    """Standardized API error envelope for frontend consumption."""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
