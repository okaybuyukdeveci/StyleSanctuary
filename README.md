# 👔 StyleSanctuary - Weather-Smart Fashion Assistant

<div align="center">

![StyleSanctuary Banner](https://img.shields.io/badge/Fashion-AI%20Powered-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Your Personal AI Fashion Stylist Based on Real-Time Weather**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-technology-stack) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

StyleSanctuary is a modern, AI-powered fashion recommendation system that suggests personalized outfits based on:
- 🌤️ **Real-time weather conditions**
- 👤 **Your personal style preferences**
- 🎯 **The occasion or event**
- 😊 **Your current mood**

Built with a beautiful glassmorphism UI inspired by modern design trends, StyleSanctuary offers both a CLI and web interface for maximum flexibility.

## ✨ Features

### 🌐 Modern Web Interface
- ✅ **Weather Horizon** - View weather for 5 major cities with beautiful glassmorphism cards
- ✅ **Quick Outfit Gallery** - Browse curated outfits WITHOUT answering questions
- ✅ **Smart Filtering** - Filter by gender, season, style, weather condition
- ✅ **Personalized Recommendations** - AI-powered outfit suggestions via local LLM
- ✅ **Outfit History** - Save and manage your favorite outfits
- ✅ **Responsive Design** - Works beautifully on desktop and mobile

### 🤖 AI-Powered
- Local LLM integration (Ollama) for privacy-first recommendations
- Smart outfit matching from FashionRec dataset
- Weather-aware suggestions (temperature, conditions, season)

### 💾 Data Management
- SQLite database for outfit history
- Favorite marking system
- Filter and search capabilities

### 🎨 Beautiful UI
- Glassmorphism design elements
- Smooth animations and transitions
- Pill-style buttons and modern cards
- Toast notifications

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running locally
- OpenWeatherMap API key (free tier works!)

### Step 1: Clone the Repository

```bash
git clone https://github.com/okaybuyukdeveci/StyleSanctuary.git
cd StyleSanctuary
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your API keys
# WEATHER_API_KEY=your_api_key_here
```

Get your free API key at: https://openweathermap.org/api

### Step 4: Setup Dataset and Database

```bash
python setup.py
```

This will:
- Initialize the SQLite database
- Create the dataset directory structure
- Download and prepare the FashionRec dataset metadata

### Step 5: Install and Configure Ollama

```bash
# Install Ollama from https://ollama.ai/

# Pull the recommended model
ollama pull qwen2.5:7b-instruct

# Start Ollama (it should be running in the background)
ollama serve
```

## 🎯 Usage

### Web Interface (Recommended)

Launch the Streamlit web application:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

#### User Journey:

1. **Quick Browse Mode**
   - View weather for major cities
   - Scroll to "Quick Outfit Gallery"
   - Filter by gender, season, or style
   - Click hearts to save favorites

2. **Personalized Mode**
   - Enter your city for weather
   - Fill in personal preferences (gender, event, style, mood)
   - Click "Generate My Outfit"
   - View AI-generated recommendations with matched items
   - Save your favorite combinations

3. **History**
   - Click "My Saved Outfits" in sidebar
   - View, filter, and manage saved outfits
   - Mark favorites or delete old ones

### CLI Interface (Classic Mode)

Run the command-line version:

```bash
python main.py
```

Follow the prompts to get outfit recommendations in your terminal.

## 📁 Project Structure

```
StyleSanctuary/
│
├── app.py                          # Main Streamlit web application
├── main.py                         # CLI version (legacy)
├── setup.py                        # Dataset & database setup script
├── config.py                       # Configuration with environment variables
├── requirements.txt                # Python dependencies
│
├── backend/
│   ├── __init__.py
│   ├── weather.py                  # Weather API integration
│   ├── agent.py                    # LLM outfit recommendation
│   ├── database.py                 # SQLite database operations
│   └── dataset_loader.py           # FashionRec dataset management
│
├── frontend/
│   └── static/
│       └── style.css               # Custom CSS (glassmorphism)
│
├── data/
│   ├── fashion_dataset/            # Downloaded outfit images
│   │   ├── images/
│   │   │   ├── tops/
│   │   │   ├── bottoms/
│   │   │   ├── shoes/
│   │   │   └── accessories/
│   │   └── metadata.json           # Dataset metadata
│   └── user_history.db             # SQLite database
│
├── .env                            # Environment variables (not in repo)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit, Custom CSS |
| **Backend** | Python 3.8+ |
| **AI/LLM** | Ollama (Local) |
| **Model** | qwen2.5:7b-instruct |
| **Weather API** | OpenWeatherMap |
| **Database** | SQLite3 |
| **Dataset** | [FashionRec](https://huggingface.co/datasets/Anony100/FashionRec) |
| **UI Design** | Glassmorphism, Modern CSS |

## 🎨 Design Inspiration

- **UI/UX**: Modern glassmorphism design
- **Color Palette**: Purple gradient with white glass effects
- **Components**: Inspired by 21st.dev and contemporary web design
- **Animations**: Smooth transitions and hover effects

## 📊 Features Checklist

- [x] Real-time weather integration for multiple cities
- [x] AI-powered outfit recommendations
- [x] Quick outfit gallery (browse without questions)
- [x] Personalized outfit generation
- [x] Outfit history and favorites
- [x] Smart filtering by gender, season, style
- [x] Responsive design (mobile + desktop)
- [x] Glassmorphism UI
- [x] SQLite data persistence
- [x] Dataset integration
- [x] CLI mode (backward compatible)
- [x] Environment variable configuration
- [x] Privacy-first (local LLM)

## 🔐 Security & Privacy

- ✅ API keys stored in `.env` file (never committed)
- ✅ Local LLM - no data sent to external AI services
- ✅ SQLite database stored locally
- ✅ No user tracking or analytics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Dataset download requires manual configuration for full FashionRec integration
- Ollama must be running locally for AI recommendations
- Weather API has rate limits on free tier

## 🗺️ Roadmap

- [ ] Full FashionRec dataset integration with images
- [ ] Image upload for personal wardrobe
- [ ] Social sharing of outfits
- [ ] Multi-language support (Turkish, English, etc.)
- [ ] Weather forecast integration (7-day outlook)
- [ ] Outfit rating and feedback system
- [ ] Mobile app (React Native)
- [ ] Cloud deployment option

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FashionRec Dataset** - Anony100/FashionRec on Hugging Face
- **OpenWeatherMap** - Weather data API
- **Ollama** - Local LLM infrastructure
- **Streamlit** - Web framework
- **Design Inspiration** - 21st.dev community

## 👨‍💻 Author

**Okay Büyükdeveci**

- GitHub: [@okaybuyukdeveci](https://github.com/okaybuyukdeveci)

---

<div align="center">

**Made with ❤️ and AI**

If you like this project, please give it a ⭐!

</div>