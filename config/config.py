exec(open('./config/api_keys_local.py').read())

TOTAL_BUTTONS = 6
SCREEN_SIZE = (640, 400)

# Weather API details
LAT = '47.39360358111309'
LONG = '8.52740899788972'
WEATHER_API_ENDPOINT = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon=-{LONG}&exclude=minutely," \
                       f"hourly&units=metric&appid="

# Joke API details
JOKE_API_ENDPOINT = f'https://api.humorapi.com/jokes/random?api-key='
