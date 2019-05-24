#!/usr/bin/env python

import paho.mqtt.client as mqtt

json_str = "{\"team\": 1, \"route\": [5,1,2]}" 

if __name__ == '__main__':
	client = mqtt.Client()
	client.connect("localhost")
	client.loop_start()
	client.publish("route", json_str)
	client.loop_stop()
