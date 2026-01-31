# agent.py
import requests
import time
from config import OLLAMA_URL, MODEL_NAME

def get_outfit_recommendation(weather: dict, context: dict) -> str:
    temperature = weather["temperature"]

    if temperature <= 5:
        temp_rule = "It's very cold. Thick outerwear is essential. Short-sleeved or thin clothing is NOT RECOMMENDED."
    elif temperature <= 15:
        temp_rule = "The weather is cool. A light coat, jacket, or sweater would be suitable."
    else:
        temp_rule = "The weather is mild or warm. Light clothing is suitable."

    prompt = f"""You are an expert personal fashion stylist with years of experience in creating weather-appropriate, stylish outfits.

Your task is to recommend a complete outfit based on the user's profile and current weather conditions.

=== WEATHER CONDITIONS ===
- Temperature: {temperature}°C
- Weather: {weather["condition"]}

=== USER PROFILE ===
- Gender: {context["gender"]}
- Going to: {context["event"]}
- Preferred style: {context["style"]}
- Current mood: {context["mood"]}

=== WEATHER-BASED RULE ===
{temp_rule}

=== GUIDELINES ===
1. Recommend clothing items appropriate for the user's gender
2. Ensure the outfit matches both the weather and the occasion
3. Consider the user's style preference and mood when selecting items
4. Suggest practical, commonly available clothing items
5. Keep suggestions concise and actionable

=== OUTPUT FORMAT ===
Provide your recommendation in this exact format:

Upper Garments: [specific item(s)]
Lower Garments: [specific item(s)]
Shoes: [specific footwear]
Accessories: [optional items like bags, hats, sunglasses, etc.]

Brief Tip: [One short styling tip based on the weather/occasion]
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,   # daha az saçmalama
            "top_p": 0.9
        }
    }

    start_time = time.perf_counter()

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    end_time = time.perf_counter()

    response_time = end_time - start_time
    print(f"\n⏱️ Ollama response time: {response_time:.2f} seconds\n")

    return response.json()["response"].strip()


def get_outfit_recommendation_with_images(weather: dict, context: dict, dataset_loader):
    """
    Get outfit recommendation with real images from FashionRec dataset
    
    Args:
        weather: Weather data dictionary
        context: User context (gender, event, style, mood)
        dataset_loader: FashionDatasetLoader instance
        
    Returns:
        Dictionary with text recommendation, images, and dataset item IDs
    """
    # Get text recommendation from LLM
    text_recommendation = get_outfit_recommendation(weather, context)
    
    # Get matching images from dataset
    temperature = weather["temperature"]
    
    # Fetch items by category
    tops = dataset_loader.get_items_by_category("top", temperature, count=1)
    bottoms = dataset_loader.get_items_by_category("bottom", temperature, count=1)
    shoes = dataset_loader.get_items_by_category("shoes", temperature, count=1)
    accessories = dataset_loader.get_items_by_category("accessories", temperature, count=1)
    
    # Prepare response
    images = {}
    dataset_items = []
    
    if tops:
        images["top"] = {
            "image_url": tops[0]["image_url"],
            "title": tops[0]["title"],
            "style": tops[0]["style"],
            "color": tops[0]["color"]
        }
        dataset_items.append(tops[0]["id"])
    
    if bottoms:
        images["bottom"] = {
            "image_url": bottoms[0]["image_url"],
            "title": bottoms[0]["title"],
            "style": bottoms[0]["style"],
            "color": bottoms[0]["color"]
        }
        dataset_items.append(bottoms[0]["id"])
    
    if shoes:
        images["shoes"] = {
            "image_url": shoes[0]["image_url"],
            "title": shoes[0]["title"],
            "style": shoes[0]["style"],
            "color": shoes[0]["color"]
        }
        dataset_items.append(shoes[0]["id"])
    
    if accessories:
        images["accessories"] = {
            "image_url": accessories[0]["image_url"],
            "title": accessories[0]["title"],
            "style": accessories[0]["style"],
            "color": accessories[0]["color"]
        }
        dataset_items.append(accessories[0]["id"])
    
    return {
        "text_recommendation": text_recommendation,
        "images": images,
        "dataset_items": dataset_items
    }
