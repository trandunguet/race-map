#!/usr/bin/env python
from Queue import Queue
import math
import sys
import json

import paho.mqtt.client as mqtt

from path import Dot, Path


def angle(a, b, c):
    v1 = b - a
    v2 = c - b
    return math.acos((v1 * v2) / round(v1.length() * v2.length(), 3))

def bfs(prev_start, start, finish):
    for id, dot in path.dots.items():
        dot.reset()
    queue = Queue()
    queue.put(start.get_clone(prev_start))
    result = []

    while not queue.empty():
        current = queue.get()

        if current.id == finish.id:
            result.append(current)

        for adj_id in current.adj:
            adj = path.dots[adj_id]

            if adj.prev_mark[current.id]:
                continue
            if angle(current.prev, current, adj) > math.pi / 180 * 72:
                continue
            adj.prev_mark[current.id] = True

            queue.put(adj.get_clone(current))

    return result

def max_track(a, b):
    if len(b) != len(a):
        return a
    c = []
    for i in range(len(a)):
        if a[i].d < b[i].d:
            c.append(a[i])
        else:
            c.append(b[i])
    return c

def process(checkpoints):
    print(checkpoints)
    start = path.dots[path.checkpoints[5]]
    prev_start = path.dots[108]
    best_track = prev_tracks = bfs(prev_start, start,  path.dots[path.checkpoints[checkpoints[1]]])
    for checkpoint in checkpoints[2:]:
        best_track = []
        for prev_track in prev_tracks:
            track = bfs(prev_track.prev, prev_track,  path.dots[path.checkpoints[checkpoint]])
            best_track = max_track(track, best_track)
        prev_tracks = best_track

    track = best_track[0]

    output = []
    while track.prev is not None:
        output.append(track)
        track = track.prev

    output_file = open('output.txt', 'w')
    for dot in output[::-1]:
        output_file.write('{} {}\n'.format(dot.x, dot.y))
    output_file.close()

def on_connect(client, userdata, flags, rc):
	m_client.subscribe("route")
	print("connect to broker")

def on_message(client, userdata, message):
	datastore = json.loads(str(message.payload))
	if datastore["team"] == team_id:
		process([x for x in datastore["route"]])

def init():
	m_client.on_message=on_message
	m_client.on_connect = on_connect
	m_client.connect(broker, 1883, 60)
	m_client.loop_forever()

if __name__ == '__main__':
    debug = False
    broker="192.168.1.124"  # ip server
    if len(sys.argv) == 2:
        broker=sys.argv[1]
    m_client = mqtt.Client()
    team_id = 1

    path = Path()
    path.load()
    init()
