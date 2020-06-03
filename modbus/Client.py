from pymodbus.client.sync import ModbusTcpClient as ModbusClient

client = ModbusClient('127.0.0.1', port=5020) #Sensoren und Aktoren
client.connect()
items = {
    "temp_sensoren" :[ 100 , "Sensor",
                       { 0x10 :  "Erdgeschoss",
                        0x11 : "Arbeitszimmer"
                        },

                       ],

    "jalousie" : [1, "Aktor", {
                0x16 : "Jalousie_Erdgeschoss"
                 }],

    "fenster" : [1, "Aktor",{
        0x20 : "Fenster_1",
        0x21 : "Fenster_2",
        0x22 : "Fenster_3"
    }]
}

def get_daten(items_dict = items, gruppe = None, adresse = None):
    item_werte = {}
    for item_gruppe in items_dict:
        if gruppe is None or item_gruppe == gruppe:
            werte_temp = {}
            teiler = items_dict[item_gruppe][0]
            for adress in items[item_gruppe][2]:
                if adresse is None or adress == adresse:
                    if "Sensor" in items_dict[item_gruppe][1] :
                        result = client.read_input_registers(address=adress, count=1, unit=1)  # IR
                    else :
                        result = client.read_holding_registers(address=adress, count=1, unit=1)
                    if teiler != 1 :
                        werte_temp[items_dict[item_gruppe][2][adress]] = result.registers[0]/teiler
                    else:
                        werte_temp[items_dict[item_gruppe][2][adress]] = result.registers[0]

            if werte_temp: #überprüft ob dictionary leer ist
                item_werte[item_gruppe] = werte_temp
    return item_werte



def aktor_triggern(value, items_dict =items, gruppe=None, adresse=None):
    for item_gruppe in items_dict:
        if gruppe is None or item_gruppe == gruppe:
            if "Aktor" in items_dict[item_gruppe][1]:
                for adress in items_dict[item_gruppe][2]:
                    if adresse is None or adress == adresse:
                        client.write_registers(adress, value, unit=1)




#aktor_triggern(adresse=0x21,value=1)
#aktor_triggern(gruppe="fenster", value=0)
#aktor_triggern(1, 33)
#print(get_daten())