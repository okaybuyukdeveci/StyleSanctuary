# backend/dataset_loader.py
import os
import json
import random
from typing import List, Dict, Optional
import pickle


class FashionDatasetLoader:
    """
    Manages FashionRec dataset from Hugging Face
    
    Note: This is a simplified implementation that uses mock data.
    For production, integrate with Hugging Face datasets library.
    """
    
    def __init__(self, cache_dir: str = "data/fashion_dataset"):
        """
        Initialize the dataset loader
        
        Args:
            cache_dir: Directory to cache dataset files
        """
        self.cache_dir = cache_dir
        self.dataset = None
        self.cache_file = os.path.join(cache_dir, "dataset_cache.pkl")
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load or create mock dataset
        self._load_or_create_dataset()
    
    def _load_or_create_dataset(self):
        """Load cached dataset or create mock data"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    self.dataset = pickle.load(f)
                return
            except Exception as e:
                print(f"Error loading cache: {e}")
        
        # Create mock dataset
        self.dataset = self._create_mock_dataset()
        
        # Save to cache
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.dataset, f)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def _create_mock_dataset(self) -> List[Dict]:
        """Create mock fashion dataset for demonstration"""
        styles = ["Casual", "Formal", "Sporty", "Chic", "Classic"]
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        genders = ["Male", "Female", "Unisex"]
        categories = ["Upper", "Lower", "Shoes", "Accessories", "Outfit"]
        
        # Mock image URLs (using placeholder images)
        base_url = "https://via.placeholder.com/300x400"
        
        dataset = []
        for i in range(500):
            item = {
                "id": i,
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
        Download dataset from Hugging Face (placeholder for actual implementation)
        
        Args:
            split: Dataset split to download
            limit: Number of items to download
        """
        # This would use the datasets library in production:
        # from datasets import load_dataset
        # dataset = load_dataset("Anony100/FashionRec", split=f"train[:{limit}]", cache_dir=self.cache_dir)
        
        print(f"📦 Using mock dataset with {len(self.dataset)} items")
        return self.dataset
    
    def get_random_outfits(self, 
                          gender: Optional[str] = None, 
                          season: Optional[str] = None, 
                          style: Optional[str] = None, 
                          count: int = 12) -> List[Dict]:
        """
        Get random outfit recommendations with optional filtering
        
        Args:
            gender: Filter by gender (Male/Female/Unisex)
            season: Filter by season (Spring/Summer/Fall/Winter)
            style: Filter by style (Casual/Formal/Sporty/Chic)
            count: Number of outfits to return
            
        Returns:
            List of outfit dictionaries
        """
        filtered = self.dataset.copy()
        
        # Apply filters
        if gender:
            filtered = [item for item in filtered if item['gender'] == gender or item['gender'] == 'Unisex']
        
        if season:
            filtered = [item for item in filtered if item['season'] == season]
        
        if style:
            filtered = [item for item in filtered if item['style'] == style]
        
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
        upper_items = [item for item in self.dataset if item['category'] == 'Upper']
        if upper_items:
            result['upper'] = random.choice(upper_items)
        
        # Find lower garment
        lower_items = [item for item in self.dataset if item['category'] == 'Lower']
        if lower_items:
            result['lower'] = random.choice(lower_items)
        
        # Find shoes
        shoes_items = [item for item in self.dataset if item['category'] == 'Shoes']
        if shoes_items:
            result['shoes'] = random.choice(shoes_items)
        
        # Find accessories
        accessories_items = [item for item in self.dataset if item['category'] == 'Accessories']
        if accessories_items:
            result['accessories'] = random.choice(accessories_items)
        
        return result
    
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
            season = "Winter"
        elif temperature <= 15:
            season = "Fall"
        elif temperature <= 25:
            season = "Spring"
        else:
            season = "Summer"
        
        return self.get_random_outfits(season=season, count=12)
