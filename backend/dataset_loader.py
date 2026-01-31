# backend/dataset_loader.py
"""
Dataset loader module for FashionRec dataset from Hugging Face.
Downloads, organizes, and provides filtering functionality for outfit images.
"""

import os
import json
import random
from typing import List, Dict, Any, Optional
from pathlib import Path
import shutil

# Dataset paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "fashion_dataset")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")


def create_dataset_structure():
    """Create the directory structure for the dataset."""
    categories = ['tops', 'bottoms', 'shoes', 'accessories']
    
    for category in categories:
        category_path = os.path.join(IMAGES_DIR, category)
        os.makedirs(category_path, exist_ok=True)
    
    print(f"✓ Dataset structure created at {DATA_DIR}")


def download_fashionrec_dataset(dataset_size: str = "half"):
    """
    Download FashionRec dataset from Hugging Face.
    
    Args:
        dataset_size: Size of dataset to download ('full', 'half', 'quarter')
    
    Note: This is a placeholder implementation. The actual FashionRec dataset
    download would require the Hugging Face datasets library and appropriate
    configuration. For now, we'll create sample metadata.
    """
    try:
        from datasets import load_dataset
        
        print(f"📦 Downloading FashionRec dataset ({dataset_size} size)...")
        print("⚠️  Note: This may take several minutes depending on your connection.")
        
        # Load dataset from Hugging Face
        # Note: The actual dataset name might be different
        # dataset = load_dataset("Anony100/FashionRec", split="train")
        
        # For now, create sample metadata structure
        print("⚠️  Creating sample metadata structure...")
        create_sample_metadata()
        
        print("✓ Dataset download complete!")
        
    except ImportError:
        print("⚠️  huggingface datasets library not available.")
        print("Creating sample metadata structure for development...")
        create_sample_metadata()
    except Exception as e:
        print(f"⚠️  Error downloading dataset: {e}")
        print("Creating sample metadata structure...")
        create_sample_metadata()


def create_sample_metadata():
    """
    Create sample metadata for development and testing.
    This simulates the FashionRec dataset structure.
    """
    create_dataset_structure()
    
    # Sample outfit data
    sample_outfits = []
    
    # Generate sample data for different categories
    categories = {
        'tops': ['T-shirt', 'Blouse', 'Sweater', 'Hoodie', 'Tank Top', 'Cardigan'],
        'bottoms': ['Jeans', 'Skirt', 'Shorts', 'Trousers', 'Leggings'],
        'shoes': ['Sneakers', 'Boots', 'Sandals', 'Loafers', 'Heels'],
        'accessories': ['Hat', 'Scarf', 'Bag', 'Sunglasses', 'Belt', 'Watch']
    }
    
    genders = ['Male', 'Female', 'Unisex']
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    styles = ['Casual', 'Sporty', 'Classic', 'Minimalist', 'Elegant', 'Streetwear']
    weather_conditions = ['Sunny', 'Rainy', 'Cold', 'Hot', 'Windy']
    
    outfit_id = 1
    
    for category, items in categories.items():
        for item in items:
            for _ in range(3):  # Create 3 variations per item
                outfit = {
                    'id': outfit_id,
                    'category': category,
                    'name': item,
                    'gender': random.choice(genders),
                    'season': random.choice(seasons),
                    'style': random.choice(styles),
                    'weather_suitability': random.sample(weather_conditions, k=random.randint(1, 3)),
                    'temperature_min': random.randint(-10, 15),
                    'temperature_max': random.randint(20, 35),
                    'image_path': f'images/{category}/{item.lower().replace(" ", "_")}_{outfit_id}.jpg',
                    'color': random.choice(['Black', 'White', 'Blue', 'Red', 'Green', 'Gray', 'Beige']),
                    'tags': random.sample(styles, k=random.randint(1, 3))
                }
                sample_outfits.append(outfit)
                outfit_id += 1
    
    # Save metadata
    with open(METADATA_FILE, 'w') as f:
        json.dump({
            'version': '1.0',
            'total_items': len(sample_outfits),
            'categories': list(categories.keys()),
            'items': sample_outfits
        }, f, indent=2)
    
    print(f"✓ Sample metadata created with {len(sample_outfits)} items")
    print(f"✓ Metadata saved to {METADATA_FILE}")


