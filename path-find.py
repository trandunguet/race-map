from queue import Queue
import math

import cv2 as cv

from path import Dot, Path

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

    while not queue.empty():
        current = queue.get()
        # for debugging:
        # cv.circle(map_view, (current.x, current.y), 4, (255, 0, 0), -1)
        # cv.imshow('map', map_view)
        # cv.waitKey()

        if current.id == finish.id:
            return current
            
        for adj_id in current.adj:
            adj = path.dots[adj_id]
            if adj.prev_mark[current.id]:
                continue
            adj.prev_mark[current] = True
            if angle(current.prev, current, adj) > math.pi / 3:
                continue

            queue.put(adj.get_clone(current))

map_view = cv.imread('roadmask.png')

input_file = open('input.txt', 'r')
for line in input_file:
    checkpoints = [int(w) for w in line.split()]

start = path.dots[path.checkpoints[5]]
prev_start = path.dots[108]
for checkpoint in checkpoints[1:]:
    track = bfs(prev_start, start,  path.dots[path.checkpoints[checkpoint]])
    start = path.dots[path.checkpoints[checkpoint]]
    prev_start = track.prev
    while track.prev is not None:
        cv.circle(map_view, (track.x, track.y), 4, (255, 0, 0), -1)
        track = track.prev
    cv.imshow('map', map_view)
    cv.waitKey()
