import requests
from datetime import datetime

def datetime_from_utc_to_local(utc_datetime):
    local_datetime_converted = datetime.fromtimestamp(utc_datetime)
    return local_datetime_converted

def get_weather_data(mode):
    try:
        api_key = '4ddb9a817af55353322cd38faa9d786b'
        lat = 49.544458
        long = 8.448040
        weather_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&appid={api_key}'
        weather_r = requests.get(weather_url)
        if mode == "hourly":
            data = weather_r.json()['hourly']
        elif mode == "week":
            data = weather_r.json()['daily']
        else:
           raise ValueError

        weather_data_dict = {}
        for day in data:
            weather_data_dict[str(datetime_from_utc_to_local(day["dt"]))] = day["weather"][0]['main']
        return weather_data_dict
    except ValueError:
        print("Bitte geben Sie einen gültigen Modus an")
