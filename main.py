"""
Weather Dashboard - Main Entry Point
"""

import json
from src.dashboard import WeatherDashboard
from src.alerts import TemperatureAlerts


def load_cities():
    """Load cities from the JSON file"""
    try:
        with open("data/cities.json", "r") as f:
            data = json.load(f)
            return data["cities"]
    except FileNotFoundError:
        print("⚠️  cities.json not found. Using default cities.")
        return ["London", "New York", "Tokyo"]
    except Exception as e:
        print(f"⚠️  Error loading cities: {e}")
        return ["London", "New York", "Tokyo"]


def main():
    """Main function to run the weather dashboard"""
    dashboard = WeatherDashboard()
    alerts_system = TemperatureAlerts(min_temp=15, max_temp=25)

    # Load cities from config file
    cities = load_cities()

    # Display full report for the first city
    dashboard.display_full_report(cities[0])

    # Display temperature alerts for the first city
    alerts_system.display_alerts(cities[0])

    # Display comparison for all cities
    print("\n")
    dashboard.display_comparison(cities)

    print("\n✨ Thank you for using Weather Dashboard!")


if __name__ == "__main__":
    main()