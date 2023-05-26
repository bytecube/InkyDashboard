import json
import os
from datetime import datetime

import requests
from PIL import ImageFont, Image, ImageDraw


from config.config import WEATHER_API_ENDPOINT
from modules.dashboard_generators.base_dashboard_generator import BaseDashboardGenerator
from modules.display_configuration import DisplayConfiguration


def parse_weather_forecast(response):
    forecasts = []
    for forecast_response in response["daily"]:
        forecast = {}

        date = datetime.fromtimestamp(forecast_response["dt"])
        forecast["date"] = date

        date_day = date.strftime("%a")
        forecast["day"] = date_day

        temperature_in_celsius = forecast_response["temp"]
        forecast["temperature"] = temperature_in_celsius

        weather = forecast_response["weather"]
        forecast["weather"] = weather

        clouds_in_percent = forecast_response["clouds"]
        forecast["clouds"] = clouds_in_percent

        try:
            rain_in_mm_per_hour = forecast_response["rain"]
            forecast["rain"] = rain_in_mm_per_hour
        except KeyError:
            pass
        forecasts.append(forecast)
    return forecasts


def get_weather_forecast(api_endpoint: str):
    api_response = json.loads(requests.get(api_endpoint + os.environ['API_KEY_OPENWEATHERMAP']).text)
    parsed_forecast = parse_weather_forecast(api_response)
    return parsed_forecast


class WeatherDashboardGenerator(BaseDashboardGenerator):

    def build_dashboard(self, button_assignment: int, display_configuration: DisplayConfiguration) -> Image:
        if os.environ['API_KEY_OPENWEATHERMAP'] is None:
            print(f"api_key_openweathermap is not defined, can't retrieve the weather forecast")
            return

        if WEATHER_API_ENDPOINT is None:
            print(f"api_endpoint is not defined, can't retrieve the weather forecast")
            return

        print(f"Generating weather dashboard")

        print(f"- Requesting weather forecast")
        forecast = get_weather_forecast(WEATHER_API_ENDPOINT)

        font_title = ImageFont.truetype('fonts/Arial.ttf', size=40)
        font_temperature = ImageFont.truetype("fonts/Arial.ttf", size=28)

        weather_icons = {
            "Rain": {"image": "icons/weather/wsymbol_0018_cloudy_with_heavy_rain.png"},
            "Clouds": {"image": "icons/weather/wsymbol_0003_white_cloud.png"},
            "Sun": {"image": "icons/weather/wsymbol_0001_sunny.png"},
            "Thunder": {"image": "icons/weather/wsymbol_0016_thundery_showers.png"},
            "Snow": {"image": "icons/weather/wsymbol_0012_heavy_snow_showers.png"},
            "Clear": {"image": "icons/weather/wsymbol_0001_sunny.png"},
        }

        img = Image.new('RGB', (display_configuration.width, display_configuration.height), color='black')
        draw = ImageDraw.Draw(img)

        x, y = 20, 20
        print(f"- Creating weather dashboard image")
        for i in range(5):
            draw.text((x, y), forecast[i]["day"].upper(),
                      font=font_title, fill='orange')

            icon_to_display = forecast[i]["weather"][0]["main"]
            img.paste(im=Image.open(weather_icons[icon_to_display]["image"]), box=(x - 5, y + 40))

            draw.text((x - 5, y + 130), str(round(forecast[i]["temperature"]
                                                  ["day"], 1)) + " °C", font=font_temperature, fill='aqua')
            x += 125

        return img
