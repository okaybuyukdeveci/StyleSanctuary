# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Weather API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "6a43f0773a93c1af4d2670a2d96993a4")

# Ollama Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:7b-instruct")

# Dataset Configuration
DATASET_SIZE = os.getenv("DATASET_SIZE", "half")
