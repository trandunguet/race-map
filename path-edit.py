import cv2 as cv
from path import Path, Dot

window_name = 'map'

# load current path
path_file = open('path.txt', 'r')
path = Path()
for line in path_file:
    words = [int(w) for w in line.split()]
    path.add_dot(words[0], words[1], words[2], words[3:])
path_file.close()

map = cv.imread('roadmask.png')

# load map, draw current path
def refresh_view():
    map_view = map.copy()
    for id, dot in path.dots.items():
        cv.circle(map_view, (dot.x, dot.y), 4, (255, 255, 255), -1)
        for adj_id in dot.adj:
            adj = path.dots[adj_id]
            cv.line(map_view, (dot.x, dot.y), (adj.x, adj.y), (255, 255, 255))

    cv.imshow(window_name, map_view)

def mouse_handler(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        path.create_dot(x, y, 1)
        refresh_view()

    if event == cv.EVENT_MBUTTONDOWN:
        path.create_dot(x, y, 2)
        refresh_view()

    if event == cv.EVENT_RBUTTONDOWN:
        path.delete_dot(x, y)
        refresh_view()

# bind the callback function to window
refresh_view()
cv.setMouseCallback(window_name, mouse_handler)
key = cv.waitKey()
if key == 13:
    path_file = open('path.txt', 'w')
    for id, dot in path.dots.items():
        path_file.write('{} {} {} '.format(id, dot.x, dot.y))
        for adj in dot.adj:
            path_file.write('{} '.format(adj))
        path_file.write('\n')
    path_file.close()
