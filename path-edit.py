#!/usr/bin/env python
import cv2 as cv
from path import Path, Dot

window_name = 'map'
set_checkpoint = 0

# load current path
path = Path()
path.load()

map = cv.imread('roadmask.png')

# load map, draw current path
def refresh_view():
    map_view = map.copy()
    for id, dot in path.dots.items():
        cv.circle(map_view, (dot.x, dot.y), 4, (255, 255, 255), -1)
        for adj_id in dot.adj:
            adj = path.dots[adj_id]
            cv.line(map_view, (dot.x, dot.y), (adj.x, adj.y), (255, 255, 255))
    for checkpoint, dot_id in path.checkpoints.items():
        dot = path.dots[dot_id]
        cv.circle(map_view, (dot.x, dot.y), 6, (0, 0, 255), -1)
        cv.putText(map_view, str(checkpoint), (dot.x - 10, dot.y - 40), cv.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 255))

    cv.imshow(window_name, map_view)

def mouse_handler(event, x, y, flags, param):
    global set_checkpoint
    if event == cv.EVENT_LBUTTONDOWN:
        if set_checkpoint == 0: 
            path.create_dot(x, y, 1)
        else:
            path.checkpoints[set_checkpoint] = path.find_two_nearest_dots(x, y)[0]
            set_checkpoint = 0

    elif event == cv.EVENT_MBUTTONDOWN:
        path.create_dot(x, y, 2)

    elif event == cv.EVENT_RBUTTONDOWN:
        path.delete_dot(x, y)

    else:
        return
        
    refresh_view()

# bind the callback function to window
refresh_view()
cv.setMouseCallback(window_name, mouse_handler)

while True:
    key = cv.waitKey()
    if key == 27:
        break

    if key == 13:
        path.save()

    if key in range(48, 59):
        set_checkpoint = (key - 9) % 10 + 1
