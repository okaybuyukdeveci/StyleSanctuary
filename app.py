#!/usr/bin/env python3
"""
StyleSanctuary - Modern Weather-Based Outfit Recommendation Web App
"""

import streamlit as st
import os
from datetime import datetime
from typing import Dict, List, Any

# Import backend modules
from backend.weather import get_weather
from backend.agent import get_outfit_recommendation
from backend.database import (
    save_outfit, get_saved_outfits, delete_outfit, toggle_favorite, init_db
)
from backend.dataset_loader import (
    get_random_outfits, filter_outfits, match_outfit_to_images
)

# Page configuration
st.set_page_config(
    page_title="StyleSanctuary - Weather Fashion Assistant",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS styling."""
    css_file = os.path.join("frontend", "static", "style.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'outfit_result' not in st.session_state:
    st.session_state.outfit_result = None
if 'form_step' not in st.session_state:
    st.session_state.form_step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Initialize database
init_db()


def render_header():
    """Render the main header."""
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: white; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                👔 StyleSanctuary
            </h1>
            <p style='color: white; font-size: 1.2rem; opacity: 0.9;'>
                Your Personal Weather-Smart Fashion Assistant
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_weather_horizon():
    """Render weather cards for 5 major cities."""
    st.markdown("<h2 class='section-header'>🌤️ Weather Horizon</h2>", unsafe_allow_html=True)
    
    cities = ['London', 'New York', 'Tokyo', 'Paris', 'Istanbul']
    
    cols = st.columns(5)
    
    for idx, city in enumerate(cities):
        with cols[idx]:
            try:
                weather = get_weather(city)
                temp = weather['temperature']
                condition = weather['condition'].title()
                
                # Weather icon mapping
                weather_icons = {
                    'clear': '☀️',
                    'clouds': '☁️',
                    'rain': '🌧️',
                    'snow': '❄️',
                    'mist': '🌫️',
                    'fog': '🌫️'
                }
                
                icon = '🌤️'
                for key, value in weather_icons.items():
                    if key in condition.lower():
                        icon = value
                        break
                
                st.markdown(f"""
                    <div class='weather-card'>
                        <h3 style='color: white; margin: 0;'>{city}</h3>
                        <div style='font-size: 3rem; margin: 10px 0;'>{icon}</div>
                        <p style='color: white; font-size: 1.5rem; font-weight: bold; margin: 5px 0;'>
                            {temp}°C
                        </p>
                        <p style='color: white; opacity: 0.8; margin: 0;'>{condition}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                    <div class='weather-card'>
                        <h3 style='color: white;'>{city}</h3>
                        <p style='color: white; opacity: 0.7;'>Weather unavailable</p>
                    </div>
                """, unsafe_allow_html=True)


def render_quick_outfit_gallery():
    """Render the Quick Outfit Gallery (browse without questions)."""
    st.markdown("<h2 class='section-header'>✨ Quick Outfit Gallery</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; opacity: 0.9; margin-bottom: 20px;'>"
                "Browse outfit inspirations without answering questions</p>", unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gender_filter = st.selectbox("Gender", ["All", "Male", "Female", "Unisex"], key="gallery_gender")
    
    with col2:
        season_filter = st.selectbox("Season", ["All", "Spring", "Summer", "Fall", "Winter"], key="gallery_season")
    
    with col3:
        style_filter = st.selectbox("Style", ["All", "Casual", "Sporty", "Classic", "Minimalist", "Elegant"], key="gallery_style")
    
    with col4:
        category_filter = st.selectbox("Category", ["All", "tops", "bottoms", "shoes", "accessories"], key="gallery_category")
    
    # Apply filters
    filters = {}
    if gender_filter != "All":
        filters['gender'] = gender_filter
    if season_filter != "All":
        filters['season'] = season_filter
    if style_filter != "All":
        filters['style'] = style_filter
    if category_filter != "All":
        filters['category'] = category_filter
    
    # Get outfits
    outfits = filter_outfits(limit=12, **filters)
    
    if not outfits:
        st.info("No outfits found matching your filters. Try adjusting them!")
        return
    
    # Display outfits in grid
    cols = st.columns(4)
    
    for idx, outfit in enumerate(outfits):
        with cols[idx % 4]:
            # Create outfit card
            with st.container():
                st.markdown(f"""
                    <div class='outfit-card'>
                        <div style='padding: 15px;'>
                            <h4 style='margin: 0 0 10px 0; color: #1a202c;'>{outfit['name']}</h4>
                            <p style='margin: 5px 0; color: #666; font-size: 0.9rem;'>
                                <strong>Category:</strong> {outfit['category'].title()}
                            </p>
                            <p style='margin: 5px 0; color: #666; font-size: 0.9rem;'>
                                <strong>Gender:</strong> {outfit['gender']}
                            </p>
                            <p style='margin: 5px 0; color: #666; font-size: 0.9rem;'>
                                <strong>Season:</strong> {outfit['season']}
                            </p>
                            <p style='margin: 5px 0; color: #666; font-size: 0.9rem;'>
                                <strong>Style:</strong> {outfit['style']}
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Favorite button
                if st.button("❤️", key=f"fav_{outfit['id']}", help="Add to favorites"):
                    st.success("Added to favorites!")


def render_personalized_form():
    """Render the multi-step personalized recommendation form."""
    st.markdown("<h2 class='section-header'>🎯 Get Personalized Outfit</h2>", unsafe_allow_html=True)
    
    # Create tabs for better UX
    tab1, tab2, tab3 = st.tabs(["📍 Location & Weather", "👤 Personal Info", "🎨 Style & Mood"])
    
    with tab1:
        st.subheader("Where are you?")
        city = st.text_input("City", value="London", placeholder="e.g., London, New York, Istanbul")
        st.session_state.form_data['city'] = city
        
        if city:
            try:
                weather = get_weather(city)
                st.success(f"✓ Weather: {weather['temperature']}°C, {weather['condition'].title()}")
                st.session_state.form_data['weather'] = weather
            except Exception as e:
                st.error(f"Could not fetch weather for {city}. Please check the city name.")
    
    with tab2:
        st.subheader("Tell us about yourself")
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        event = st.text_input("Where are you going?", placeholder="e.g., Office, School, Date, Gym, Party")
        
        st.session_state.form_data['gender'] = gender
        st.session_state.form_data['event'] = event
    
    with tab3:
        st.subheader("Your style preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            style = st.selectbox("Preferred Style", [
                "Casual", "Sporty", "Classic", "Minimalist", 
                "Elegant", "Streetwear", "Boho", "Vintage"
            ])
        
        with col2:
            mood = st.selectbox("Current Mood", [
                "Energetic", "Relaxed", "Professional", "Creative",
                "Confident", "Playful", "Comfortable"
            ])
        
        st.session_state.form_data['style'] = style
        st.session_state.form_data['mood'] = mood
    
    # Generate button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ Generate My Outfit", type="primary", use_container_width=True):
        if 'weather' not in st.session_state.form_data:
            st.error("Please enter a valid city to get weather information.")
            return
        
        if not st.session_state.form_data.get('event'):
            st.error("Please tell us where you're going.")
            return
        
        with st.spinner("Creating your perfect outfit... 🎨"):
            try:
                # Get LLM recommendation
                context = {
                    'gender': st.session_state.form_data['gender'],
                    'event': st.session_state.form_data['event'],
                    'style': st.session_state.form_data['style'],
                    'mood': st.session_state.form_data['mood']
                }
                
                recommendation = get_outfit_recommendation(
                    st.session_state.form_data['weather'],
                    context
                )
                
                # Match with dataset images
                outfit_items = match_outfit_to_images(
                    recommendation,
                    context,
                    st.session_state.form_data['weather']
                )
                
                # Store result
                st.session_state.outfit_result = {
                    'recommendation': recommendation,
                    'outfit_items': outfit_items,
                    'weather': st.session_state.form_data['weather'],
                    'context': context,
                    'city': st.session_state.form_data['city']
                }
                
                # Switch to results view
                st.session_state.page = 'results'
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating outfit: {e}")


