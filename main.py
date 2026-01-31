# main.py
from backend.weather import get_weather
from backend.agent import get_outfit_recommendation

def main():
    print("\n" + "=" * 50)
    print("   WEATHER FIT AGENT")
    print("   Okay Büyükdeveci")
    print("=" * 50 + "\n")

    city = input("Which city are you in? (e.g., London): ").strip()
    gender = input("What is your gender? (Male / Female / Other): ").strip()
    event = input("Where will you go? (e.g., School, Cafe, Market, Office): ").strip()
    style = input("What's your style? (e.g., Sporty, Classic, Minimalist, Casual): ").strip()
    mood = input("How do you feel today? (e.g., Energetic, Tired, Relaxed, Happy): ").strip()

    print(f"\n Weather data is being collected for {city}...\n")

    weather = get_weather(city)

    print(
        f"Weather information received.: {weather['temperature']}°C, "
        f"{weather['condition'].title()} \n"
    )

    print(" Your outfit is being created...\n")

    context = {
        "gender": gender,
        "event": event,
        "style": style,
        "mood": mood
    }

    outfit = get_outfit_recommendation(weather, context)

    print("=" * 40)
    print(f" Our suggestions for you ({city}) ")
    print("=" * 40 + "\n")

    print(outfit)
    print("\nHave a Nice Day! ☀️")

if __name__ == "__main__":
    main()
