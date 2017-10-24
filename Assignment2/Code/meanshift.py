# Jason Hatfield - 29163434
# CSE 473 - PA2 - Question 2
# Due: 7/12/17

# Mean Shift Segmentation

import numpy as np
import cv2
import math
from random import randint

# Mean shift variable settings
H = 90
Iter = 10

img = cv2.imread('Butterfly.jpg')
segImg = np.zeros(img.shape, np.uint8)

# Takes color image matrix as input, returns vector array [B,G,R,x,y].
def matrixToVector(img):
    
    rows, cols, z = img.shape
    matrix = []
    
    for x in range(0, rows):
        for y in range(0, cols):
            b,g,r = img[x][y]
            matrix.append([b, g, r, x, y])
            
    matrix = np.array(matrix)
    
    return matrix
 
# Gathers neighbors in close proximity to random pixel for use by meanShift().   
def getNeighbors(initialAvg, matrix):
    
    neighbors = []

    for i in range(0, len(matrix)):
        pixel = matrix[i]
        d = math.sqrt(sum((pixel - initialAvg)**2))
        
        if(d < H):
             neighbors.append(i)
             
    return neighbors

# Add mean value for pixel and neighbors to result image, remove them from active matrix.
def removePixels(neighbors,average,matrix):
    
    for i in neighbors:
        pixel = matrix[i]
        x=pixel[3]
        y=pixel[4]
        segImg[x][y] = np.array(average[:3], np.uint8)
        
    return np.delete(matrix, neighbors, axis=0)

# Calculates mean for each value of 5-D vector.
def average(neighbors, matrix):
    
    neighbors = matrix[neighbors]
    r = neighbors[:,:1]
    g = neighbors[:,1:2]
    b = neighbors[:,2:3]
    x = neighbors[:,3:4]
    y = neighbors[:,4:5]
    average = np.array([np.mean(r), np.mean(g), np.mean(b), np.mean(x), np.mean(y)])
    
    return average

# Main mean shift function, randomly selects a pixel, call to calculate neighbors, call to remove matched pixels, 
# mean calculation.
def meanShift(img):
    
    clusters = 0
    vector = matrixToVector(img)

    while(len(vector) > 0):
        
        print('Pixels Remaining: ' + str(len(vector)))

        randomIndex = randint(0, len(vector) - 1)
        initialAvg = vector[randomIndex]

        neighbors = getNeighbors(initialAvg, vector)

        if(len(neighbors) == 1):
            vector = removePixels([randomIndex], initialAvg, vector)
            clusters += 1
            continue
            
        avg = average(neighbors, vector)
        meanShift = abs(avg - initialAvg)

        if(np.mean(meanShift) < Iter):
            vector = removePixels(neighbors, avg, vector)
            clusters += 1
    
def main():
    
    meanShift(img)
    cv2.imwrite("meanShift-h90.png", segImg)
    #cv2.imshow('Original Image', img)
    #cv2.imshow('Segmented Image', segImg)

main()