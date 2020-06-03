from flask import Flask
from modbus import Client
from flask import render_template, request
from influx import influx_db
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
    print(data)
    influx_db.write_to_database(data)
    return render_template('temperatur.html', daten=data)




if __name__ == '__main__':
    print("Starte Flask Server")
    app.run()
