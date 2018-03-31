#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

# Tests connection and publishes warning, tests subscription and prints message

print("Connecting to broker...\n")
mqtt_client = mqtt.Client("client1") # new client with name
mqtt_client.connect("104.238.164.118", 8883, 60) # connects to broker address

mqtt_client.publish("HP18/report/test", "SEND TEST") # publishes to topic with message (should appear on mosquito)

mqtt_client.loop_start() # starts listening
mqtt_client.subscribe("HP18/report/test") # subscribes to topic

def on_message(client, userdata, msg):
  print("message received " ,str(msg.payload.decode("utf-8")))
  print("message topic =", msg.topic)
  print("message qos =", msg.qos)
  print("message retain flag =", msg.retain)

mqtt_client.on_message = on_message # callback

mqtt_client.publish("HP18/report/test", "RECIEVE TEST") # publishes test (should recieve automatically once subscribed)
time.sleep(1) # waits for callback
mqtt_client.loop_stop() # stops listening

mqtt_client.disconnect() # disconnects client from broker
