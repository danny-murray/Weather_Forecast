'''     Dan's Weather forcast app - 3 day forecast based on city or postcode    '''

import requests
import urllib3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Disabling SSL verifications to avoid warnings when making API requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Retrieves weather data from the Weather API for a given location
def get_weather_data(location):
    api_key = get_api_key()
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3&aqi=no"
    response = requests.get(url, verify=False)
    try:
        response.raise_for_status()  # Raises exception if API response is unsuccessful
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Error occurred while retrieving weather data.") from e

# Extracts relevant weather info and displays as forecast
def display_weather_forecast(weather_data):
    location = weather_data['location']['name']
    forecast_message = f"Weather forecast for {location}:\n\n"
    for day in weather_data['forecast']['forecastday']:
        date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A, %d %B %Y')
        temperature = day['day']['avgtemp_c']
        humidity = day['day']['avghumidity']
        forecast_message += f"Date: {date}\n"
        forecast_message += f"Temperature: {temperature}°C\n"
        forecast_message += f"Humidity: {humidity}%\n\n"

    # Forecast results window
    forecast_window = tk.Toplevel()
    forecast_window.title("Your Weather Forecast")
    forecast_window.geometry("400x250")  # Window size
    forecast_window.configure(bg="#333333")  # Background colour

    # Create a label to display the forecast message
    forecast_label = tk.Label(forecast_window, text=forecast_message, font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    forecast_label.pack(pady=10)

# Retrieves the API key from api_key.txt
def get_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

# Retrieves weather data for location and displays forecast
def retrieve_and_display_weather(location):
    try:
        weather_data = get_weather_data(location)
        display_weather_forecast(weather_data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", "Error occurred while retrieving weather data.")
    except (KeyError, ValueError) as e:
        messagebox.showerror("Error", "Invalid API response. Please check your API key.")

# GUI for the weather forecast app
def create_gui():
    def on_submit():
        location = entry.get()
        retrieve_and_display_weather(location)
        entry.delete(0, tk.END)
    root = tk.Tk()
    root.title("Weather Forecast App")

    # Size configuration of root window
    root.geometry("400x150")

    # Widget style
    root.configure(bg="#333333")  # Background colour
    label_font = ("Arial", 14, "bold")  # Label font
    entry_font = ("Arial", 12)  # Input font
    button_font = ("Arial", 12, "bold")  # Button font
    label = tk.Label(root, text="Enter a location (city or post code):", font=label_font, fg="#FFFFFF", bg="#333333")
    label.pack(pady=10)
    entry = tk.Entry(root, font=entry_font, width=30)
    entry.pack(pady=10)
    button = tk.Button(root, text="Submit", font=button_font, command=on_submit, fg="#FFFFFF", bg="#555555")
    button.pack(pady=10)
    root.mainloop()

if __name__ == '__main__':
    create_gui()