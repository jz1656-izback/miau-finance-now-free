"""Pawdentity seed — idempotently create the admin user for development/staging.

Usage:
    python -m app.seed_admin              # uses configured DATABASE_URL
    DATABASE_URL=postgresql+asyncpg://miau:pass@localhost:5434/miau python -m app.seed_admin

🔒 SECURITY (V7-001/C1): This creates a REAL database user with bcrypt-hashed
password (NOT a hardcoded code backdoor). The password is a published demo
credential — change it before production use.
"""
import asyncio
import os
import sys

# Ensure we can import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

ADMIN_USER = "pawdmin"
ADMIN_PASS = "miau2026"
ADMIN_EMAIL = "admin@miau.finance"
ADMIN_ROLE = "admin"


async def seed_admin():
    """Idempotently create the admin user if it doesn't exist."""
    # Build connection string: prefer explicit env, fall back to config
    database_url = os.environ.get(
        "DATABASE_URL",
        f"postgresql+asyncpg://miau:miau_dev_password@localhost:5434/miau",
    )

    engine = create_async_engine(
        database_url,
        pool_size=1,
        max_overflow=0,
        echo=False,
        connect_args={"timeout": 10, "ssl": False},
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # Check if admin already exists
        result = await session.execute(
            text("SELECT id, username, role FROM users WHERE username = :username"),
            {"username": ADMIN_USER},
        )
        existing = result.mappings().first()

        if existing:
            print(f"✅ Admin user '{ADMIN_USER}' already exists (role: {existing['role']})")
            return existing["id"]

        # Create admin user
        password_hash = bcrypt.hashpw(ADMIN_PASS.encode(), bcrypt.gensalt()).decode()
        from uuid import uuid4
        user_id = uuid4()

        await session.execute(
            text("""
                INSERT INTO users (id, username, email, password_hash, role)
                VALUES (:id, :username, :email, :password_hash, :role)
            """),
            {
                "id": user_id,
                "username": ADMIN_USER,
                "email": ADMIN_EMAIL,
                "password_hash": password_hash,
                "role": ADMIN_ROLE,
            },
        )
        await session.commit()
        print(f"✅ Created admin user '{ADMIN_USER}' (id: {user_id})")
        return user_id


if __name__ == "__main__":
    asyncio.run(seed_admin())
