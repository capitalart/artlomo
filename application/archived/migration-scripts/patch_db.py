#!/usr/bin/env python3
"""
One-time database migration script to add missing columns to the users table.
Run this script once to align the SQLite database with the User model.

Usage: python3 patch_db.py
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

# Determine database path - check multiple locations
def find_db_path() -> Path:
    candidates = [
        Path("/srv/artlomo/var/db/artlomo.sqlite3"),
        Path("/srv/artlomo/data/artlomo.sqlite3"),
        Path("/srv/artlomo/application/database/users.db"),
    ]
    for p in candidates:
        if p.exists():
            return p
    # Fallback to db.py import
    try:
        from db import DB_PATH
        return DB_PATH
    except Exception:
        pass
    return candidates[0]  # Default

DB_PATH = find_db_path()


def get_existing_columns(cursor: sqlite3.Cursor, table: str) -> set[str]:
    """Get the set of existing column names for a table."""
    cursor.execute(f"PRAGMA table_info({table})")
    return {row[1] for row in cursor.fetchall()}


def migrate_users_table(db_path: Path) -> None:
    """Add missing columns to the users table."""
    print(f"[patch_db] Connecting to database: {db_path}")
    
    if not db_path.exists():
        print(f"[patch_db] Database does not exist. It will be created on first app run.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        existing = get_existing_columns(cursor, "users")
        print(f"[patch_db] Existing columns in 'users': {sorted(existing)}")
        
        migrations = []
        
        # Check and add 'email' column (without UNIQUE - SQLite limitation)
        if "email" not in existing:
            migrations.append(("email", "ALTER TABLE users ADD COLUMN email TEXT"))
            print("[patch_db] Will add column: email")
        
        # Check and add 'role' column
        if "role" not in existing:
            migrations.append(("role", "ALTER TABLE users ADD COLUMN role VARCHAR(32) NOT NULL DEFAULT 'artist'"))
            print("[patch_db] Will add column: role")
        
        # Check and add 'created_at' column
        if "created_at" not in existing:
            migrations.append(("created_at", "ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            print("[patch_db] Will add column: created_at")
        
        if not migrations:
            print("[patch_db] All required columns already exist. No migration needed.")
            return
        
        # Run migrations
        for col_name, sql in migrations:
            print(f"[patch_db] Running: {sql}")
            cursor.execute(sql)
        
        conn.commit()
        print(f"[patch_db] Successfully added {len(migrations)} column(s).")
        
        # Set default role for any existing users with NULL role
        cursor.execute("UPDATE users SET role = 'artist' WHERE role IS NULL")
        affected = cursor.rowcount
        if affected > 0:
            conn.commit()
            print(f"[patch_db] Set default role='artist' for {affected} existing user(s).")
        
        # Verify final schema
        final_columns = get_existing_columns(cursor, "users")
        print(f"[patch_db] Final columns in 'users': {sorted(final_columns)}")
        
    except Exception as e:
        print(f"[patch_db] ERROR: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    print("[patch_db] Starting database migration...")
    migrate_users_table(DB_PATH)
    print("[patch_db] Migration complete.")
