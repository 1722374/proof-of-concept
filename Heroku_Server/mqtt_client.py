import paho.mqtt.client as mqtt

MQT_BROKER_URL = "broker.hivemq.com"
MQTT_CHANNEL = "IITIFTTT68165"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(MQTT_CHANNEL)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQT_BROKER_URL, 1883, 60)

client.loop_forever()
