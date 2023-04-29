# Rename file to 'api_keys_local.py' if running locally

import os

if 'API_KEY_OPENWEATHERMAP' not in os.environ:
    os.environ['API_KEY_OPENWEATHERMAP'] = ''

if 'API_KEY_JOKES' not in os.environ:
    os.environ['API_KEY_JOKES'] = ''

if 'CALENDAR_URL' not in os.environ:
    os.environ['CALENDAR_URL'] = ''
