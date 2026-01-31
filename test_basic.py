#!/usr/bin/env python3
"""
Basic functionality tests for StyleSanctuary
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from backend import database
        from backend import dataset_loader
        from backend.weather import get_weather
        from backend.agent import get_outfit_recommendation
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_database():
    """Test database operations."""
    print("\nTesting database...")
    try:
        from backend.database import (
            init_db, save_outfit, get_saved_outfits, 
            delete_outfit, toggle_favorite
        )
        
        # Initialize database
        init_db()
        print("✓ Database initialized")
        
        # Test save outfit
        outfit_data = {
            'city': 'TestCity',
            'temperature': 20.0,
            'weather_condition': 'Clear',
            'gender': 'Male',
            'event': 'Test Event',
            'style': 'Casual',
            'mood': 'Happy',
            'recommendation': 'Test recommendation',
            'image_urls': ['test1.jpg', 'test2.jpg'],
            'is_favorite': False
        }
        
        outfit_id = save_outfit(outfit_data)
        print(f"✓ Outfit saved with ID: {outfit_id}")
        
        # Test get outfits
        outfits = get_saved_outfits({'limit': 10})
        print(f"✓ Retrieved {len(outfits)} outfit(s)")
        
        # Test toggle favorite
        if outfit_id:
            new_status = toggle_favorite(outfit_id)
            print(f"✓ Toggled favorite status: {new_status}")
        
        # Test delete
        if outfit_id:
            deleted = delete_outfit(outfit_id)
            print(f"✓ Deleted outfit: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dataset_loader():
    """Test dataset loader operations."""
    print("\nTesting dataset loader...")
    try:
        from backend.dataset_loader import (
            load_metadata, filter_outfits, get_random_outfits
        )
        
        # Load metadata
        metadata = load_metadata()
        print(f"✓ Metadata loaded: {metadata.get('total_items', 0)} items")
        
        # Test filtering
        filtered = filter_outfits(gender='Male', limit=5)
        print(f"✓ Filtered outfits: {len(filtered)} results")
        
        # Test random outfits
        random_outfits = get_random_outfits(count=5)
        print(f"✓ Random outfits: {len(random_outfits)} results")
        
        return True
        
    except Exception as e:
        print(f"✗ Dataset loader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from config import WEATHER_API_KEY, OLLAMA_URL, MODEL_NAME, DATASET_SIZE
        
        print(f"✓ Weather API Key configured: {'Yes' if WEATHER_API_KEY else 'No'}")
        print(f"✓ Ollama URL: {OLLAMA_URL}")
        print(f"✓ Model Name: {MODEL_NAME}")
        print(f"✓ Dataset Size: {DATASET_SIZE}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("  StyleSanctuary - Basic Functionality Tests")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Database", test_database),
        ("Dataset Loader", test_dataset_loader),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 60)
    print(f"  Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
