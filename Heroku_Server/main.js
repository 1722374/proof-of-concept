const mqtt = require('mqtt');
const express = require('express')

const port = process.env.PORT || 3001;

const MQTT_BROKER_URL = 'tcp://broker.hivemq.com';
const MQTT_CHANNEL = 'IITIFTTT68165';
const MQTT_MESSAGE_STUB = 'IFTTT';

const app = express()

app.get('/mqtt/receive', (req, res) => {

    const client = mqtt.connect(MQTT_BROKER_URL);

    // read value from request-url
    const value = req.query.value;

    client.on('connect', () => {
        client.publish(MQTT_CHANNEL, `${MQTT_MESSAGE_STUB}${value}`);
        client.end();
    });

    return res.status(200);
});

app.listen(port, '0.0.0.0', () => console.log(`Server listening at http://0.0.0.0:${port}`));