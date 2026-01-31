#!/usr/bin/env python3
"""
Initial setup script for StyleSanctuary
- Creates necessary directories
- Initializes database
- Sets up dataset cache
- Checks environment configuration
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary directories for the application"""
    print("📁 Creating directory structure...")
    
    directories = [
        "data",
        "data/fashion_dataset",
        "assets",
        "backend"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {directory}")
    
    print("✅ Directories created successfully!\n")


def setup_database():
    """Initialize the SQLite database"""
    print("🗄️  Setting up database...")
    
    try:
        from backend.database import OutfitDatabase
        
        db = OutfitDatabase()
        print("   ✓ Database initialized at data/user_history.db")
        print("✅ Database setup complete!\n")
        return True
    except Exception as e:
        print(f"   ❌ Database setup failed: {e}\n")
        return False


def setup_dataset():
    """Initialize the fashion dataset"""
    print("📦 Setting up fashion dataset...")
    
    try:
        from backend.dataset_loader import FashionDatasetLoader
        
        loader = FashionDatasetLoader()
        print(f"   ✓ Dataset initialized with {len(loader.dataset)} items")
        print("✅ Dataset setup complete!\n")
        return True
    except Exception as e:
        print(f"   ❌ Dataset setup failed: {e}\n")
        return False


def check_env_file():
    """Check if .env file exists and guide user"""
    print("🔑 Checking environment configuration...")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        print("   ⚠️  .env file not found")
        
        if env_example_path.exists():
            print("   ℹ️  Copy .env.example to .env and configure your API keys:")
            print("      cp .env.example .env")
        else:
            print("   ℹ️  Create a .env file with your API keys")
        
        print("\n   Required environment variables:")
        print("   - WEATHER_API_KEY: Your OpenWeatherMap API key")
        print("   - OLLAMA_URL: Ollama API endpoint (default: http://localhost:11434/api/generate)")
        print("   - MODEL_NAME: Ollama model name (default: qwen2.5:7b-instruct)")
        print()
    else:
        print("   ✓ .env file found")
        
        # Try to load and validate
        try:
            from config import WEATHER_API_KEY, OLLAMA_URL, MODEL_NAME
            
            if WEATHER_API_KEY and WEATHER_API_KEY != "your_api_key_here":
                print("   ✓ WEATHER_API_KEY is configured")
            else:
                print("   ⚠️  WEATHER_API_KEY needs to be configured")
            
            print(f"   ✓ OLLAMA_URL: {OLLAMA_URL}")
            print(f"   ✓ MODEL_NAME: {MODEL_NAME}")
            
        except Exception as e:
            print(f"   ⚠️  Error loading config: {e}")
    
    print("✅ Environment check complete!\n")


def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        "streamlit",
        "requests",
        "dotenv",
        "PIL",
        "pandas"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "dotenv":
                __import__("dotenv")
            elif package == "PIL":
                __import__("PIL")
            else:
                __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ❌ {package} not found")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   ⚠️  Missing packages detected!")
        print(f"   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed!\n")
        return True


def main():
    """Run all setup steps"""
    print("\n" + "=" * 60)
    print("   StyleSanctuary Setup")
    print("   Modern AI-Powered Outfit Recommendation App")
    print("=" * 60 + "\n")
    
    # Create directories
    create_directories()
    
    # Check dependencies
    deps_ok = check_dependencies()
    if not deps_ok:
        print("\n⚠️  Please install dependencies first:")
        print("   pip install -r requirements.txt\n")
        sys.exit(1)
    
    # Setup database
    db_ok = setup_database()
    
    # Setup dataset
    dataset_ok = setup_dataset()
    
    # Check environment
    check_env_file()
    
    # Final message
    print("=" * 60)
    if db_ok and dataset_ok:
        print("✅ Setup completed successfully!")
        print("\n🚀 You can now start the application:")
        print("   streamlit run app.py")
        print("\n📖 Or use the CLI version:")
        print("   python main.py")
    else:
        print("⚠️  Setup completed with some warnings.")
        print("   Please check the messages above and fix any issues.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
