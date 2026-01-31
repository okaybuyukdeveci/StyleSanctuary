# backend/dataset_loader.py
import os
import json
import random
from typing import List, Dict, Optional
from pathlib import Path


class FashionDatasetLoader:
    """
    Manages FashionRec dataset from Hugging Face
    
    Loads real FashionRec dataset from HuggingFace or falls back to mock data if unavailable.
    """
    
    def __init__(self, cache_dir: str = "data/fashion_dataset"):
        """
        Initialize the dataset loader
        
        Args:
            cache_dir: Directory to cache dataset files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.dataset = None
        
        # Load FashionRec dataset
        self.dataset = self._load_fashionrec_dataset()
    
    def _load_fashionrec_dataset(self):
        """Load FashionRec dataset from HuggingFace (only half of it)"""
        cache_file = self.cache_dir / "fashionrec_cache.json"
        
        # Check if cached version exists
        if cache_file.exists():
            print("📦 Loading cached FashionRec dataset...")
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                print(f"✅ Loaded {len(data)} items from cache")
                return data
            except Exception as e:
                print(f"⚠️  Error loading cache: {e}")
        
        print("🌐 Downloading FashionRec dataset from HuggingFace...")
        try:
            from datasets import load_dataset
            
            # Load only the train split (smaller portion - 50%)
            dataset = load_dataset("Anony100/FashionRec", split="train[:50%]")
            
            # Convert to list of dicts
            processed_data = []
            for idx, item in enumerate(dataset):
                processed_item = {
                    "id": f"fashionrec_{idx}",
                    "title": item.get("product_name", f"Outfit {idx}"),
                    "image_url": item.get("image", ""),
                    "category": item.get("category", "casual"),
                    "gender": item.get("gender", "unisex"),
                    "season": self._infer_season(item),
                    "style": item.get("style", "casual"),
                    "color": item.get("color", "neutral"),
                    "tags": item.get("tags", [])
                }
                processed_data.append(processed_item)
            
            # Cache for future use
            with open(cache_file, 'w') as f:
                json.dump(processed_data, f)
            
            print(f"✅ Loaded {len(processed_data)} items from FashionRec dataset")
            return processed_data
            
        except Exception as e:
            print(f"❌ Error loading FashionRec dataset: {e}")
            print("⚠️  Falling back to mock data...")
            return self._generate_mock_data()
    
    def _infer_season(self, item):
        """Infer season from item metadata"""
        category = item.get("category", "").lower()
        tags = str(item.get("tags", "")).lower()
        
        if any(word in category or word in tags for word in ["summer", "short", "tank", "sandal"]):
            return "summer"
        elif any(word in category or word in tags for word in ["winter", "coat", "jacket", "boot"]):
            return "winter"
        elif any(word in category or word in tags for word in ["spring", "light"]):
            return "spring"
        elif any(word in category or word in tags for word in ["fall", "autumn"]):
            return "fall"
        return "all-season"
    
    def _generate_mock_data(self) -> List[Dict]:
        """Create mock fashion dataset for demonstration (fallback)"""
        styles = ["Casual", "Formal", "Sporty", "Chic", "Classic"]
        seasons = ["spring", "summer", "fall", "winter"]
        genders = ["male", "female", "unisex"]
        categories = ["top", "bottom", "shoes", "accessories", "outfit"]
        
        # Mock image URLs (using placeholder images)
        base_url = "https://via.placeholder.com/300x400"
        
        dataset = []
        for i in range(500):
            item = {
                "id": f"mock_{i}",
                "title": f"Fashion Item {i+1}",
                "image_url": f"{base_url}/CCCCCC/666666?text=Item+{i+1}",
                "category": random.choice(categories),
                "style": random.choice(styles),
                "season": random.choice(seasons),
                "gender": random.choice(genders),
                "color": random.choice(["Black", "White", "Blue", "Red", "Green", "Gray", "Brown"]),
                "tags": random.sample(["comfortable", "trendy", "elegant", "sporty", "casual", "formal"], k=2)
            }
            dataset.append(item)
        
        return dataset
    
    def download_dataset(self, split: str = "train", limit: int = 500):
        """
        Download dataset from Hugging Face (compatibility method)
        
        Args:
            split: Dataset split to download
            limit: Number of items to download
        """
        print(f"📦 Dataset ready with {len(self.dataset)} items")
        return self.dataset
    
    def get_random_outfits(self, 
                          gender: Optional[str] = None, 
                          season: Optional[str] = None, 
                          style: Optional[str] = None, 
                          count: int = 12) -> List[Dict]:
        """
        Get random outfit recommendations with optional filtering
        
        Args:
            gender: Filter by gender (male/female/unisex)
            season: Filter by season (spring/summer/fall/winter)
            style: Filter by style (Casual/Formal/Sporty/Chic)
            count: Number of outfits to return
            
        Returns:
            List of outfit dictionaries
        """
        filtered = self.dataset.copy()
        
        # Apply filters (case-insensitive)
        if gender and gender.lower() != "unisex":
            filtered = [item for item in filtered 
                       if item['gender'].lower() in [gender.lower(), "unisex"]]
        
        if season:
            filtered = [item for item in filtered 
                       if item['season'].lower() in [season.lower(), "all-season"]]
        
        if style:
            filtered = [item for item in filtered 
                       if style.lower() in item['style'].lower()]
        
        # Return random selection
        if len(filtered) > count:
            return random.sample(filtered, count)
        return filtered
    
    def get_matching_images(self, llm_recommendation: str) -> Dict[str, Dict]:
        """
        Find matching images from dataset based on LLM recommendation
        
        Args:
            llm_recommendation: Text recommendation from LLM
            
        Returns:
            Dictionary with image data for different clothing types
        """
        # Parse the recommendation text for clothing types
        recommendation_lower = llm_recommendation.lower()
        
        result = {}
        
        # Find upper garment
        upper_items = [item for item in self.dataset if 'upper' in item['category'].lower() or 'top' in item['category'].lower()]
        if upper_items:
            result['upper'] = random.choice(upper_items)
        
        # Find lower garment
        lower_items = [item for item in self.dataset if 'lower' in item['category'].lower() or 'bottom' in item['category'].lower()]
        if lower_items:
            result['lower'] = random.choice(lower_items)
        
        # Find shoes
        shoes_items = [item for item in self.dataset if 'shoe' in item['category'].lower()]
        if shoes_items:
            result['shoes'] = random.choice(shoes_items)
        
        # Find accessories
        accessories_items = [item for item in self.dataset if 'accessor' in item['category'].lower()]
        if accessories_items:
            result['accessories'] = random.choice(accessories_items)
        
        return result
    
    def get_items_by_category(self, category: str, weather_temp: Optional[float] = None, count: int = 5) -> List[Dict]:
        """
        Get items by category (tops, bottoms, shoes, accessories)
        
        Args:
            category: Category to filter by
            weather_temp: Optional temperature for weather-based filtering
            count: Number of items to return
            
        Returns:
            List of matching items
        """
        # Filter by category
        filtered = [item for item in self.dataset 
                   if category.lower() in item["category"].lower()]
        
        # Weather-based filtering
        if weather_temp is not None:
            if weather_temp < 10:  # Cold
                filtered = [item for item in filtered 
                           if item["season"].lower() in ["winter", "fall", "all-season"]]
            elif weather_temp > 25:  # Hot
                filtered = [item for item in filtered 
                           if item["season"].lower() in ["summer", "spring", "all-season"]]
        
        # Return random selection
        if len(filtered) > count:
            return random.sample(filtered, count)
        return filtered
    
    def search_outfits(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search outfits by query string with optional filters
        
        Args:
            query: Search query
            filters: Optional filter dictionary
            
        Returns:
            List of matching outfits
        """
        query_lower = query.lower()
        results = []
        
        for item in self.dataset:
            # Simple search in title and tags
            if (query_lower in item['title'].lower() or 
                any(query_lower in tag.lower() for tag in item['tags'])):
                results.append(item)
        
        # Apply additional filters if provided
        if filters:
            if filters.get('gender'):
                results = [item for item in results if item['gender'] == filters['gender']]
            if filters.get('season'):
                results = [item for item in results if item['season'] == filters['season']]
            if filters.get('style'):
                results = [item for item in results if item['style'] == filters['style']]
        
        return results
    
    def get_outfit_by_weather(self, temperature: float, condition: str) -> List[Dict]:
        """
        Get outfit recommendations based on weather conditions
        
        Args:
            temperature: Temperature in Celsius
            condition: Weather condition description
            
        Returns:
            List of appropriate outfit items
        """
        # Determine appropriate season based on temperature
        if temperature <= 5:
            season = "winter"
        elif temperature <= 15:
            season = "fall"
        elif temperature <= 25:
            season = "spring"
        else:
            season = "summer"
        
        return self.get_random_outfits(season=season, count=12)
