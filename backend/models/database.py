"""
MongoDB database configuration using Motor (async driver)
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB Atlas"""
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is not set")

        cls.client = AsyncIOMotorClient(mongodb_uri)
        cls.db = cls.client.get_database("cv_wizard")

        # Create indexes
        await cls.create_indexes()

        print("✅ Connected to MongoDB Atlas")

    @classmethod
    async def create_indexes(cls):
        """Create database indexes"""
        if cls.db is None:
            return

        cv_sessions = cls.db.cv_sessions

        # Create unique index on session_id
        await cv_sessions.create_index("session_id", unique=True)

        # Create TTL index on created_at (24 hours)
        await cv_sessions.create_index(
            "created_at",
            expireAfterSeconds=86400,  # 24 hours
        )

        # Create index on file_hash for duplicate detection
        await cv_sessions.create_index("file_hash")

        print("✅ Database indexes created")

    @classmethod
    async def close_db(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()
            print("❌ Disconnected from MongoDB")

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if cls.db is None:
            raise RuntimeError("Database not connected. Call connect_db() first.")
        return cls.db


# Helper functions for CV sessions
async def create_cv_session(session_data: dict) -> dict:
    """Create a new CV session"""
    db = Database.get_database()

    # Set expiration time (24 hours from now)
    session_data["created_at"] = datetime.utcnow()
    session_data["expires_at"] = datetime.utcnow() + timedelta(hours=24)

    result = await db.cv_sessions.insert_one(session_data)
    session_data["_id"] = str(result.inserted_id)

    return session_data


async def get_cv_session(session_id: str) -> Optional[dict]:
    """Get CV session by session ID"""
    db = Database.get_database()
    session = await db.cv_sessions.find_one({"session_id": session_id})

    if session:
        session["_id"] = str(session["_id"])

    return session


async def update_cv_session(session_id: str, update_data: dict) -> bool:
    """Update CV session"""
    db = Database.get_database()
    result = await db.cv_sessions.update_one(
        {"session_id": session_id}, {"$set": update_data}
    )

    return result.modified_count > 0


async def delete_cv_session(session_id: str) -> bool:
    """Delete CV session"""
    db = Database.get_database()
    result = await db.cv_sessions.delete_one({"session_id": session_id})

    return result.deleted_count > 0


async def check_duplicate_file(file_hash: str) -> Optional[dict]:
    """Check if file with same hash already exists"""
    db = Database.get_database()
    session = await db.cv_sessions.find_one({"file_hash": file_hash})

    if session:
        session["_id"] = str(session["_id"])

    return session
