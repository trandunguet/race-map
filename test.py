import cv2 as cv

img = cv.imread('roadmask.png')
output = open('output.txt', 'r')

for line in output:
    words = [int(w) for w in line.split()]
    img_view = img.copy()
    cv.circle(img_view, tuple(words), 4, (255, 255, 255), -1)
    cv.imshow('view', img_view)
    cv.waitKey()
