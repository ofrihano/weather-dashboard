"""
Weather Analyzer
Analyzes forecast data to recommend the best days for activities
"""

from src.weather_service import WeatherService


class WeatherAnalyzer:
    """Analyzes weather patterns and recommends best days"""

    def __init__(self, preferred_temp_min=15, preferred_temp_max=25):
        """
        Initialize the analyzer with temperature preferences

        Args:
            preferred_temp_min (float): Minimum preferred temperature (°C)
            preferred_temp_max (float): Maximum preferred temperature (°C)
        """
        self.weather_service = WeatherService()
        self.preferred_temp_min = preferred_temp_min
        self.preferred_temp_max = preferred_temp_max

    def calculate_day_score(self, day_data: dict) -> float:
        """
        Calculate a score for a day based on weather conditions
        Score ranges from 0 (worst) to 100 (perfect)

        Args:
            day_data (dict): Daily weather summary

        Returns:
            float: Score for the day
        """
        score = 100.0  # Start with perfect score

        # Temperature scoring (40 points max)
        temp_avg = day_data['temp_avg']
        preferred_temp_avg = (self.preferred_temp_min + self.preferred_temp_max) / 2

        # Penalize if temperature is outside preferred range
        if temp_avg < self.preferred_temp_min:
            # Too cold
            diff = self.preferred_temp_min - temp_avg
            score -= min(diff * 2, 40)  # Lose up to 40 points for being too cold
        elif temp_avg > self.preferred_temp_max:
            # Too hot
            diff = temp_avg - self.preferred_temp_max
            score -= min(diff * 2, 40)  # Lose up to 40 points for being too hot
        else:
            # Within range - bonus for being close to ideal
            diff = abs(temp_avg - preferred_temp_avg)
            score -= diff * 1  # Small penalty for being away from ideal

        # Rain probability scoring (30 points max)
        rain_prob = day_data['rain_probability']
        if rain_prob > 70:
            score -= 30  # Heavy rain likely
        elif rain_prob > 50:
            score -= 20  # Moderate rain likely
        elif rain_prob > 30:
            score -= 10  # Light rain possible
        elif rain_prob > 10:
            score -= 5  # Very light rain possible
        # else: no penalty for low rain probability

        # Wind speed scoring (15 points max)
        wind_speed = day_data['max_wind_speed']
        if wind_speed > 15:
            score -= 15  # Very windy
        elif wind_speed > 10:
            score -= 10  # Windy
        elif wind_speed > 7:
            score -= 5  # Breezy
        # else: calm, no penalty

        # Humidity scoring (15 points max)
        humidity = day_data['avg_humidity']
        if humidity > 85:
            score -= 15  # Very humid
        elif humidity > 70:
            score -= 8  # Humid
        elif humidity < 30:
            score -= 5  # Very dry
        # else: comfortable humidity

        # Ensure score doesn't go below 0
        return max(score, 0)

    def find_best_day(self, city: str) -> dict:
        """
        Find the best day in the forecast for outdoor activities

        Args:
            city (str): Name of the city

        Returns:
            dict: Information about the best day including score and reasoning
        """
        try:
            daily_summary = self.weather_service.get_daily_summary(city)

            if not daily_summary:
                return {'error': 'No forecast data available'}

            # Score each day
            scored_days = []
            for day in daily_summary:
                score = self.calculate_day_score(day)
                scored_days.append({
                    'date': day['date'],
                    'score': score,
                    'data': day
                })

            # Find the best day (highest score)
            best_day = max(scored_days, key=lambda x: x['score'])

            # Generate reasoning
            reasoning = self._generate_reasoning(best_day['data'], best_day['score'])

            return {
                'date': best_day['date'],
                'score': best_day['score'],
                'weather': best_day['data'],
                'reasoning': reasoning,
                'all_days': scored_days
            }

        except Exception as e:
            return {'error': f"Error analyzing forecast: {e}"}

    def _generate_reasoning(self, day_data: dict, score: float) -> list:
        """
        Generate human-readable reasoning for the day's score

        Args:
            day_data (dict): Weather data for the day
            score (float): Calculated score

        Returns:
            list: List of reasoning points
        """
        reasons = []

        # Temperature reasoning
        temp_avg = day_data['temp_avg']
        if self.preferred_temp_min <= temp_avg <= self.preferred_temp_max:
            reasons.append(f"✅ Comfortable temperature: {temp_avg}°C")
        elif temp_avg < self.preferred_temp_min:
            reasons.append(f"❄️  Cooler than ideal: {temp_avg}°C")
        else:
            reasons.append(f"🔥 Warmer than ideal: {temp_avg}°C")

        # Rain reasoning
        rain_prob = day_data['rain_probability']
        if rain_prob < 10:
            reasons.append(f"☀️  Very low rain chance: {rain_prob:.0f}%")
        elif rain_prob < 30:
            reasons.append(f"🌤️  Low rain chance: {rain_prob:.0f}%")
        elif rain_prob < 50:
            reasons.append(f"⛅ Moderate rain chance: {rain_prob:.0f}%")
        else:
            reasons.append(f"🌧️  High rain chance: {rain_prob:.0f}%")

        # Wind reasoning
        wind = day_data['max_wind_speed']
        if wind < 5:
            reasons.append(f"🍃 Calm winds: {wind} m/s")
        elif wind < 10:
            reasons.append(f"💨 Light breeze: {wind} m/s")
        else:
            reasons.append(f"🌬️  Windy conditions: {wind} m/s")

        # Overall assessment
        if score >= 90:
            reasons.append("⭐ Perfect conditions for outdoor activities!")
        elif score >= 75:
            reasons.append("😊 Great day for being outside!")
        elif score >= 60:
            reasons.append("👍 Good day, though not perfect")
        elif score >= 40:
            reasons.append("🤔 Fair day with some challenges")
        else:
            reasons.append("⚠️  Challenging weather conditions")

        return reasons

    def compare_days(self, city: str) -> list:
        """
        Compare all days in the forecast with scores

        Args:
            city (str): Name of the city

        Returns:
            list: All days with scores, sorted by score (best first)
        """
        try:
            daily_summary = self.weather_service.get_daily_summary(city)

            scored_days = []
            for day in daily_summary:
                score = self.calculate_day_score(day)
                scored_days.append({
                    'date': day['date'],
                    'score': round(score, 1),
                    'temp_avg': day['temp_avg'],
                    'temp_range': f"{day['temp_min']}°C - {day['temp_max']}°C",
                    'rain_prob': day['rain_probability'],
                    'description': day['description']
                })

            # Sort by score (highest first)
            scored_days.sort(key=lambda x: x['score'], reverse=True)

            return scored_days

        except Exception as e:
            return []

    def display_best_day_recommendation(self, city: str):
        """
        Display the best day recommendation in a formatted way

        Args:
            city (str): Name of the city
        """
        print(f"\n⭐ BEST DAY RECOMMENDATION FOR {city.upper()}")
        print("━" * 70)
        print(f"Preferred temperature range: {self.preferred_temp_min}°C - {self.preferred_temp_max}°C")
        print()

        result = self.find_best_day(city)

        if 'error' in result:
            print(f"❌ {result['error']}")
            return

        # Display best day
        weather = result['weather']
        print(f"🏆 BEST DAY: {result['date']}")
        print(f"   Score: {result['score']:.1f}/100")
        print()
        print(f"   🌡️  Temperature: {weather['temp_min']}°C - {weather['temp_max']}°C "
              f"(avg: {weather['temp_avg']}°C)")
        print(f"   ☁️  Conditions: {weather['description']}")
        print(f"   💧 Rain Probability: {weather['rain_probability']:.0f}%")
        print(f"   💨 Max Wind Speed: {weather['max_wind_speed']} m/s")
        print()
        print("   📝 Why this day?")
        for reason in result['reasoning']:
            print(f"      {reason}")

        # Display comparison table
        print(f"\n📊 ALL DAYS COMPARISON:")
        print("-" * 70)
        print(f"{'Rank':<6} | {'Date':<12} | {'Score':<8} | {'Temp Range':<18} | Rain | Conditions")
        print("-" * 70)

        for i, day in enumerate(result['all_days'], 1):
            rank = f"#{i}"
            score_str = f"{day['score']:.1f}/100"
            temp_range = f"{day['data']['temp_min']}°C - {day['data']['temp_max']}°C"
            rain = f"{day['data']['rain_probability']:.0f}%"

            # Add medal emoji for top 3
            if i == 1:
                rank = "🥇 #1"
            elif i == 2:
                rank = "🥈 #2"
            elif i == 3:
                rank = "🥉 #3"

            print(
                f"{rank:<6} | {day['date']:<12} | {score_str:<8} | {temp_range:<18} | {rain:<4} | {day['data']['description']}")


# For testing purposes
if __name__ == "__main__":
    print("🧪 Testing Weather Analyzer...\n")

    # Create analyzer with preferred temperature range
    analyzer = WeatherAnalyzer(preferred_temp_min=15, preferred_temp_max=25)

    # Test with a city
    city = "London"

    print("TEST 1: Find Best Day")
    print("=" * 70)
    best_day = analyzer.find_best_day(city)

    if 'error' not in best_day:
        print(f"Best Day: {best_day['date']}")
        print(f"Score: {best_day['score']:.1f}/100")
        print(f"\nReasons:")
        for reason in best_day['reasoning']:
            print(f"  {reason}")
    else:
        print(f"Error: {best_day['error']}")

    print("\n" + "=" * 70 + "\n")

    # Test full display
    analyzer.display_best_day_recommendation(city)

    print("\n" + "=" * 70)
    print("✅ Weather Analyzer test completed!")