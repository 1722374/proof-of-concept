from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient



client = ModbusClient('127.0.0.1', port=5020) #Sensoren und Aktoren
client.connect()
items = {
    "temp_sensoren" :[ "16 Bit" , "Sensor",
                       { 0x10 :  "Erdgeschoss",
                        0x11 : "Arbeitszimmer"
                        },

                       ],

    "taster" : ["1 Bit", "Aktor", {
                0x16 : "Klingel"
                 }],

    "fenster" : ["1 Bit", "Aktor",{
        0x20 : "Fenster_1",
        0x21 : "Fenster_2",
        0x22 : "Fenster_3"
    }]
}

def get_daten(items = items, gruppe = None, adresse = None):
    item_werte = {}
    for item_gruppe in items:
        if gruppe is None or item_gruppe == gruppe:
            werte_temp = {}
            if "16 Bit" in items[item_gruppe][0]:
                for adress in items[item_gruppe][2]:
                    if adresse is None or adress == adresse:
                        if "Sensor" in items[item_gruppe][1] :
                            result = client.read_input_registers(address=adress, count=1, unit=1)  # IR
                        else :
                            result = client.read_holding_registers(address=adress, count=1, unit=1)
                        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,wordorder=Endian.Big)
                        werte_temp[items[item_gruppe][2][adress]] = decoder.decode_16bit_float()
            #wenn diese Adresse 1 Bit werte enthält
            if "1 Bit" in items[item_gruppe][0]:
                for adress in items[item_gruppe][2]:
                    if adresse is None or adress == adresse:
                        if "Sensor" in items[item_gruppe][1]:
                            result = client.read_input_registers(address=adress, count=1, unit=1)  # IR
                        else:
                            result = client.read_holding_registers(address=adress, count=1, unit=1)
                        werte_temp[items[item_gruppe][2][adress]] = result.registers[0]  # liest den Wert aus und schreibt es in das Dictionary
            if werte_temp: #überprüft ob dictionary leer ist
                item_werte[item_gruppe] = werte_temp
    return item_werte



def aktor_triggern(value, adresse, items =items):
    for item_gruppe in items:
        if "Aktor" in items[item_gruppe][1]:
            for adress in items[item_gruppe][2]:
                if adress == adresse:
                    if  "1 Bit" in items[item_gruppe][0]:
                        client.write_registers(adresse, value, unit=1)


#aktor_triggern(adresse=0x21,value=1)
#print(get_daten(adresse=0x21))