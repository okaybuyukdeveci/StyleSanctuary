"""
StyleSanctuary - AI-Powered Weather-Based Outfit Recommendation App

Main Streamlit application with modern UI and FashionRec dataset integration
"""

import streamlit as st
from backend.weather import get_weather
from backend.agent import get_outfit_recommendation_with_images
from backend.dataset_loader import FashionDatasetLoader
from backend.database import OutfitDatabase


# Page configuration
st.set_page_config(
    page_title="StyleSanctuary",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_custom_css():
    """Load custom CSS for glassmorphism and styling"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Weather cards */
    .weather-card {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        margin: 10px 0;
    }
    
    .weather-card:hover {
        transform: translateY(-5px);
    }
    
    .weather-card h4 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
    }
    
    .weather-card h2 {
        margin: 10px 0;
        font-size: 36px;
        font-weight: 700;
    }
    
    .weather-card p {
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Outfit cards */
    .outfit-card {
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        transition: transform 0.3s ease;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .outfit-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 20px;
        padding: 10px 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Section titles */
    h3 {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.title("👔 StyleSanctuary")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Ana Sayfa", "✨ Kişisel Öneri", "💾 Kayıtlarım", "ℹ️ Hakkında"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.caption("AI-Powered Fashion Assistant")
        st.caption("Weather-Based Outfit Recommendations")
        
        return page


def render_weather_horizon():
    """Render weather horizon section with multiple cities"""
    st.markdown("### 🌤️ Weather Horizon")
    st.caption("Canlı hava durumu bilgileri")
    
    cities = ["London", "New York", "Tokyo", "Sydney", "Dubai"]
    
    cols = st.columns(5)
    
    for idx, city in enumerate(cities):
        with cols[idx]:
            try:
                weather = get_weather(city)
                
                # Weather emoji based on condition
                condition_lower = weather['condition'].lower()
                emoji = "☀️"
                if "cloud" in condition_lower:
                    emoji = "☁️"
                elif "rain" in condition_lower:
                    emoji = "🌧️"
                elif "snow" in condition_lower:
                    emoji = "❄️"
                elif "clear" in condition_lower:
                    emoji = "☀️"
                
                st.markdown(f"""
                <div class="weather-card">
                    <h4>{city}</h4>
                    <div style="font-size: 48px; margin: 10px 0;">{emoji}</div>
                    <h2>{weather['temperature']:.1f}°C</h2>
                    <p>{weather['condition'].title()}</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="weather-card">
                    <h4>{city}</h4>
                    <p style="margin-top: 20px;">❌ Veri alınamadı</p>
                </div>
                """, unsafe_allow_html=True)


def render_outfit_gallery(dataset_loader, database):
    """Render quick outfit gallery with filters"""
    st.markdown("### 👗 Quick Outfit Gallery")
    st.caption("Sorulara cevap vermeden kombin önerilerini keşfedin!")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender_filter = st.selectbox("Cinsiyet", ["Hepsi", "Male", "Female", "Unisex"])
    with col2:
        season_filter = st.selectbox("Mevsim", ["Hepsi", "Spring", "Summer", "Fall", "Winter"])
    with col3:
        style_filter = st.selectbox("Stil", ["Hepsi", "Casual", "Formal", "Sporty", "Chic"])
    
    # Prepare filters
    filters = {
        "gender": None if gender_filter == "Hepsi" else gender_filter,
        "season": None if season_filter == "Hepsi" else season_filter,
        "style": None if style_filter == "Hepsi" else style_filter
    }
    
    # Get outfits from dataset
    outfits = dataset_loader.get_random_outfits(**filters, count=12)
    
    if not outfits:
        st.info("Seçilen filtrelere uygun kombin bulunamadı. Farklı filtreler deneyin!")
        return
    
    # Display in grid layout
    cols = st.columns(4)
    
    for idx, outfit in enumerate(outfits):
        with cols[idx % 4]:
            st.image(outfit["image_url"], use_container_width=True)
            st.markdown(f"**{outfit['title']}**")
            st.caption(f"{outfit['season']} • {outfit['style']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("👁️ Detay", key=f"view_{idx}"):
                    with st.expander("Detaylar", expanded=True):
                        st.write(f"**Kategori:** {outfit['category']}")
                        st.write(f"**Renk:** {outfit['color']}")
                        st.write(f"**Etiketler:** {', '.join(outfit['tags'])}")
            
            with col_b:
                if st.button("💾 Kaydet", key=f"save_{idx}"):
                    try:
                        database.save_outfit({
                            "city": "Gallery",
                            "temperature": 0,
                            "weather_condition": "N/A",
                            "gender": outfit['gender'],
                            "event": "Gallery Browse",
                            "style": outfit['style'],
                            "mood": "Exploring",
                            "recommendation": f"Quick save: {outfit['title']}",
                            "image_urls": {"main": outfit["image_url"]},
                            "dataset_ids": [outfit["id"]]
                        })
                        st.success("✅ Kaydedildi!")
                    except Exception as e:
                        st.error(f"❌ Hata: {e}")


def render_personalized_recommendation(dataset_loader, database):
    """Render personalized recommendation form and results"""
    st.markdown("### ✨ Kişisel Kombin Önerisi")
    st.caption("AI destekli, size özel kombin önerisi alın")
    
    # Form
    with st.form("recommendation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            city = st.text_input("Şehir", value="London", help="Bulunduğunuz şehir")
            gender = st.radio("Cinsiyet", ["Male", "Female", "Other"])
            event = st.selectbox("Etkinlik", 
                               ["School", "Cafe", "Office", "Dinner", "Sports", "Party", "Casual Walk"])
        
        with col2:
            style_options = ["Casual", "Classic", "Minimalist", "Sporty", "Chic", "Formal"]
            style = st.multiselect("Stil Tercihleri", style_options, default=["Casual"])
            mood = st.select_slider("Ruh Hali", 
                                   options=["😢 Tired", "😐 Neutral", "😊 Happy", "🔥 Energetic"])
        
        submit_button = st.form_submit_button("🎨 Kombin Öner", use_container_width=True)
    
    # Process recommendation
    if submit_button:
        if not city.strip():
            st.error("Lütfen şehir adını girin!")
            return
        
        if not style:
            st.error("Lütfen en az bir stil tercihi seçin!")
            return
        
        with st.spinner("🌤️ Hava durumu kontrol ediliyor..."):
            try:
                weather = get_weather(city)
            except Exception as e:
                st.error(f"❌ Hava durumu alınamadı: {e}")
                return
        
        # Display weather info
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.metric("Şehir", city.title())
        with col2:
            st.metric("Sıcaklık", f"{weather['temperature']:.1f}°C")
        with col3:
            st.metric("Durum", weather['condition'].title())
        
        st.markdown("---")
        
        with st.spinner("🤖 AI kombin oluşturuyor..."):
            try:
                # Prepare context
                context = {
                    "gender": gender,
                    "event": event,
                    "style": ", ".join(style),
                    "mood": mood
                }
                
                # Get recommendation
                recommendation = get_outfit_recommendation_with_images(weather, context, dataset_loader)
                
                # Display recommendation
                st.markdown("#### 🎯 AI Önerisi")
                st.info(recommendation["text_recommendation"])
                
                # Display images
                if recommendation["images"]:
                    st.markdown("#### 📸 Önerilen Kıyafetler")
                    
                    image_cols = st.columns(len(recommendation["images"]))
                    
                    for idx, (item_type, image_data) in enumerate(recommendation["images"].items()):
                        with image_cols[idx]:
                            st.image(image_data["image_url"], caption=item_type.title(), use_container_width=True)
                            st.caption(f"{image_data.get('style', 'N/A')} - {image_data.get('color', 'N/A')}")
                
                # Save button
                st.markdown("---")
                if st.button("💾 Bu Kombini Kaydet", type="primary", use_container_width=True):
                    try:
                        database.save_outfit({
                            "city": city,
                            "temperature": weather["temperature"],
                            "weather_condition": weather["condition"],
                            "gender": gender,
                            "event": event,
                            "style": ", ".join(style),
                            "mood": mood,
                            "recommendation": recommendation["text_recommendation"],
                            "image_urls": recommendation["images"],
                            "dataset_ids": recommendation["dataset_items"]
                        })
                        st.success("✅ Kombin başarıyla kaydedildi!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Kayıt hatası: {e}")
                
            except Exception as e:
                st.error(f"❌ Öneri oluşturulamadı: {e}")
                st.info("Ollama servisinin çalıştığından emin olun: http://localhost:11434")


def render_saved_outfits(database):
    """Render saved outfits history"""
    st.markdown("### 💾 Kayıtlı Kombinlerim")
    st.caption("Geçmiş kombin önerileriniz")
    
    try:
        outfits = database.get_all_outfits()
    except Exception as e:
        st.error(f"❌ Veritabanı hatası: {e}")
        return
    
    if not outfits:
        st.info("Henüz kaydedilmiş kombin yok. Kombin oluştur ve kaydet!")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_city = st.text_input("Şehir Filtrele", placeholder="Şehir adı...")
    with col2:
        sort_by = st.selectbox("Sırala", ["En Yeni", "En Eski", "Favoriler"])
    
    # Apply filters
    filtered_outfits = outfits
    if filter_city:
        filtered_outfits = [o for o in outfits if filter_city.lower() in str(o.get('city', '')).lower()]
    
    # Sort
    if sort_by == "En Eski":
        filtered_outfits = list(reversed(filtered_outfits))
    elif sort_by == "Favoriler":
        filtered_outfits = [o for o in filtered_outfits if o.get('is_favorite')]
    
    st.markdown(f"**Toplam {len(filtered_outfits)} kombin**")
    st.markdown("---")
    
    # Display outfits
    for outfit in filtered_outfits:
        with st.expander(f"📅 {outfit.get('created_at', 'N/A')} - {outfit.get('city', 'Unknown')} "
                        f"({'⭐' if outfit.get('is_favorite') else ''})"):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**AI Önerisi:**")
                st.write(outfit.get('recommendation', 'N/A'))
                
                # Display images if available
                if outfit.get('image_urls'):
                    st.markdown("**Kıyafetler:**")
                    image_urls = outfit['image_urls']
                    if isinstance(image_urls, dict) and image_urls:
                        img_cols = st.columns(min(len(image_urls), 4))
                        for idx, (item_type, img_data) in enumerate(image_urls.items()):
                            if idx < 4:  # Limit to 4 images
                                with img_cols[idx]:
                                    if isinstance(img_data, dict) and 'image_url' in img_data:
                                        st.image(img_data['image_url'], caption=item_type.title(), 
                                               use_container_width=True)
                                    elif isinstance(img_data, str):
                                        st.image(img_data, caption=item_type.title(), 
                                               use_container_width=True)
            
            with col2:
                st.markdown("**Detaylar:**")
                st.write(f"🌡️ {outfit.get('temperature', 'N/A')}°C")
                st.write(f"🌤️ {outfit.get('weather_condition', 'N/A')}")
                st.write(f"👤 {outfit.get('gender', 'N/A')}")
                st.write(f"📍 {outfit.get('event', 'N/A')}")
                st.write(f"🎨 {outfit.get('style', 'N/A')}")
                st.write(f"😊 {outfit.get('mood', 'N/A')}")
                
                st.markdown("---")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("⭐ Favori", key=f"fav_{outfit['id']}"):
                        database.toggle_favorite(outfit['id'])
                        st.rerun()
                
                with col_b:
                    if st.button("🗑️ Sil", key=f"delete_{outfit['id']}"):
                        if database.delete_outfit(outfit['id']):
                            st.success("Silindi!")
                            st.rerun()


def render_about():
    """Render about page"""
    st.markdown("# 👔 StyleSanctuary")
    
    st.markdown("""
    AI destekli, hava durumuna göre kişiselleştirilmiş kombin önerisi uygulaması.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✨ Özellikler")
        st.markdown("""
        - 🌤️ **Canlı Hava Durumu**: 5 şehir için anlık hava durumu
        - 🎨 **Quick Outfit Gallery**: Sorulara cevap vermeden kombin önerileri
        - 🤖 **AI Destekli Öneriler**: Ollama LLM ile kişiselleştirilmiş kombinler
        - 📸 **Fashion Dataset**: Gerçek kıyafet görselleri
        - 💾 **Kombin Kaydetme**: Geçmiş kombinlerinizi saklayın
        - 🎭 **Kişiselleştirme**: Ruh halinize, stilinize göre öneriler
        """)
    
    with col2:
        st.markdown("### 🛠️ Teknolojiler")
        st.markdown("""
        - **Frontend**: Streamlit
        - **AI Model**: Ollama (Qwen 2.5)
        - **Weather API**: OpenWeatherMap
        - **Database**: SQLite
        - **Dataset**: Mock Fashion Data
        """)
    
    st.markdown("---")
    
    st.markdown("### 👤 Geliştirici")
    st.markdown("""
    **Okay Büyükdeveci**
    
    GitHub: [@okaybuyukdeveci](https://github.com/okaybuyukdeveci)
    """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Lisans")
    st.markdown("MIT License")


def initialize_session_state():
    """Initialize session state variables"""
    if 'dataset_loader' not in st.session_state:
        st.session_state.dataset_loader = FashionDatasetLoader()
    
    if 'database' not in st.session_state:
        st.session_state.database = OutfitDatabase()


def main():
    """Main application entry point"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Get instances
    dataset_loader = st.session_state.dataset_loader
    database = st.session_state.database
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Main content area
    if page == "🏠 Ana Sayfa":
        render_weather_horizon()
        st.markdown("---")
        render_outfit_gallery(dataset_loader, database)
    
    elif page == "✨ Kişisel Öneri":
        render_personalized_recommendation(dataset_loader, database)
    
    elif page == "💾 Kayıtlarım":
        render_saved_outfits(database)
    
    elif page == "ℹ️ Hakkında":
        render_about()


if __name__ == "__main__":
    main()
