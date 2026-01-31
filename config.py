# config.py
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "6a43f0773a93c1af4d2670a2d96993a4")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:7b-instruct")

# Dataset config
DATASET_CACHE_DIR = os.getenv("DATASET_CACHE_DIR", "data/fashion_dataset")
DATASET_LIMIT = int(os.getenv("DATASET_LIMIT", "500"))
