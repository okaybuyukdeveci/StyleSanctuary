# backend/database.py
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional


class OutfitDatabase:
    """SQLite database manager for saved outfits"""
    
    def __init__(self, db_path: str = "data/user_history.db"):
        """Initialize database connection and create table if needed"""
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """Create the saved_outfits table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_outfits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                city VARCHAR(100),
                temperature FLOAT,
                weather_condition VARCHAR(100),
                gender VARCHAR(50),
                event VARCHAR(100),
                style VARCHAR(200),
                mood VARCHAR(100),
                recommendation TEXT,
                image_urls TEXT,
                dataset_ids TEXT,
                is_favorite BOOLEAN DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_outfit(self, outfit_data: dict) -> int:
        """
        Save an outfit to the database
        
        Args:
            outfit_data: Dictionary containing outfit information
            
        Returns:
            The ID of the newly created outfit
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert JSON fields to strings
        image_urls = json.dumps(outfit_data.get('image_urls', {}))
        dataset_ids = json.dumps(outfit_data.get('dataset_ids', []))
        
        cursor.execute("""
            INSERT INTO saved_outfits (
                city, temperature, weather_condition, gender, event,
                style, mood, recommendation, image_urls, dataset_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            outfit_data.get('city'),
            outfit_data.get('temperature'),
            outfit_data.get('weather_condition'),
            outfit_data.get('gender'),
            outfit_data.get('event'),
            outfit_data.get('style'),
            outfit_data.get('mood'),
            outfit_data.get('recommendation'),
            image_urls,
            dataset_ids
        ))
        
        outfit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return outfit_id
    
    def get_all_outfits(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve all saved outfits with optional filtering
        
        Args:
            filters: Optional dictionary with filter criteria
            
        Returns:
            List of outfit dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM saved_outfits ORDER BY created_at DESC"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        
        outfits = []
        for row in rows:
            outfit = dict(row)
            # Parse JSON fields
            try:
                outfit['image_urls'] = json.loads(outfit['image_urls']) if outfit['image_urls'] else {}
                outfit['dataset_ids'] = json.loads(outfit['dataset_ids']) if outfit['dataset_ids'] else []
            except json.JSONDecodeError:
                outfit['image_urls'] = {}
                outfit['dataset_ids'] = []
            
            outfits.append(outfit)
        
        return outfits
    
    def delete_outfit(self, outfit_id: int) -> bool:
        """
        Delete an outfit by ID
        
        Args:
            outfit_id: The ID of the outfit to delete
            
        Returns:
            True if deleted successfully
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM saved_outfits WHERE id = ?", (outfit_id,))
        
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        return deleted
    
    def toggle_favorite(self, outfit_id: int) -> bool:
        """
        Toggle the favorite status of an outfit
        
        Args:
            outfit_id: The ID of the outfit
            
        Returns:
            True if successful
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current favorite status
        cursor.execute("SELECT is_favorite FROM saved_outfits WHERE id = ?", (outfit_id,))
        result = cursor.fetchone()
        
        if result:
            new_status = not bool(result[0])
            cursor.execute("UPDATE saved_outfits SET is_favorite = ? WHERE id = ?", 
                         (new_status, outfit_id))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
