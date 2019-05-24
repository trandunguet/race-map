#!/usr/bin/env python3
from queue import Queue
import math

import cv2 as cv

from path import Dot, Path

debug = False

path = Path()
path.load()

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

        if debug:
            cv.circle(map_view, (current.x, current.y), 4, (255, 0, 0), -1)
            cv.imshow('map', map_view)
            cv.waitKey()

        if current.id == finish.id:
            result.append(current)
            
        for adj_id in current.adj:
            adj = path.dots[adj_id]

            if debug:
                cv.circle(map_view, (adj.x, adj.y), 4, (0, 0, 255), -1)
                cv.imshow('map', map_view)
                cv.waitKey()

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

map_view = cv.imread('roadmask.png')

input_file = open('input.txt', 'r')
output_file = open('output.txt', 'w')
for line in input_file:
    checkpoints = [int(w) for w in line.split()]

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
    cv.circle(map_view, (track.x, track.y), 4, (255, 0, 0), -1)
    output.append(track)
    track = track.prev
cv.imshow('map', map_view)
cv.waitKey()

for dot in output[::-1]:
    output_file.write('{} {}\n'.format(dot.x, dot.y))
