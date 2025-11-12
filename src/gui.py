"""
Weather Dashboard GUI
Graphical user interface for the weather dashboard
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from src.dashboard import WeatherDashboard
from src.alerts import TemperatureAlerts
from src.analyzer import WeatherAnalyzer


class WeatherDashboardGUI:
    """Main GUI window for the weather dashboard"""

    def __init__(self, root):
        """
        Initialize the GUI

        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("🌤️ Weather Dashboard")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Initialize weather services
        self.dashboard = WeatherDashboard()
        self.alerts = TemperatureAlerts(min_temp=15, max_temp=25)
        self.analyzer = WeatherAnalyzer(preferred_temp_min=15, preferred_temp_max=25)

        # Load cities
        self.cities = self.load_cities()

        # Create GUI components
        self.create_widgets()

    def load_cities(self):
        """Load cities from JSON file"""
        try:
            with open("data/cities.json", "r") as f:
                data = json.load(f)
                return data["cities"]
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not load cities: {e}\nUsing defaults.")
            return ["London", "New York", "Tokyo", "Paris", "Sydney"]

    def create_widgets(self):
        """Create all GUI widgets"""

        # Configure colors
        bg_color = "#f0f0f0"
        button_color = "#4CAF50"
        self.root.configure(bg=bg_color)

        # ===== HEADER =====
        header_frame = tk.Frame(self.root, bg="#2196F3", pady=15)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="🌤️ Weather Dashboard",
            font=("Arial", 24, "bold"),
            bg="#2196F3",
            fg="white"
        )
        header_label.pack()

        # ===== CONTROL PANEL =====
        control_frame = tk.Frame(self.root, bg=bg_color, pady=20)
        control_frame.pack(fill="x", padx=20)

        # City selection
        city_label = tk.Label(
            control_frame,
            text="Select City:",
            font=("Arial", 12, "bold"),
            bg=bg_color
        )
        city_label.pack(side="left", padx=10)

        self.city_var = tk.StringVar(value=self.cities[0])
        self.city_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.city_var,
            values=self.cities,
            state="readonly",
            font=("Arial", 11),
            width=20
        )
        self.city_dropdown.pack(side="left", padx=10)

        # Add custom city button
        add_city_btn = tk.Button(
            control_frame,
            text="+ Add City",
            command=self.add_custom_city,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        add_city_btn.pack(side="left", padx=10)

        # ===== BUTTON PANEL =====
        button_frame = tk.Frame(self.root, bg=bg_color, pady=10)
        button_frame.pack(fill="x", padx=20)

        # Create buttons for different features
        buttons = [
            ("📍 Current Weather", self.show_current_weather, "#4CAF50"),
            ("📅 5-Day Forecast", self.show_forecast, "#2196F3"),
            ("🚨 Temperature Alerts", self.show_alerts, "#FF5722"),
            ("⭐ Best Day", self.show_best_day, "#9C27B0"),
            ("🌍 Compare Cities", self.show_comparison, "#FF9800")
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 11, "bold"),
                padx=15,
                pady=10,
                relief="flat",
                cursor="hand2",
                activebackground=color,
                activeforeground="white"
            )
            btn.pack(side="left", padx=5, expand=True, fill="x")

        # ===== DISPLAY AREA =====
        display_frame = tk.Frame(self.root, bg=bg_color, pady=10)
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrolled text widget for output
        self.output_text = scrolledtext.ScrolledText(
            display_frame,
            font=("Courier New", 10),
            bg="white",
            fg="black",
            wrap="word",
            padx=15,
            pady=15,
            relief="solid",
            borderwidth=1
        )
        self.output_text.pack(fill="both", expand=True)

        # Welcome message
        self.display_welcome_message()

        # ===== FOOTER =====
        footer_frame = tk.Frame(self.root, bg="#2196F3", pady=10)
        footer_frame.pack(fill="x", side="bottom")

        footer_label = tk.Label(
            footer_frame,
            text="Weather Dashboard v1.0 | Data from OpenWeatherMap",
            font=("Arial", 9),
            bg="#2196F3",
            fg="white"
        )
        footer_label.pack()

    def display_welcome_message(self):
        """Display welcome message in the output area"""
        welcome = """
        ╔════════════════════════════════════════════════════════════════╗
        ║                  WELCOME TO WEATHER DASHBOARD                 ║
        ╚════════════════════════════════════════════════════════════════╝

        👋 Hello! Welcome to your personal weather dashboard.

        📍 SELECT A CITY from the dropdown above
        🔘 CLICK A BUTTON to view weather information

        Features:
        • 📍 Current Weather - See current conditions
        • 📅 5-Day Forecast - Plan ahead with forecasts
        • 🚨 Temperature Alerts - Get comfort zone warnings
        • ⭐ Best Day - Find the perfect day this week
        • 🌍 Compare Cities - Compare weather across cities

        Ready to explore the weather? Choose a city and get started! 🌤️
        """
        self.update_output(welcome)

    def update_output(self, text):
        """
        Update the output text area

        Args:
            text (str): Text to display
        """
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, text)
        self.output_text.config(state="disabled")

    def add_custom_city(self):
        """Add a custom city to the list"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add City")
        dialog.geometry("300x120")
        dialog.resizable(False, False)

        tk.Label(dialog, text="Enter city name:", font=("Arial", 11)).pack(pady=10)

        city_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        city_entry.pack(pady=5)
        city_entry.focus()

        def add_city():
            city = city_entry.get().strip()
            if city and city not in self.cities:
                self.cities.append(city)
                self.city_dropdown['values'] = self.cities
                self.city_var.set(city)
                messagebox.showinfo("Success", f"Added {city} to the list!")
                dialog.destroy()
            elif city in self.cities:
                messagebox.showwarning("Warning", f"{city} is already in the list!")
            else:
                messagebox.showerror("Error", "Please enter a city name!")

        add_btn = tk.Button(
            dialog,
            text="Add",
            command=add_city,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=20,
            pady=5
        )
        add_btn.pack(pady=10)

        # Allow Enter key to submit
        city_entry.bind("<Return>", lambda e: add_city())

    def show_current_weather(self):
        """Display current weather for selected city"""
        city = self.city_var.get()
        try:
            weather = self.dashboard.weather_service.get_current_weather_formatted(city)

            output = f"""