def render_outfit_results():
    """Render the AI-powered wardrobe canvas with results."""
    if not st.session_state.outfit_result:
        st.warning("No outfit generated yet. Please go back and create one!")
        if st.button("← Back to Form"):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    result = st.session_state.outfit_result
    
    st.markdown("<h2 class='section-header'>🎨 Your Perfect Outfit</h2>", unsafe_allow_html=True)
    
    # Weather info
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(f"📍 {result['city']} | 🌡️ {result['weather']['temperature']}°C | "
                f"🌤️ {result['weather']['condition'].title()}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LLM Recommendation
    with st.expander("📝 Style Expert Recommendation", expanded=True):
        st.markdown(f"<div style='background: white; padding: 20px; border-radius: 12px;'>"
                   f"{result['recommendation']}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Outfit Items
    st.subheader("🎯 Matched Items from Gallery")
    
    categories = ['tops', 'bottoms', 'shoes', 'accessories']
    category_labels = {
        'tops': '👕 Upper Garments',
        'bottoms': '👖 Lower Garments',
        'shoes': '👟 Footwear',
        'accessories': '🎒 Accessories'
    }
    
    for category in categories:
        items = result['outfit_items'].get(category, [])
        if items:
            st.markdown(f"### {category_labels[category]}")
            cols = st.columns(min(len(items), 4))
            
            for idx, item in enumerate(items):
                with cols[idx]:
                    st.markdown(f"""
                        <div class='outfit-card'>
                            <div style='padding: 15px;'>
                                <h5 style='margin: 0 0 8px 0;'>{item['name']}</h5>
                                <p style='margin: 3px 0; font-size: 0.85rem; color: #666;'>
                                    {item.get('color', 'N/A')}
                                </p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save This Outfit", use_container_width=True):
            try:
                # Prepare outfit data
                outfit_data = {
                    'city': result['city'],
                    'temperature': result['weather']['temperature'],
                    'weather_condition': result['weather']['condition'],
                    'gender': result['context']['gender'],
                    'event': result['context']['event'],
                    'style': result['context']['style'],
                    'mood': result['context']['mood'],
                    'recommendation': result['recommendation'],
                    'image_urls': [],  # Would contain actual image paths
                    'is_favorite': False
                }
                
                outfit_id = save_outfit(outfit_data)
                st.success(f"✓ Outfit saved! (ID: {outfit_id})")
            except Exception as e:
                st.error(f"Error saving outfit: {e}")
    
    with col2:
        if st.button("🔄 Generate Different Outfit", use_container_width=True):
            st.session_state.outfit_result = None
            st.session_state.page = 'home'
            st.rerun()
    
    with col3:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()


def render_saved_outfits():
    """Render the saved outfits history page."""
    st.markdown("<h2 class='section-header'>💝 My Saved Outfits</h2>", unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_city = st.selectbox("Filter by City", ["All"] + ["London", "New York", "Tokyo", "Paris", "Istanbul"])
    
    with col2:
        filter_gender = st.selectbox("Filter by Gender", ["All", "Male", "Female", "Other"])
    
    with col3:
        filter_event = st.text_input("Filter by Event", placeholder="e.g., Office")
    
    with col4:
        show_favorites = st.checkbox("Favorites Only")
    
    # Build filters
    filters = {}
    if filter_city != "All":
        filters['city'] = filter_city
    if filter_gender != "All":
        filters['gender'] = filter_gender
    if filter_event:
        filters['event'] = filter_event
    if show_favorites:
        filters['is_favorite'] = True
    
    # Get saved outfits
    saved = get_saved_outfits(filters)
    
    if not saved:
        st.info("No saved outfits yet. Create your first outfit!")
        return
    
    st.markdown(f"<p style='text-align: center; color: white;'>Found {len(saved)} outfit(s)</p>", 
                unsafe_allow_html=True)
    
    # Display saved outfits
    for outfit in saved:
        with st.expander(f"🎨 {outfit['event']} in {outfit['city']} - {outfit['created_at'][:10]}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Weather:** {outfit['temperature']}°C, {outfit['weather_condition']}")
                st.write(f"**Style:** {outfit['style']} | **Mood:** {outfit['mood']}")
                st.markdown("---")
                st.write(outfit['recommendation'])
            
            with col2:
                # Action buttons
                fav_label = "💛 Unfavorite" if outfit['is_favorite'] else "❤️ Favorite"
                if st.button(fav_label, key=f"fav_{outfit['id']}"):
                    toggle_favorite(outfit['id'])
                    st.rerun()
                
                if st.button("🗑️ Delete", key=f"del_{outfit['id']}"):
                    delete_outfit(outfit['id'])
                    st.success("Outfit deleted!")
                    st.rerun()


def main():
    """Main application entry point."""
    render_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("💝 My Saved Outfits", use_container_width=True):
            st.session_state.page = 'saved'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info(
            "StyleSanctuary is your personal weather-smart fashion assistant. "
            "Get AI-powered outfit recommendations based on weather, your style, and occasion."
        )
        
        st.markdown("---")
        st.markdown("### 🛠️ Technology")
        st.markdown("""
        - **Weather:** OpenWeatherMap API
        - **AI:** Ollama (Local LLM)
        - **Dataset:** FashionRec
        - **Framework:** Streamlit
        """)
    
    # Main content area
    if st.session_state.page == 'home':
        render_weather_horizon()
        st.markdown("<br><br>", unsafe_allow_html=True)
        render_quick_outfit_gallery()
        st.markdown("<br><br>", unsafe_allow_html=True)
        render_personalized_form()
    
    elif st.session_state.page == 'results':
        render_outfit_results()
    
    elif st.session_state.page == 'saved':
        render_saved_outfits()


if __name__ == "__main__":
    main()
