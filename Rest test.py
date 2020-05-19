import requests
from ast import literal_eval
url = "http://localhost:8080/rest/items/Temperatursensor"

r = requests.get(url)

print(r.json())
temperatur = r.json()["state"]
print(temperatur.split(" ")[0])
temperatur_decoded = float(literal_eval(temperatur))
print(temperatur_decoded)