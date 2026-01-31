# backend/database.py
"""
Database module for StyleSanctuary
Manages SQLite database for outfit saving and preset outfits.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "user_history.db")


def get_db_connection():
    """Create and return a database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create saved_outfits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            city VARCHAR(100),
            temperature FLOAT,
            weather_condition VARCHAR(50),
            gender VARCHAR(20),
            event VARCHAR(100),
            style VARCHAR(50),
            mood VARCHAR(50),
            recommendation TEXT,
            image_urls TEXT,
            is_favorite BOOLEAN DEFAULT 0
        )
    ''')
    
    # Create preset_outfits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preset_outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200),
            description TEXT,
            gender VARCHAR(20),
            season VARCHAR(20),
            style_tags TEXT,
            image_urls TEXT,
            temperature_min FLOAT,
            temperature_max FLOAT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✓ Database initialized at {DB_PATH}")


def save_outfit(outfit_data: Dict[str, Any]) -> int:
    """
    Save an outfit to the database.
    
    Args:
        outfit_data: Dictionary containing outfit information
            - city (str): City name
            - temperature (float): Temperature in Celsius
            - weather_condition (str): Weather description
            - gender (str): User's gender
            - event (str): Occasion/event
            - style (str): Style preference
            - mood (str): User's mood
            - recommendation (str): LLM-generated recommendation text
            - image_urls (list): List of image URLs/paths
            - is_favorite (bool, optional): Favorite flag
    
    Returns:
        int: ID of the saved outfit
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO saved_outfits (
            city, temperature, weather_condition, gender, event,
            style, mood, recommendation, image_urls, is_favorite
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        outfit_data.get('city'),
        outfit_data.get('temperature'),
        outfit_data.get('weather_condition'),
        outfit_data.get('gender'),
        outfit_data.get('event'),
        outfit_data.get('style'),
        outfit_data.get('mood'),
        outfit_data.get('recommendation'),
        json.dumps(outfit_data.get('image_urls', [])),
        outfit_data.get('is_favorite', 0)
    ))
    
    outfit_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return outfit_id


def get_saved_outfits(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve saved outfits from the database.
    
    Args:
        filters: Optional filters to apply
            - city (str): Filter by city
            - gender (str): Filter by gender
            - event (str): Filter by event
            - is_favorite (bool): Filter by favorite status
            - date_from (str): Filter by date (ISO format)
            - date_to (str): Filter by date (ISO format)
            - limit (int): Maximum number of results
    
    Returns:
        List of outfit dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM saved_outfits WHERE 1=1"
    params = []
    
    if filters:
        if 'city' in filters:
            query += " AND city = ?"
            params.append(filters['city'])
        
        if 'gender' in filters:
            query += " AND gender = ?"
            params.append(filters['gender'])
        
        if 'event' in filters:
            query += " AND event = ?"
            params.append(filters['event'])
        
        if 'is_favorite' in filters:
            query += " AND is_favorite = ?"
            params.append(filters['is_favorite'])
        
        if 'date_from' in filters:
            query += " AND created_at >= ?"
            params.append(filters['date_from'])
        
        if 'date_to' in filters:
            query += " AND created_at <= ?"
            params.append(filters['date_to'])
    
    query += " ORDER BY created_at DESC"
    
    if filters and 'limit' in filters:
        query += " LIMIT ?"
        params.append(filters['limit'])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    outfits = []
    for row in rows:
        outfit = dict(row)
        outfit['image_urls'] = json.loads(outfit['image_urls']) if outfit['image_urls'] else []
        outfits.append(outfit)
    
    return outfits


def delete_outfit(outfit_id: int) -> bool:
    """
    Delete an outfit from the database.
    
    Args:
        outfit_id: ID of the outfit to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM saved_outfits WHERE id = ?", (outfit_id,))
    affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return affected > 0


def toggle_favorite(outfit_id: int) -> bool:
    """
    Toggle the favorite status of an outfit.
    
    Args:
        outfit_id: ID of the outfit
    
    Returns:
        bool: New favorite status
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current status
    cursor.execute("SELECT is_favorite FROM saved_outfits WHERE id = ?", (outfit_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        return False
    
    new_status = not bool(row['is_favorite'])
    
    # Update status
    cursor.execute(
        "UPDATE saved_outfits SET is_favorite = ? WHERE id = ?",
        (new_status, outfit_id)
    )
    
    conn.commit()
    conn.close()
    
    return new_status


def get_preset_outfits(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve preset outfits from the database.
    
    Args:
        filters: Optional filters to apply
            - gender (str): Filter by gender
            - season (str): Filter by season
            - temperature (float): Filter by suitable temperature
            - style_tags (list): Filter by style tags
            - limit (int): Maximum number of results
    
    Returns:
        List of preset outfit dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM preset_outfits WHERE 1=1"
    params = []
    
    if filters:
        if 'gender' in filters:
            query += " AND gender = ?"
            params.append(filters['gender'])
        
        if 'season' in filters:
            query += " AND season = ?"
            params.append(filters['season'])
        
        if 'temperature' in filters:
            temp = filters['temperature']
            query += " AND temperature_min <= ? AND temperature_max >= ?"
            params.extend([temp, temp])
        
        if 'style_tags' in filters and filters['style_tags']:
            # Search for any matching style tag
            tag_conditions = []
            for tag in filters['style_tags']:
                tag_conditions.append("style_tags LIKE ?")
                params.append(f'%"{tag}"%')
            query += " AND (" + " OR ".join(tag_conditions) + ")"
    
    query += " ORDER BY RANDOM()"
    
    if filters and 'limit' in filters:
        query += " LIMIT ?"
        params.append(filters['limit'])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    outfits = []
    for row in rows:
        outfit = dict(row)
        outfit['style_tags'] = json.loads(outfit['style_tags']) if outfit['style_tags'] else []
        outfit['image_urls'] = json.loads(outfit['image_urls']) if outfit['image_urls'] else []
        outfits.append(outfit)
    
    return outfits


def add_preset_outfit(preset_data: Dict[str, Any]) -> int:
    """
    Add a preset outfit to the database.
    
    Args:
        preset_data: Dictionary containing preset outfit information
    
    Returns:
        int: ID of the added preset outfit
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO preset_outfits (
            title, description, gender, season, style_tags,
            image_urls, temperature_min, temperature_max
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        preset_data.get('title'),
        preset_data.get('description'),
        preset_data.get('gender'),
        preset_data.get('season'),
        json.dumps(preset_data.get('style_tags', [])),
        json.dumps(preset_data.get('image_urls', [])),
        preset_data.get('temperature_min'),
        preset_data.get('temperature_max')
    ))
    
    preset_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return preset_id


# Initialize database on module import
try:
    init_db()
except Exception as e:
    print(f"Warning: Could not initialize database. Please ensure the data directory is writable and try running setup.py. Error: {e}")
