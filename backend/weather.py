# weather.py
import requests
from config import WEATHER_API_KEY

def get_weather(city: str) -> dict:
    """
    Fetch weather data for a given city
    
    Args:
        city: Name of the city
        
    Returns:
        Dictionary with city, temperature, and condition
        
    Raises:
        ValueError: If city is not found or API key is invalid
        ConnectionError: If unable to connect to the API
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "en"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"]
        }
    except requests.exceptions.Timeout:
        raise ConnectionError(f"Request timeout while fetching weather for {city}")
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Unable to connect to weather API")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid API key. Please check your WEATHER_API_KEY in .env")
        elif e.response.status_code == 404:
            raise ValueError(f"City '{city}' not found")
        else:
            raise ValueError(f"Weather API error: {e}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid response from weather API: {e}")
