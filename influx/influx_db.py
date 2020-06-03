from influxdb import InfluxDBClient
from datetime import datetime

def write_to_database(data, database="sensoren"):
    client = InfluxDBClient(host='localhost', port=8086)
    time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    for measurement in data:
        items = data[measurement]
        for tag in items:
            json_body = [
                {
                    "measurement" : measurement,
                    "tags" : {
                        "Item Name" : tag
                    },
                    "time": time,
                    "fields" :{
                        "value": items[tag]
                    }
                }

            ]
            client.switch_database(database= database)
            client.write_points(json_body)
            print("daten geschrieben")

# client = InfluxDBClient(host='localhost', port=8086)
# client.switch_database("sensoren")
# measurements= client.get_list_measurements()
# for measurement in measurements:
#     for name in measurement:
#         query_string = 'select * from {0};'.format(measurement[name])
#         print(client.query(query_string))


