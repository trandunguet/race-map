import cv2 as cv
from path import Path, Dot

window_name = 'map'
set_checkpoint = 0

# load current path
path = Path()
path_file = open('path.txt', 'r')
for line in path_file:
    words = [int(w) for w in line.split()]
    path.add_dot(words[0], words[1], words[2], words[3:])
path_file.close()

checkpoint_file = open('checkpoints.txt', 'r')
for line in checkpoint_file:
    words = [int(w) for w in line.split()]
    path.checkpoints[words[0]] = words[1]
checkpoint_file.close()

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
            refresh_view()
        else:
            path.checkpoints[set_checkpoint] = path.find_two_nearest_dots(x, y)[0]
            set_checkpoint = 0
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

while True:
    key = cv.waitKey()
    if key == 27:
        break

    if key == 13:
        path_file = open('path.txt', 'w')
        for id, dot in path.dots.items():
            path_file.write('{} {} {} '.format(id, dot.x, dot.y))
            for adj in dot.adj:
                path_file.write('{} '.format(adj))
            path_file.write('\n')
        path_file.close()

        checkpoint_file = open('checkpoints.txt', 'w')
        for checkpoint, dot_id in path.checkpoints.items():
            checkpoint_file.write('{} {} \n'.format(checkpoint, dot_id))
        checkpoint_file.close()

    if key in range(48, 59):
        set_checkpoint = (key - 9) % 10 + 1
