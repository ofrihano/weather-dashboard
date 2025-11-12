"""
Weather Dashboard - Main Entry Point
Can run in CLI or GUI mode
"""

import sys
from src.gui import main as gui_main


def main():
    """Main function - launches GUI by default"""

    # Check if user wants CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI version
        from src.dashboard import WeatherDashboard
        from src.alerts import TemperatureAlerts
        from src.analyzer import WeatherAnalyzer
        import json

        def load_cities():
            try:
                with open("data/cities.json", "r") as f:
                    data = json.load(f)
                    return data["cities"]
            except:
                return ["London", "New York", "Tokyo"]

        dashboard = WeatherDashboard()
        alerts_system = TemperatureAlerts(min_temp=15, max_temp=25)
        analyzer = WeatherAnalyzer(preferred_temp_min=15, preferred_temp_max=25)

        cities = load_cities()

        dashboard.display_full_report(cities[0])
        alerts_system.display_alerts(cities[0])
        analyzer.display_best_day_recommendation(cities[0])

        print("\n")
        dashboard.display_comparison(cities)
        print("\n✨ Thank you for using Weather Dashboard!")
    else:
        # Run GUI version (default)
        gui_main()


if __name__ == "__main__":
    main()