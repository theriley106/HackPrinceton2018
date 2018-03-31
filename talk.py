#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# Tests connection and publishes warning

broker = "104.238.164.118"
print("Connecting to broker...\n")
mqtt_client = mqtt.Client("client1")
mqtt_client.connect(broker,8883,60)

mqtt_client.publish("HP18/report", "ACTIVE SOFT DRINK ON PREMISES!");

mqtt_client.disconnect()
