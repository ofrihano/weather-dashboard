"""
API Client for OpenWeatherMap
Handles all HTTP requests to the weather API
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class WeatherAPIClient:
    """Client for interacting with OpenWeatherMap API"""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self):
        """Initialize the API client with API key from environment variables"""
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY not found in environment variables")

    def get_current_weather(self, city: str) -> dict:
        """
        Fetch current weather data for a specific city

        Args:
            city (str): Name of the city

        Returns:
            dict: Weather data from API

        Raises:
            requests.RequestException: If API request fails
        """
        endpoint = f"{self.BASE_URL}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Use Celsius
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"City '{city}' not found")
            elif response.status_code == 401:
                raise ValueError("Invalid API key")
            else:
                raise Exception(f"HTTP Error: {e}")

        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout for city '{city}'")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching weather data: {e}")

    def get_forecast(self, city: str) -> dict:
        """
        Fetch 5-day weather forecast for a specific city

        Args:
            city (str): Name of the city

        Returns:
            dict: Forecast data from API

        Raises:
            requests.RequestException: If API request fails
        """
        endpoint = f"{self.BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"City '{city}' not found")
            elif response.status_code == 401:
                raise ValueError("Invalid API key")
            else:
                raise Exception(f"HTTP Error: {e}")

        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout for city '{city}'")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching forecast data: {e}")


# For testing purposes
if __name__ == "__main__":
    # This code only runs when you execute this file directly
    try:
        client = WeatherAPIClient()

        # Test with a city
        print("Testing API Client...")
        print("=" * 50)
        print("Enter a city:")
        city = input()
        weather = client.get_current_weather(city)
        print(f"\n✅ Current Weather in {city}:")
        print(f"   Temperature: {weather['main']['temp']}°C")
        print(f"   Conditions: {weather['weather'][0]['description']}")
        print(f"   Humidity: {weather['main']['humidity']}%")

    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")