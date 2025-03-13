#sfm.py: Detect and match keypoints between images, Recover camera poses (rotations and translations), Triangulate 3D points from the matched 2D keypoints, Incrementally register additional images and expand your 3D point cloud, Output your reconstruction as a .ply file,
#contains the calculations and the big guns.

import numpy as np
import cv2



#SIFT algo to detect keypoints and get descriptors for img
def detectFeatures( image ):
    siftDetector = cv2.SIFT_create()
    grayImage = cv2.cvtColor( image,  cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = siftDetector.detectAndCompute( grayImage, None)
    return keypoints, descriptors

#FLANN descriptor matchmaker btw images and a ratio test to kill outliers (far off points)
#play around wiht ratio threshold.
''' The images are ordered spatially, so it may not be necessary to consider all
possible pairs of images for matches. Matching the first image with the second,
then the second with the third, and so on, would be a good place to start, and
might be sufficient'''
def matchDescriptors(descriptorsOne,  descriptorsTwo, ratioThreshold=0.4 ):
    FLANN_INDEX_KDTREE=  1
    indexParameters =dict(algorithm=FLANN_INDEX_KDTREE,trees =5 )
    searchParameters = dict( checks=50)
    flannMatcher = cv2.FlannBasedMatcher(indexParameters,   searchParameters )
    knnMatches =  flannMatcher.knnMatch( descriptorsOne,descriptorsTwo, k=2)
    goodMatches =[]
    #Implement ratio tests or other heuristics to filter out poor matches. 
    for firstMatch,secondMatch in knnMatches:
        if firstMatch.distance < ratioThreshold*secondMatch.distance:
            goodMatches.append((  firstMatch.queryIdx  , firstMatch.trainIdx))
    return goodMatches

#est the relative camera pose using the essential matrix. The essential matrix approach works when camera intrinsics (K) are known. 
#Estimate E using cv2.findEssentialMat and cv2.recoverPose may be helpful. This step recovers the initial baseline between your first two images.

#Triangulation: 3D points from two images (2d) given camera poses points. 2d -> 3d 

#PNP: solve for the camera pose of new image using 2D-3D correspondence
