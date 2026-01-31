# backend/__init__.py
"""
StyleSanctuary Backend Module
Handles database operations, dataset loading, and outfit recommendations.
"""

from .database import (
    save_outfit,
    get_saved_outfits,
    delete_outfit,
    toggle_favorite,
    get_preset_outfits,
    init_db
)

__all__ = [
    'save_outfit',
    'get_saved_outfits',
    'delete_outfit',
    'toggle_favorite',
    'get_preset_outfits',
    'init_db'
]
