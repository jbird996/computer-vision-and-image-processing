#Jason Hatfield - 29163434
#CSE473 Summer 2017
#PA1 - Question 1a

import numpy as np
import cv2

#Import image, extract dimensions
img = cv2.imread('lena_gray.jpg',0)
rows = img.shape[0]
cols = img.shape[1]

#Initialize 3x3 Sobel filters
filter1 = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
filter2 = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

#Initialize resultant matrices
filter1_result = np.zeros((rows,cols))
filter2_result = np.zeros((rows,cols))
filter3_result = np.zeros((rows,cols))

#Pad image with a single pixel matching the corresponding pixel on the edge of the image
img = np.pad(img,(1,1),'edge')

#Brute force algorithm for looping the image matrix and applying 2D convolution
for x in range(0,rows):
    for y in range(0,cols):
        Gx = (filter1[0][0] * img[x-1][y-1]) + (filter1[0][1] * img[x-1][y]) + (filter1[0][2] * img[x-1][y+1]) \
             + (filter1[1][0] * img[x][y-1]) + (filter1[1][1] * img[x][y]) + (filter1[1][2] * img[x][y+1])     \
             + (filter1[2][0] * img[x+1][y-1]) + (filter1[2][1] * img[x+1][y]) + (filter1[2][2] * img[x+1][y+1])
             
        Gy = (filter2[0][0] * img[x-1][y-1]) + (filter2[0][1] * img[x-1][y]) + (filter2[0][2] * img[x-1][y+1]) \
             + (filter2[1][0] * img[x][y-1]) + (filter2[1][1] * img[x][y]) + (filter2[1][2] * img[x][y+1])     \
             + (filter2[2][0] * img[x+1][y-1]) + (filter2[2][1] * img[x+1][y]) + (filter2[2][2] * img[x+1][y+1])
             
        filter1_result[x][y] = Gx
        filter2_result[x][y] = Gy
        filter3_result[x][y] = np.sqrt(np.square(Gx) + np.square(Gy))

#Write resultant images to disk
cv2.imwrite('Gx.png',filter1_result) 
cv2.imwrite('Gy.png',filter2_result)
cv2.imwrite('G.png',filter3_result)

#Code to display imported image
#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
