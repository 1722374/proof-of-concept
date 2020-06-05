import requests
from datetime import datetime

def datetime_from_utc_to_local(utc_datetime):
    local_datetime_converted = datetime.fromtimestamp(utc_datetime)
    return local_datetime_converted

#Gibt die Wetterdaten der nächsten 48 Stunden (Stündliche angaben) oder der ganzen Woche (Nur 13:00 Uhr) als dictionary zurück.
#Die Keys sind die Zeiten (in Deutsche Zeit formartiert) und die Values sind das entsprechende Wetter
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


#Liest alle Zeiten aus den Wetter Daten an denen es regnen wird und gibt eine Liste zurück.
#Für eine detaillierte Ansicht für die nächsten 48 Stunden --> mode = "hourly"
#Für eine Tagesansicht für jede Woche (nur 13:00 Uhr) --> mode = "week"
#days_only auf True wenn nur der Tag angegeben werden soll. Bei Falls werden alle Zeiten (Tag und Stunden) angezeigt
def get_rain_date(mode, days_only):
    dict = get_weather_data(mode)
    zeit_liste = []
    if "Rain" in dict.values():
        for day in dict:
            if dict[day] == "Rain":
                if days_only:
                    day = day.split(" ")[0]
                if day not in zeit_liste:
                    #Keine Duplikate
                    zeit_liste.append(day)
    return zeit_liste

