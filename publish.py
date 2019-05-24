#!/usr/bin/env python
import sys

import paho.mqtt.client as mqtt

json_str = "{\"team\": 1, \"route\": [" + sys.argv[1] + "]}" 

if __name__ == '__main__':
	client = mqtt.Client()
	client.connect("localhost")
	client.loop_start()
	client.publish("route", json_str)
	client.loop_stop()
