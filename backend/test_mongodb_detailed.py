#!/usr/bin/env python3
"""
Detailed MongoDB connection test to diagnose issues
"""

import asyncio
import os
import sys
from urllib.parse import quote_plus

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_connection():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient

        mongodb_uri = os.getenv("MONGODB_URI")

        if not mongodb_uri:
            print("❌ MONGODB_URI not found in .env file")
            return False

        print("Testing MongoDB connection...")
        print(f"URI (first 30 chars): {mongodb_uri[:30]}...")
        print()

        # Test connection with detailed error handling
        try:
            print("1. Creating MongoDB client...")
            client = AsyncIOMotorClient(
                mongodb_uri,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
            )

            print("2. Attempting to ping MongoDB server...")
            result = await client.admin.command("ping")

            print("3. Connection successful!")
            print(f"   Ping result: {result}")

            print("\n4. Listing databases...")
            db_list = await client.list_database_names()
            print(f"   Available databases: {db_list}")

            client.close()
            print("\n✅ All MongoDB tests passed!")
            return True

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)

            print(f"\n❌ Connection failed!")
            print(f"   Error type: {error_type}")
            print(f"   Error message: {error_msg}")
            print()

            # Provide specific guidance based on error
            if "Authentication failed" in error_msg:
                print("💡 Suggestion: Check your username and password")
                print("   - Make sure credentials are correct")
                print("   - Verify database user exists in MongoDB Atlas")

            elif "quote_plus" in error_msg or "RFC 3986" in error_msg:
                print("💡 Suggestion: Your password contains special characters")
                print("   Run: python encode_mongodb_uri.py")
                print("   Then update your .env file with the encoded URI")

            elif "Network" in error_msg or "Timeout" in error_msg:
                print("💡 Suggestion: Network/firewall issue")
                print("   - Check MongoDB Atlas network access settings")
                print("   - Add your IP address (or 0.0.0.0/0 for testing)")
                print("   - Verify cluster is running")

            elif "DNS" in error_msg:
                print("💡 Suggestion: DNS resolution failed")
                print("   - Check your cluster address")
                print("   - Verify internet connection")

            else:
                print("💡 Suggestion: General connection issue")
                print("   - Verify MONGODB_URI in .env file")
                print("   - Check MongoDB Atlas cluster status")

            return False

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Run: pip install motor pymongo dnspython")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)
