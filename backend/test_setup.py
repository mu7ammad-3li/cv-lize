"""
Quick setup test to verify all components are working
Run this after installation to check if everything is configured correctly
"""

import sys


def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")

    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("motor", "Motor (MongoDB async driver)"),
        ("pydantic", "Pydantic"),
        ("spacy", "spaCy"),
        ("pdfplumber", "pdfplumber"),
        ("openai", "OpenAI (OpenRouter compatible)"),
        ("slowapi", "SlowAPI (rate limiting)"),
        ("dotenv", "python-dotenv"),
    ]

    failed = []
    for package, name in packages:
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            failed.append(package)

    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n✅ All packages installed!")
    return True


def test_spacy_model():
    """Test if spaCy model is downloaded"""
    print("\nTesting spaCy model...")

    try:
        import spacy

        try:
            nlp = spacy.load("en_core_web_md")
            print("  ✅ en_core_web_md model loaded")
            return True
        except OSError:
            try:
                nlp = spacy.load("en_core_web_sm")
                print("  ⚠️  Using en_core_web_sm (smaller model)")
                print(
                    "  💡 For better results, run: python -m spacy download en_core_web_md"
                )
                return True
            except OSError:
                print("  ❌ No spaCy model found")
                print("  Run: python -m spacy download en_core_web_md")
                return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\nTesting environment configuration...")

    import os
    from pathlib import Path

    env_file = Path(".env")

    if not env_file.exists():
        print("  ❌ .env file not found")
        print("  Run: cp .env.example .env")
        print("  Then edit .env with your credentials")
        return False

    print("  ✅ .env file exists")

    # Load env file
    from dotenv import load_dotenv

    load_dotenv()

    required_vars = ["MONGODB_URI", "OPENROUTER_API_KEY"]

    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if (
            not value
            or value.startswith("your-")
            or value.startswith("your_")
            or value == ""
        ):
            print(f"  ❌ {var} not configured")
            missing.append(var)
        else:
            # Mask the value for security
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"  ✅ {var}: {masked}")

    if missing:
        print(f"\n⚠️  Please configure: {', '.join(missing)}")
        return False

    return True


def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\nTesting MongoDB connection...")

    try:
        import asyncio
        import os

        from motor.motor_asyncio import AsyncIOMotorClient

        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri or mongodb_uri.startswith("mongodb+srv://username:password"):
            print("  ⚠️  MongoDB URI not configured, skipping connection test")
            return True

        async def test_connection():
            try:
                client = AsyncIOMotorClient(mongodb_uri, serverSelectionTimeoutMS=5000)
                await client.admin.command("ping")
                client.close()
                return True
            except Exception as e:
                print(f"  ❌ Connection failed: {e}")
                return False

        result = asyncio.run(test_connection())
        if result:
            print("  ✅ MongoDB connection successful")
        return result
    except Exception as e:
        print(f"  ❌ Error testing connection: {e}")
        return False


def test_openrouter_api():
    """Test OpenRouter API key"""
    print("\nTesting OpenRouter API...")

    try:
        import os

        from openai import AsyncOpenAI

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or api_key.startswith("your-"):
            print("  ⚠️  OpenRouter API key not configured, skipping API test")
            return True

        try:
            client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            # Don't actually call the API to avoid using quota
            print("  ✅ OpenRouter API configured")
            model = os.getenv(
                "OPENROUTER_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct"
            )
            print(f"  ✅ Using model: {model}")
            return True
        except Exception as e:
            print(f"  ❌ OpenRouter API error: {e}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("CV Wizard - Backend Setup Test")
    print("=" * 60)

    tests = [
        ("Package imports", test_imports),
        ("spaCy model", test_spacy_model),
        ("Environment configuration", test_env_file),
        ("MongoDB connection", test_mongodb_connection),
        ("OpenRouter API", test_openrouter_api),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test failed with error: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All tests passed! You're ready to run the backend.")
        print("\nNext steps:")
        print("  1. Run: python main.py")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Test the API with a CV file")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
