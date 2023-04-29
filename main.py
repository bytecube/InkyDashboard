from config.config import SCREEN_SIZE, WEATHER_API_ENDPOINT, JOKE_API_ENDPOINT
from modules.helper import save_dashboard
from modules.dashboards.joke_dashboard import generate_joke_dashboard
from modules.dashboards.calendar_dashboard import generate_calendar_dashboard
from modules.dashboards.weather_dashboard import generate_weather_dashboard

# Generate the dashboards
save_dashboard(button=1, dashboard_img=generate_weather_dashboard(api_endpoint=WEATHER_API_ENDPOINT, screen_size=SCREEN_SIZE))
save_dashboard(button=2, dashboard_img=generate_calendar_dashboard(screen_size=SCREEN_SIZE))
save_dashboard(button=3, dashboard_img=generate_joke_dashboard(api_endpoint=JOKE_API_ENDPOINT, screen_size=SCREEN_SIZE))
