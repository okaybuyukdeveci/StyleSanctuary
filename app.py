# app.py - FastAPI Web Application
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import json
import os
from datetime import datetime
from weather import get_weather
from agent import get_outfit_recommendation

app = FastAPI(title="StyleSanctuary", description="Weather-based outfit recommendation system")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Data file paths
OUTFITS_FILE = "data/outfits.json"
SAVED_OUTFITS_FILE = "data/saved_outfits.json"

# Load outfit dataset
def load_outfits():
    with open(OUTFITS_FILE, "r") as f:
        return json.load(f)

# Load saved outfits
def load_saved_outfits():
    if os.path.exists(SAVED_OUTFITS_FILE):
        with open(SAVED_OUTFITS_FILE, "r") as f:
            return json.load(f)
    return []

# Save outfit
def save_outfit(outfit_data):
    saved_outfits = load_saved_outfits()
    outfit_data["saved_at"] = datetime.now().isoformat()
    saved_outfits.append(outfit_data)
    with open(SAVED_OUTFITS_FILE, "w") as f:
        json.dump(saved_outfits, f, indent=2)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with outfit showcase"""
    outfits = load_outfits()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "outfits": outfits[:6]  # Show first 6 outfits on home page
    })

@app.get("/api/outfits")
async def get_all_outfits():
    """API endpoint to get all outfit suggestions"""
    return load_outfits()

@app.get("/api/outfits/filter")
async def filter_outfits(
    style: Optional[str] = None,
    season: Optional[str] = None,
    gender: Optional[str] = None
):
    """Filter outfits by criteria"""
    outfits = load_outfits()
    
    if style:
        outfits = [o for o in outfits if o.get("style", "").lower() == style.lower()]
    if season:
        outfits = [o for o in outfits if o.get("season", "").lower() == season.lower() or o.get("season") == "all"]
    if gender:
        outfits = [o for o in outfits if o.get("gender", "").lower() == gender.lower() or o.get("gender") == "unisex"]
    
    return outfits

@app.post("/api/recommend")
async def recommend_outfit(
    city: str = Form(...),
    gender: str = Form(...),
    event: str = Form(...),
    style: str = Form(...),
    mood: str = Form(...)
):
    """Get personalized outfit recommendation based on weather and preferences"""
    try:
        # Get weather data
        weather = get_weather(city)
        
        # Get AI recommendation
        context = {
            "gender": gender,
            "event": event,
            "style": style,
            "mood": mood
        }
        
        outfit_text = get_outfit_recommendation(weather, context)
        
        # Also find matching pre-defined outfits
        temperature = weather["temperature"]
        outfits = load_outfits()
        matching_outfits = [
            o for o in outfits 
            if o["temp_range"][0] <= temperature <= o["temp_range"][1]
        ]
        
        return {
            "success": True,
            "weather": weather,
            "recommendation": outfit_text,
            "matching_outfits": matching_outfits[:3]  # Top 3 matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-outfit")
async def save_outfit_api(
    outfit_name: str = Form(...),
    upper: str = Form(...),
    lower: str = Form(...),
    shoes: str = Form(...),
    accessories: str = Form(...),
    city: str = Form(...),
    temperature: float = Form(...)
):
    """Save a custom outfit"""
    outfit_data = {
        "name": outfit_name,
        "upper": upper,
        "lower": lower,
        "shoes": shoes,
        "accessories": accessories,
        "city": city,
        "temperature": temperature
    }
    save_outfit(outfit_data)
    return {"success": True, "message": "Outfit saved successfully!"}

@app.get("/api/saved-outfits")
async def get_saved_outfits():
    """Get all saved outfits"""
    return load_saved_outfits()

@app.get("/browse", response_class=HTMLResponse)
async def browse_outfits(request: Request):
    """Browse all outfit suggestions"""
    outfits = load_outfits()
    return templates.TemplateResponse("browse.html", {
        "request": request,
        "outfits": outfits
    })

@app.get("/recommend", response_class=HTMLResponse)
async def recommend_page(request: Request):
    """Personalized recommendation page"""
    return templates.TemplateResponse("recommend.html", {
        "request": request
    })

@app.get("/saved", response_class=HTMLResponse)
async def saved_page(request: Request):
    """View saved outfits"""
    saved_outfits = load_saved_outfits()
    return templates.TemplateResponse("saved.html", {
        "request": request,
        "saved_outfits": saved_outfits
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
