from flask import Flask
from modbus import Client
from flask import render_template, request
from influx import influx_db
from weather_data import weather_data
from modbus import data_poller
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/temp_daten')
def temp_daten():
    data = Client.get_daten(gruppe="temp_sensoren")
    print(data)
    return render_template('temperatur.html', daten=data)

@app.route('/alle_daten')
def alle_daten():
    data = Client.get_daten()
    print(data)
    return render_template('temperatur.html', daten=data)

@app.route('/write_data')
def write_data():
    data = Client.get_daten()
    print(data)
    influx_db.write_to_database(data)
    return render_template('temperatur.html', daten=data)

@app.route('/fenster/')
def fenster():

    adresse = None if request.args.get('adresse') is None else int(request.args.get('adresse'),16)
    gruppe = request.args.get('gruppe')
    value = int(request.args.get('value'))
    Client.aktor_triggern(adresse= adresse, gruppe= gruppe, value=value)
    data = Client.get_daten(gruppe="fenster")
    influx_db.write_to_database(data)
    dates = weather_data.get_rain_date("week", True)
    return render_template('temperatur.html', daten=data, dates = dates)




if __name__ == '__main__':
    print("Starte Flask Server")
    app.run()

data_poller.poll_data(60, Client.get_daten, influx_db.write_to_database)
def starte_flask_server():
    print("Starte Flask Server")
    app.run()