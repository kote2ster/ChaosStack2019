import cv2
import numpy as np
from pavlidis import pavlidis

txt = 'semilab-1.txt'
width, height = 0, 0
scale = 3
blob_min_size, blob_max_size = 500, 700000

def check(walked_image, x, y):
    return (walked_image[x][y][0] == 255 and walked_image[x][y][1] == 255 and walked_image[x][y][2] == 255) \
        or (walked_image[x][y][0] == 0 and walked_image[x][y][1] == 255 and walked_image[x][y][2] == 0)

with open(txt) as f:
    line = f.readline()
    width = len(line)
    f.seek(0)
    lines = f.readlines()
    height = len(lines)

image = np.zeros((height, width, 3), dtype=np.uint8)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

with open(txt) as f:
    lines = f.readlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '1':
                image[y][x] = 255

#canny_img = cv2.Canny(new_img, 0, 255)
blobs = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
stored_blobs = []
for blob in blobs[0]:
    size = cv2.contourArea(blob)
    if blob_max_size > size and size > blob_min_size:
        stored_blobs.append(blob)

image_contour = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
walked_image = image_contour.copy()
starting_points = [blob[0][0] for blob in stored_blobs]
starting_point_idx = 0
curr_pos = starting_points[starting_point_idx]

cost = 0

x, y, y_off = 0, 0, 0
move_list = []
laser_on = True
move_list.append('LASER_ON')
cost += 100

while True:
    if x+1 < height:
        x += 1
        if all(point == 255 for point in walked_image[x][y]):
            if not laser_on:
                laser_on = True
                move_list.append('MOVE_Y ' + str(x))
                cost += 1
                move_list.append('LASER_ON')
                cost += 100
        else:
            if laser_on:
                laser_on = False
                move_list.append('MOVE_Y ' + str(x-1))
                cost += 1
                move_list.append('LASER_OFF')
                cost += 1
    else:
        move_list.append('MOVE_Y ' + str(x))
        cost += 1
        x = 0
        y += 1
        if y == width:
            break
        laser_on = False
        move_list.append('LASER_OFF')
        cost += 1
        move_list.append('MOVE_X ' + str(y))
        cost += 1
        move_list.append('MOVE_Y ' + str(x))
        cost += 1
        if all(point == 255 for point in walked_image[x][y]):
            laser_on = True
            move_list.append('LASER_ON')
            cost += 100

with open('out.txt', 'w') as f:
    for move in move_list:
        f.write(move + '\n')

image_contour = walked_image #cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#cv2.drawContours(image_contour, stored_blobs, -1, (0, 0, 255), thickness=1)
new_img = cv2.resize(image_contour, (int(width*scale), int(height*scale)))
cv2.imshow('image', new_img)
while True:
    key = cv2.waitKey(1)
    if key == ord('s'):
        new_img = cv2.resize(image, (int(width*scale), int(height*scale)))
        cv2.imshow('image', new_img)