╔════════════════════════════════════════════════════════════════╗
║                    CURRENT WEATHER                             ║
╚════════════════════════════════════════════════════════════════╝

📍 {weather['city'].upper()}, {weather['country']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌡️  Temperature
   Current: {weather['temperature']}°C
   Feels like: {weather['feels_like']}°C
   Range: {weather['temp_min']}°C - {weather['temp_max']}°C

☁️  Conditions
   {weather['description']}

💧 Humidity
   {weather['humidity']}%

💨 Wind
   Speed: {weather['wind_speed']} m/s

☁️  Cloud Cover
   {weather['clouds']}%

🕐 Last Updated
   {weather['timestamp']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            self.update_output(output)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch weather data:\n{e}")

    def show_forecast(self):
        """Display 5-day forecast for selected city"""
        city = self.city_var.get()
        try:
            daily_summary = self.dashboard.weather_service.get_daily_summary(city)

            output = f"""
╔════════════════════════════════════════════════════════════════╗
║                     5-DAY FORECAST                             ║
╚════════════════════════════════════════════════════════════════╝

📍 {city.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
            for day in daily_summary:
                output += f"""
📅 {day['date']}
   🌡️  Temperature: {day['temp_min']}°C - {day['temp_max']}°C (avg: {day['temp_avg']}°C)
   ☁️  Conditions: {day['description']}
   💧 Rain Probability: {day['rain_probability']:.0f}%
   💨 Max Wind: {day['max_wind_speed']} m/s
   💧 Humidity: {day['avg_humidity']:.0f}%
"""

            output += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            self.update_output(output)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch forecast data:\n{e}")

    def show_alerts(self):
        """Display temperature alerts for selected city"""
        city = self.city_var.get()
        try:
            current_alert = self.alerts.check_current_temperature(city)
            forecast_alerts = self.alerts.check_forecast_alerts(city)
            comfortable_days = self.alerts.find_comfortable_days(city)

            output = f"""
╔════════════════════════════════════════════════════════════════╗
║                    TEMPERATURE ALERTS                          ║
╚════════════════════════════════════════════════════════════════╝

📍 {city.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  Comfortable Range: {self.alerts.min_comfortable_temp}°C - {self.alerts.max_comfortable_temp}°C

📍 CURRENT STATUS
   {current_alert['message']}

"""

            if forecast_alerts:
                output += "📅 UPCOMING ALERTS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                for day_alert in forecast_alerts:
                    output += f"\n{day_alert['date']}:\n"
                    for alert in day_alert['alerts']:
                        output += f"   {alert}\n"
            else:
                output += "✅ NO ALERTS\n   All forecast days are within your comfort zone!\n"

            if comfortable_days:
                output += "\n\n😊 COMFORTABLE DAYS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                for day in comfortable_days:
                    output += f"\n{day['date']}: {day['temp_min']}°C - {day['temp_max']}°C "
                    output += f"(avg: {day['temp_avg']}°C)\n   {day['description']}\n"

            output += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            self.update_output(output)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch alert data:\n{e}")

    def show_best_day(self):
        """Display best day recommendation for selected city"""
        city = self.city_var.get()
        try:
            result = self.analyzer.find_best_day(city)

            if 'error' in result:
                messagebox.showerror("Error", result['error'])
                return

            weather = result['weather']

            output = f"""
╔════════════════════════════════════════════════════════════════╗
║                   BEST DAY RECOMMENDATION                      ║
╚════════════════════════════════════════════════════════════════╝

📍 {city.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  Preferred Temperature: {self.analyzer.preferred_temp_min}°C - {self.analyzer.preferred_temp_max}°C

🏆 BEST DAY: {result['date']}
   Score: {result['score']:.1f}/100

   🌡️  Temperature: {weather['temp_min']}°C - {weather['temp_max']}°C (avg: {weather['temp_avg']}°C)
   ☁️  Conditions: {weather['description']}
   💧 Rain Probability: {weather['rain_probability']:.0f}%
   💨 Max Wind Speed: {weather['max_wind_speed']} m/s

📝 WHY THIS DAY?
"""
            for reason in result['reasoning']:
                output += f"   {reason}\n"

            output += "\n\n📊 ALL DAYS RANKED\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            for i, day in enumerate(result['all_days'], 1):
                rank = f"#{i}"
                if i == 1:
                    rank = "🥇 #1"
                elif i == 2:
                    rank = "🥈 #2"
                elif i == 3:
                    rank = "🥉 #3"

                output += f"{rank}  {day['date']}  |  Score: {day['score']:.1f}/100\n"
                output += f"      {day['data']['temp_min']}°C - {day['data']['temp_max']}°C  |  "
                output += f"{day['data']['description']}  |  Rain: {day['data']['rain_probability']:.0f}%\n\n"

            output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            self.update_output(output)
        except Exception as e:
            messagebox.showerror("Error", f"Could not analyze forecast:\n{e}")

    def show_comparison(self):
        """Display comparison of all cities"""
        try:
            output = """
╔════════════════════════════════════════════════════════════════╗
║                    CITY COMPARISON                             ║
╚════════════════════════════════════════════════════════════════╝

🌍 TEMPERATURE COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

            for city in self.cities:
                try:
                    weather = self.dashboard.weather_service.get_current_weather_formatted(city)
                    output += f"\n📍 {weather['city']}, {weather['country']}\n"
                    output += f"   🌡️  {weather['temperature']}°C (feels like {weather['feels_like']}°C)\n"
                    output += f"   ☁️  {weather['description']}\n"
                    output += f"   💧 Humidity: {weather['humidity']}%  |  💨 Wind: {weather['wind_speed']} m/s\n"
                except Exception as e:
                    output += f"\n📍 {city}\n   ❌ Error: {str(e)[:50]}\n"

            output += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            self.update_output(output)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch comparison data:\n{e}")


def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = WeatherDashboardGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()