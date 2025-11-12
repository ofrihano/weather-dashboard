"""
Temperature Alerts System
Monitors weather conditions and alerts users about temperature extremes
"""

from src.weather_service import WeatherService


class TemperatureAlerts:
    """System for monitoring temperature alerts and preferences"""

    def __init__(self, min_temp=15, max_temp=25):
        """
        Initialize alerts with temperature preferences

        Args:
            min_temp (float): Minimum comfortable temperature (°C)
            max_temp (float): Maximum comfortable temperature (°C)
        """
        self.weather_service = WeatherService()
        self.min_comfortable_temp = min_temp
        self.max_comfortable_temp = max_temp

    def check_current_temperature(self, city: str) -> dict:
        """
        Check if current temperature is within comfortable range

        Args:
            city (str): Name of the city

        Returns:
            dict: Alert information with status and message
        """
        try:
            weather = self.weather_service.get_current_weather_formatted(city)
            temp = weather['temperature']

            alert = {
                'city': weather['city'],
                'temperature': temp,
                'status': 'comfortable',
                'message': '✅ Temperature is comfortable',
                'severity': 'none'
            }

            # Check if too cold
            if temp < self.min_comfortable_temp:
                diff = self.min_comfortable_temp - temp
                alert['status'] = 'too_cold'
                alert['severity'] = 'high' if diff > 10 else 'medium'
                alert['message'] = f"❄️  COLD ALERT: {temp}°C is {diff:.1f}°C below comfortable range"

            # Check if too hot
            elif temp > self.max_comfortable_temp:
                diff = temp - self.max_comfortable_temp
                alert['status'] = 'too_hot'
                alert['severity'] = 'high' if diff > 10 else 'medium'
                alert['message'] = f"🔥 HEAT ALERT: {temp}°C is {diff:.1f}°C above comfortable range"

            # Check for extreme conditions
            if temp < 0:
                alert['severity'] = 'extreme'
                alert['message'] = f"⚠️  EXTREME COLD: {temp}°C - Freezing conditions!"
            elif temp > 35:
                alert['severity'] = 'extreme'
                alert['message'] = f"⚠️  EXTREME HEAT: {temp}°C - Very hot conditions!"

            return alert

        except Exception as e:
            return {
                'city': city,
                'status': 'error',
                'message': f"❌ Error checking temperature: {e}",
                'severity': 'none'
            }

    def check_forecast_alerts(self, city: str) -> list:
        """
        Check forecast for upcoming temperature alerts

        Args:
            city (str): Name of the city

        Returns:
            list: List of alerts for upcoming days
        """
        try:
            daily_summary = self.weather_service.get_daily_summary(city)
            alerts = []

            for day in daily_summary:
                day_alert = {
                    'date': day['date'],
                    'temp_min': day['temp_min'],
                    'temp_max': day['temp_max'],
                    'alerts': []
                }

                # Check minimum temperature
                if day['temp_min'] < self.min_comfortable_temp:
                    diff = self.min_comfortable_temp - day['temp_min']
                    day_alert['alerts'].append(
                        f"❄️  Morning cold: {day['temp_min']}°C ({diff:.1f}°C below comfortable)"
                    )

                # Check maximum temperature
                if day['temp_max'] > self.max_comfortable_temp:
                    diff = day['temp_max'] - self.max_comfortable_temp
                    day_alert['alerts'].append(
                        f"🔥 Afternoon heat: {day['temp_max']}°C ({diff:.1f}°C above comfortable)"
                    )

                # Check for extreme conditions
                if day['temp_min'] < 0:
                    day_alert['alerts'].append(f"⚠️  Freezing conditions expected!")

                if day['temp_max'] > 35:
                    day_alert['alerts'].append(f"⚠️  Extreme heat expected!")

                # Check for large temperature swings
                temp_range = day['temp_max'] - day['temp_min']
                if temp_range > 15:
                    day_alert['alerts'].append(
                        f"📊 Large temperature swing: {temp_range:.1f}°C variation"
                    )

                # Only add days with alerts
                if day_alert['alerts']:
                    alerts.append(day_alert)

            return alerts

        except Exception as e:
            return [{'date': 'error', 'alerts': [f"❌ Error: {e}"]}]

    def find_comfortable_days(self, city: str) -> list:
        """
        Find days in the forecast with comfortable temperatures

        Args:
            city (str): Name of the city

        Returns:
            list: Days with temperatures in comfortable range
        """
        try:
            daily_summary = self.weather_service.get_daily_summary(city)
            comfortable_days = []

            for day in daily_summary:
                # Check if the day's average temperature is comfortable
                if self.min_comfortable_temp <= day['temp_avg'] <= self.max_comfortable_temp:
                    # Also check that extremes aren't too bad
                    if day['temp_min'] >= (self.min_comfortable_temp - 5) and \
                            day['temp_max'] <= (self.max_comfortable_temp + 5):
                        comfortable_days.append({
                            'date': day['date'],
                            'temp_avg': day['temp_avg'],
                            'temp_min': day['temp_min'],
                            'temp_max': day['temp_max'],
                            'description': day['description'],
                            'rain_probability': day['rain_probability']
                        })

            return comfortable_days

        except Exception as e:
            return []

    def display_alerts(self, city: str):
        """
        Display all alerts for a city in a formatted way

        Args:
            city (str): Name of the city
        """
        print(f"\n🚨 TEMPERATURE ALERTS FOR {city.upper()}")
        print("━" * 70)
        print(f"Comfortable range: {self.min_comfortable_temp}°C - {self.max_comfortable_temp}°C")
        print()

        # Current temperature alert
        current_alert = self.check_current_temperature(city)
        print(f"📍 Current: {current_alert['message']}")

        # Forecast alerts
        forecast_alerts = self.check_forecast_alerts(city)

        if forecast_alerts:
            print(f"\n📅 Upcoming Alerts:")
            print("-" * 70)
            for day_alert in forecast_alerts:
                print(f"\n{day_alert['date']}:")
                for alert in day_alert['alerts']:
                    print(f"  {alert}")
        else:
            print(f"\n✅ No alerts in the forecast - all days look comfortable!")

        # Find comfortable days
        comfortable_days = self.find_comfortable_days(city)

        if comfortable_days:
            print(f"\n😊 COMFORTABLE DAYS:")
            print("-" * 70)
            for day in comfortable_days:
                print(f"{day['date']}: {day['temp_min']}°C - {day['temp_max']}°C "
                      f"(avg: {day['temp_avg']}°C) - {day['description']}")


# For testing purposes
if __name__ == "__main__":
    print("🧪 Testing Temperature Alerts System...\n")

    # Create alerts system with custom comfort range
    alerts = TemperatureAlerts(min_temp=15, max_temp=25)

    # Test with a city
    city = "London"

    print("TEST 1: Current Temperature Alert")
    print("=" * 70)
    current_alert = alerts.check_current_temperature(city)
    print(f"City: {current_alert['city']}")
    print(f"Temperature: {current_alert['temperature']}°C")
    print(f"Status: {current_alert['status']}")
    print(f"Message: {current_alert['message']}")
    print(f"Severity: {current_alert['severity']}")

    print("\n" + "=" * 70)

    # Test full display
    alerts.display_alerts(city)

    print("\n" + "=" * 70)
    print("✅ Temperature Alerts test completed!")