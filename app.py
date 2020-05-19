from flask import Flask
from modbus import Client
from flask import render_template
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
    influx_db.write_to_database_all(data)
    return render_template('temperatur.html', daten=data)

@app.route('/fenster_öffnen/<adresse>')
def fenster_öffnen(adresse):
    adresse = int(adresse, 16)
    Client.aktor_triggern(adresse= adresse,value=1)
    data = Client.get_daten(gruppe="fenster")
    print(data)
    influx_db.write_to_database_all(data)
    return render_template('temperatur.html', daten=data)


if __name__ == '__main__':
    app.run()