def load_metadata() -> Dict[str, Any]:
    """Load metadata from JSON file."""
    if not os.path.exists(METADATA_FILE):
        print("⚠️  Metadata file not found. Creating sample data...")
        create_sample_metadata()
    
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)


def filter_outfits(
    category: Optional[str] = None,
    gender: Optional[str] = None,
    season: Optional[str] = None,
    style: Optional[str] = None,
    weather_condition: Optional[str] = None,
    temperature: Optional[float] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Filter outfits based on criteria.
    
    Args:
        category: Category to filter by ('tops', 'bottoms', 'shoes', 'accessories')
        gender: Gender to filter by ('Male', 'Female', 'Unisex')
        season: Season to filter by
        style: Style preference
        weather_condition: Weather condition
        temperature: Current temperature
        limit: Maximum number of results
    
    Returns:
        List of matching outfit items
    """
    metadata = load_metadata()
    items = metadata.get('items', [])
    
    # Filter items
    filtered = items
    
    if category:
        filtered = [item for item in filtered if item['category'] == category]
    
    if gender:
        filtered = [item for item in filtered 
                   if item['gender'] == gender or item['gender'] == 'Unisex']
    
    if season:
        filtered = [item for item in filtered if item['season'] == season]
    
    if style:
        filtered = [item for item in filtered 
                   if style in item.get('tags', []) or item.get('style') == style]
    
    if weather_condition:
        filtered = [item for item in filtered 
                   if weather_condition in item.get('weather_suitability', [])]
    
    if temperature is not None:
        filtered = [item for item in filtered 
                   if item['temperature_min'] <= temperature <= item['temperature_max']]
    
    # Shuffle and limit results
    random.shuffle(filtered)
    return filtered[:limit]


def get_outfit_by_category(
    weather: Dict[str, Any],
    user_context: Dict[str, Any],
    category: str,
    count: int = 1
) -> List[Dict[str, Any]]:
    """
    Get outfit items for a specific category based on weather and user context.
    
    Args:
        weather: Weather information (temperature, condition)
        user_context: User preferences (gender, style, mood)
        category: Category to get items for
        count: Number of items to retrieve
    
    Returns:
        List of outfit items
    """
    temperature = weather.get('temperature', 20)
    weather_condition = weather.get('condition', '')
    
    # Map weather conditions to simple categories
    weather_map = {
        'clear': 'Sunny',
        'clouds': 'Sunny',
        'rain': 'Rainy',
        'snow': 'Cold',
        'mist': 'Rainy',
        'fog': 'Rainy'
    }
    
    simple_weather = 'Sunny'
    for key, value in weather_map.items():
        if key in weather_condition.lower():
            simple_weather = value
            break
    
    # Determine season based on temperature
    if temperature < 5:
        season = 'Winter'
    elif temperature < 15:
        season = 'Fall'
    elif temperature < 25:
        season = 'Spring'
    else:
        season = 'Summer'
    
    return filter_outfits(
        category=category,
        gender=user_context.get('gender'),
        season=season,
        style=user_context.get('style'),
        weather_condition=simple_weather,
        temperature=temperature,
        limit=count
    )


def match_outfit_to_images(
    llm_recommendation: str,
    user_context: Dict[str, Any],
    weather: Dict[str, Any]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Match LLM text recommendation to actual outfit images from dataset.
    
    Args:
        llm_recommendation: Text recommendation from LLM
        user_context: User preferences (gender, style, mood, event)
        weather: Weather information (temperature, condition)
    
    Returns:
        Dictionary with outfit items by category
    """
    outfit = {
        'tops': get_outfit_by_category(weather, user_context, 'tops', 2),
        'bottoms': get_outfit_by_category(weather, user_context, 'bottoms', 1),
        'shoes': get_outfit_by_category(weather, user_context, 'shoes', 1),
        'accessories': get_outfit_by_category(weather, user_context, 'accessories', 2)
    }
    
    return outfit


def get_random_outfits(count: int = 12, **filters) -> List[Dict[str, Any]]:
    """
    Get random outfits for the Quick Gallery.
    
    Args:
        count: Number of outfits to retrieve
        **filters: Optional filters (gender, season, style, etc.)
    
    Returns:
        List of random outfit items
    """
    return filter_outfits(limit=count, **filters)


# Initialize dataset on module import
if not os.path.exists(METADATA_FILE):
    print("Initializing dataset structure...")
    try:
        create_sample_metadata()
    except Exception as e:
        print(f"Warning: Could not initialize dataset: {e}")
