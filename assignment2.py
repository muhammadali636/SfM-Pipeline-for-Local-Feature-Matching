#assignment2.py: driver code.
#references
#https://www.geeksforgeeks.org/sift-interest-point-detector-using-python-opencv/ - theory + sift
#https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html - CV tutorial on features: SIFT and Ratio + orb _FLANN
#https://en.wikipedia.org/wiki/Perspective-n-Point - PNP (MIN 6 points needed)
#https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html - pose computation PNP
#https://docs.opencv.org/4.5.5/d9/d0c/group__calib3d.html#gad3fc9a0c82b08df034234979960b778c - cv documentation
#ttps://github.com/MayankD409/Structure-From-Motion/blob/main/func.py - another sfm project, based some of the sfm.py methodology on this.
# https://stackoverflow.com/questions/16295551/how-to-correctly-use-cvtriangulatepoints?rq=3 - how to correctly use triangulatepoints.
#https://www.open3d.org/docs/release/getting_started.html


import numpy as np
import cv2
from utils import loadImages, readCalibrationMatrix, writePLY
from sfm import detectFeatures, matchDescriptors

def main():
    #PART 1. Image reading and preprocessing
    #Load images from the images/ folder
    numberOfImages = 30  #expects images "0000.jpg" --> "0029.jpg"
    images =loadImages("images",numberOfImages )
    
    #read camera intrisics aka calibration matrix
    cameraMatrix = readCalibrationMatrix( "K.txt")
    
    #PART 2: Feature Detection and Matching (SIFT and FLANN)
    features = []  #storing here keypoints and descriptors for each img
    for image in images:
        keypoints,descriptors = detectFeatures( image)
        features.append((keypoints,descriptors))
    
    #PART3: Pose Estimation for the First Two Images via essential matrix.
    

    
    
    #PART4: Triangulation and 3D Point Cloud Construction (4 marks) - trangulatePoints lacks documentation on opencv.
    
    
    
    #Step 5: Write the final point cloud to a PLY file.
    #swritePLY("mycloud.ply", pointCloud)
    #print("Saved mycloud.ply")
    #print(len(pointCloud), "points.")

main()
