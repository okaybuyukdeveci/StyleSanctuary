#!/usr/bin/env python3
"""
Setup script for StyleSanctuary
Downloads and prepares the FashionRec dataset.
"""

import os
import sys
from backend.dataset_loader import download_fashionrec_dataset, create_dataset_structure
from backend.database import init_db
from config import DATASET_SIZE


def main():
    """Run setup tasks."""
    print("=" * 60)
    print("  StyleSanctuary Setup")
    print("=" * 60)
    print()
    
    # Step 1: Initialize database
    print("Step 1: Initializing database...")
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return 1
    
    print()
    
    # Step 2: Create dataset structure
    print("Step 2: Creating dataset structure...")
    try:
        create_dataset_structure()
        print("✓ Dataset structure created successfully")
    except Exception as e:
        print(f"✗ Error creating dataset structure: {e}")
        return 1
    
    print()
    
    # Step 3: Download dataset
    print(f"Step 3: Preparing FashionRec dataset ({DATASET_SIZE} size)...")
    try:
        download_fashionrec_dataset(DATASET_SIZE)
        print("✓ Dataset prepared successfully")
    except Exception as e:
        print(f"✗ Error preparing dataset: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Copy .env.example to .env and configure your API keys")
    print("  2. Run: streamlit run app.py")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
