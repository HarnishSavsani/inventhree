"""
Database module for asynchronous SQLite inventory storage.
Uses aiosqlite for non-blocking database queries.
"""

import os
import aiosqlite
from typing import AsyncGenerator

DB_PATH = os.path.join(os.path.dirname(__file__), "inventory.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    current_stock INTEGER NOT NULL CHECK(current_stock >= 0),
    reserved_stock INTEGER NOT NULL DEFAULT 0 CHECK(reserved_stock >= 0),
    price REAL NOT NULL DEFAULT 0.0 CHECK(price >= 0.0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_inventory_sku ON inventory(sku);
"""

SEED_PRODUCTS = [
    ("PROD-1001-BLK", "Ultra Wireless Headphones - Matte Black", 50, 0, 149.99),
    ("PROD-1002-WHT", "Ultra Wireless Headphones - Arctic White", 25, 0, 149.99),
    ("PROD-2005-RGB", "Ergonomic Mechanical Keyboard - RGB", 15, 2, 89.50),
    ("PROD-3040-USC", "65W GaN USB-C Fast Charger", 100, 5, 29.99),
    ("PROD-4099-PRO", "Smart Fitness Tracker v2 - Onyx", 8, 0, 79.95),
    ("PROD-5500-LMT", "Limited Edition Cyberpunk Mousepad", 3, 1, 34.00),
    ("PROD-9999-OUT", "Legacy USB 2.0 Optical Mouse", 0, 0, 12.50)
]


async def init_db():
    """Initialize database tables and seed sample catalog if empty."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA_SQL)
        
        # Check if table already has records
        async with db.execute("SELECT COUNT(*) FROM inventory") as cursor:
            count = (await cursor.fetchone())[0]
            
        if count == 0:
            await db.executemany(
                """
                INSERT INTO inventory (sku, name, current_stock, reserved_stock, price)
                VALUES (?, ?, ?, ?, ?)
                """,
                SEED_PRODUCTS
            )
            await db.commit()


async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Dependency for obtaining an asynchronous database connection."""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()
