# StyleSanctuary 👗

**Your Personal Fashion Assistant - Weather-Based Outfit Recommendations**

StyleSanctuary is a modern web application that provides personalized outfit recommendations based on real-time weather conditions, your style preferences, mood, and occasion.

## ✨ Features

- 🌤️ **Weather-Smart Recommendations**: Get outfit suggestions based on real-time weather data from your city
- 🎨 **Browse Pre-Designed Outfits**: Explore a curated collection of 12+ outfit ideas for different seasons and styles
- 🤖 **AI-Powered Personalization**: Receive personalized recommendations using Ollama AI
- 💾 **Save Your Favorites**: Keep track of your favorite outfit combinations
- 📱 **Responsive Design**: Beautiful, modern interface that works on desktop and mobile
- 🎯 **Filter by Style**: Browse outfits by style (casual, sporty, classic, minimalist), season, and gender

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running (for AI recommendations)
- OpenWeather API key (free tier works fine)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/okaybuyukdeveci/StyleSanctuary.git
   cd StyleSanctuary
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Ollama (for AI recommendations)**
   ```bash
   # Install Ollama from https://ollama.ai/
   # Then pull the model:
   ollama pull qwen2.5:7b-instruct
   ```

4. **Configure API keys**
   - Edit `config.py` and add your OpenWeather API key
   - The default API key is included, but you can get your own free key at https://openweathermap.org/api

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to: `http://localhost:8000`

## 📖 Usage

### Home Page
- Browse trending outfit ideas
- See featured outfits for different styles and occasions
- Quick access to all features

### Browse Outfits
- Explore the complete collection of 12+ pre-designed outfits
- Filter by style (casual, sporty, classic, minimalist)
- Filter by season (spring, summer, autumn, winter)
- Filter by gender preference
- Click on any outfit to see detailed information

### Get Personalized Recommendation
1. Enter your city (e.g., London, Istanbul, New York)
2. Select your gender preference
3. Specify where you're going (e.g., office, cafe, party)
4. Choose your style preference
5. Describe your mood
6. Get an AI-powered recommendation based on current weather!
7. See similar outfits from our collection
8. Save your favorite combinations

### Saved Outfits
- View all your saved outfit combinations
- See the weather conditions and location for each saved outfit
- Build your personal style collection

## 🏗️ Project Structure

```
StyleSanctuary/
├── app.py              # FastAPI web application
├── main.py             # Original CLI version
├── agent.py            # AI recommendation logic
├── weather.py          # Weather API integration
├── config.py           # Configuration (API keys, settings)
├── requirements.txt    # Python dependencies
├── data/
│   ├── outfits.json   # Pre-designed outfit dataset
│   └── saved_outfits.json  # User-saved outfits
├── static/
│   ├── css/
│   │   └── style.css  # Modern styling
│   └── js/
│       └── main.js    # Frontend JavaScript
└── templates/
    ├── base.html      # Base template
    ├── index.html     # Home page
    ├── browse.html    # Browse outfits
    ├── recommend.html # Get recommendations
    └── saved.html     # Saved outfits
```

## 🛠️ Technologies Used

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI**: Ollama (qwen2.5:7b-instruct model)
- **Weather API**: OpenWeatherMap
- **Styling**: Modern CSS with gradients, animations, and responsive design

## 🎨 Design Philosophy

The UI design is inspired by modern web design trends from [21st.dev](https://21st.dev/community/components), featuring:
- Clean, minimalist interface
- Smooth animations and transitions
- Gradient backgrounds
- Card-based layouts
- Responsive grid system
- Intuitive navigation
- Accessible color schemes

## 📝 Original CLI Version

The project includes the original command-line interface version in `main.py`. You can still use it:

```bash
python main.py
```

## 🤝 Contributing

This is an open-source project shared on GitHub. Feel free to:
- Fork the repository
- Add new features
- Improve the design
- Add more outfit suggestions
- Enhance the AI recommendations

## 📄 License

This project is created by Okay Büyükdeveci and is open for educational and personal use.

## 🙏 Acknowledgments

- Weather data from OpenWeatherMap
- AI powered by Ollama
- Design inspiration from 21st.dev community
- Placeholder images from placeholder.com

## 📧 Contact

Created by Okay Büyükdeveci

---

**Enjoy your personalized fashion experience! 👗✨**