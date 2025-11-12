"""
Weather Dashboard
Displays weather information in a formatted, user-friendly way
"""

from src.weather_service import WeatherService


class WeatherDashboard:
    """Main dashboard for displaying weather information"""

    def __init__(self):
        """Initialize the dashboard with weather service"""
        self.weather_service = WeatherService()

    def display_header(self):
        """Display the dashboard header"""
        print("\n" + "=" * 70)
        print("                    🌤️  WEATHER DASHBOARD  🌤️")
        print("=" * 70)

    def display_current_weather(self, city: str):
        """
        Display current weather for a city

        Args:
            city (str): Name of the city
        """
        try:
            weather = self.weather_service.get_current_weather_formatted(city)

            print(f"\n📍 {weather['city'].upper()}, {weather['country']}")
            print("━" * 70)
            print(f"🌡️  Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)")
            print(f"    Range: {weather['temp_min']}°C - {weather['temp_max']}°C")
            print(f"☁️  Conditions: {weather['description']}")
            print(f"💧 Humidity: {weather['humidity']}%")
            print(f"💨 Wind Speed: {weather['wind_speed']} m/s")
            print(f"🕐 Updated: {weather['timestamp']}")

        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

    def display_forecast(self, city: str):
        """
        Display 5-day forecast summary for a city

        Args:
            city (str): Name of the city
        """
        try:
            daily_summary = self.weather_service.get_daily_summary(city)

            print(f"\n📅 5-DAY FORECAST")
            print("━" * 70)
            print(f"{'Date':<12} | {'Temperature':<15} | {'Conditions':<20} | Rain")
            print("-" * 70)

            for day in daily_summary:
                temp_range = f"{day['temp_min']}°C - {day['temp_max']}°C"
                rain_icon = "💧" if day['rain_probability'] > 30 else "☀️"

                print(
                    f"{day['date']:<12} | {temp_range:<15} | {day['description']:<20} | {rain_icon} {day['rain_probability']:.0f}%")

        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

    def display_full_report(self, city: str):
        """
        Display complete weather report (current + forecast)

        Args:
            city (str): Name of the city
        """
        self.display_header()
        self.display_current_weather(city)
        self.display_forecast(city)
        print("\n" + "=" * 70 + "\n")

    def display_multiple_cities(self, cities: list):
        """
        Display weather for multiple cities

        Args:
            cities (list): List of city names
        """
        self.display_header()

        for city in cities:
            self.display_current_weather(city)

        print("\n" + "=" * 70 + "\n")

    def display_comparison(self, cities: list):
        """
        Display a temperature comparison table for multiple cities

        Args:
            cities (list): List of city names
        """
        print("\n🌍 TEMPERATURE COMPARISON")
        print("━" * 70)
        print(f"{'City':<20} | {'Current Temp':<15} | {'Feels Like':<15} | Conditions")
        print("-" * 70)

        for city in cities:
            try:
                weather = self.weather_service.get_current_weather_formatted(city)
                city_name = f"{weather['city']}, {weather['country']}"
                temp = f"{weather['temperature']}°C"
                feels = f"{weather['feels_like']}°C"

                print(f"{city_name:<20} | {temp:<15} | {feels:<15} | {weather['description']}")

            except Exception as e:
                print(f"{city:<20} | ❌ Error: {str(e)[:40]}")

        print("-" * 70)


# For testing purposes
if __name__ == "__main__":
    dashboard = WeatherDashboard()

    print("\n🧪 Testing Dashboard Display...\n")

    # Test 1: Full report for one city
    print("TEST 1: Full Weather Report")
    dashboard.display_full_report("London")

    # Test 2: Multiple cities current weather
    print("\nTEST 2: Multiple Cities")
    cities = ["London", "New York", "Tokyo"]
    dashboard.display_multiple_cities(cities)

    # Test 3: Temperature comparison
    print("\nTEST 3: Temperature Comparison")
    dashboard.display_comparison(cities)

    print("✅ Dashboard test completed!")