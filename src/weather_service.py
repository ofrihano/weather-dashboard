"""
Weather Service
Processes weather data and provides clean, formatted information
"""

from datetime import datetime
from src.api_client import WeatherAPIClient


class WeatherService:
    """Service for processing and formatting weather data"""

    def __init__(self):
        """Initialize the weather service with API client"""
        self.api_client = WeatherAPIClient()

    def get_current_weather_formatted(self, city: str) -> dict:
        """
        Get current weather with clean, formatted data

        Args:
            city (str): Name of the city

        Returns:
            dict: Formatted weather information
        """
        try:
            # Fetch raw data from API
            raw_data = self.api_client.get_current_weather(city)

            # Extract and format the important information
            formatted = {
                "city": raw_data["name"],
                "country": raw_data["sys"]["country"],
                "temperature": round(raw_data["main"]["temp"], 1),
                "feels_like": round(raw_data["main"]["feels_like"], 1),
                "temp_min": round(raw_data["main"]["temp_min"], 1),
                "temp_max": round(raw_data["main"]["temp_max"], 1),
                "humidity": raw_data["main"]["humidity"],
                "pressure": raw_data["main"]["pressure"],
                "description": raw_data["weather"][0]["description"].title(),
                "wind_speed": raw_data["wind"]["speed"],
                "clouds": raw_data["clouds"]["all"],
                "timestamp": datetime.fromtimestamp(raw_data["dt"]).strftime("%Y-%m-%d %H:%M:%S")
            }

            return formatted

        except ValueError as e:
            raise ValueError(f"Error fetching weather for {city}: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: missing {e}")
        except Exception as e:
            raise Exception(f"Error processing weather data: {e}")

    def get_forecast_formatted(self, city: str) -> list:
        """
        Get 5-day forecast with formatted data

        Args:
            city (str): Name of the city

        Returns:
            list: List of forecast entries (every 3 hours)
        """
        try:
            # Fetch raw forecast data
            raw_data = self.api_client.get_forecast(city)

            forecast_list = []

            # Process each forecast entry (API returns data every 3 hours)
            for item in raw_data["list"]:
                forecast_entry = {
                    "datetime": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
                    "date": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d"),
                    "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                    "temperature": round(item["main"]["temp"], 1),
                    "feels_like": round(item["main"]["feels_like"], 1),
                    "temp_min": round(item["main"]["temp_min"], 1),
                    "temp_max": round(item["main"]["temp_max"], 1),
                    "humidity": item["main"]["humidity"],
                    "description": item["weather"][0]["description"].title(),
                    "wind_speed": item["wind"]["speed"],
                    "rain_probability": item.get("pop", 0) * 100  # Probability of precipitation
                }
                forecast_list.append(forecast_entry)

            return forecast_list

        except ValueError as e:
            raise ValueError(f"Error fetching forecast for {city}: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: missing {e}")
        except Exception as e:
            raise Exception(f"Error processing forecast data: {e}")

    def get_daily_summary(self, city: str) -> list:
        """
        Get a daily summary of the forecast (one entry per day)

        Args:
            city (str): Name of the city

        Returns:
            list: List of daily summaries with avg/min/max temperatures
        """
        try:
            forecast = self.get_forecast_formatted(city)

            # Group forecasts by date
            daily_data = {}
            for entry in forecast:
                date = entry["date"]
                if date not in daily_data:
                    daily_data[date] = {
                        "temperatures": [],
                        "descriptions": [],
                        "humidity": [],
                        "wind_speeds": [],
                        "rain_probabilities": []
                    }

                daily_data[date]["temperatures"].append(entry["temperature"])
                daily_data[date]["descriptions"].append(entry["description"])
                daily_data[date]["humidity"].append(entry["humidity"])
                daily_data[date]["wind_speeds"].append(entry["wind_speed"])
                daily_data[date]["rain_probabilities"].append(entry["rain_probability"])

            # Calculate daily summaries
            daily_summaries = []
            for date, data in daily_data.items():
                summary = {
                    "date": date,
                    "temp_avg": round(sum(data["temperatures"]) / len(data["temperatures"]), 1),
                    "temp_min": round(min(data["temperatures"]), 1),
                    "temp_max": round(max(data["temperatures"]), 1),
                    "avg_humidity": round(sum(data["humidity"]) / len(data["humidity"]), 1),
                    "max_wind_speed": round(max(data["wind_speeds"]), 1),
                    "rain_probability": round(max(data["rain_probabilities"]), 1),
                    # Most common weather description for the day
                    "description": max(set(data["descriptions"]), key=data["descriptions"].count)
                }
                daily_summaries.append(summary)

            return daily_summaries

        except Exception as e:
            raise Exception(f"Error creating daily summary: {e}")


# For testing purposes
if __name__ == "__main__":
    print("Testing Weather Service...")
    print("=" * 60)
    print("Please enter a city:")
    city = input()
    service = WeatherService()

    try:
        # Test 1: Current Weather
        print(f"\n📍 Current Weather in {city}:")
        print("-" * 60)
        weather = service.get_current_weather_formatted(city)
        print(f"City: {weather['city']}, {weather['country']}")
        print(f"Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)")
        print(f"Conditions: {weather['description']}")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind Speed: {weather['wind_speed']} m/s")
        print(f"Updated: {weather['timestamp']}")

        # Test 2: Daily Summary
        print("\n📅 5-Day Forecast Summary:")
        print("-" * 60)
        daily = service.get_daily_summary("London")
        for day in daily:
            print(f"\n{day['date']}:")
            print(f"  🌡️  Temperature: {day['temp_min']}°C - {day['temp_max']}°C (avg: {day['temp_avg']}°C)")
            print(f"  ☁️  Conditions: {day['description']}")
            print(f"  💧 Rain Probability: {day['rain_probability']}%")

        print("\n✅ Weather Service test completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")