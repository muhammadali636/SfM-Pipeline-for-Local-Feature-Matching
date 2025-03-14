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
from sfm import detectFeatures, matchDescriptors, estimatePose, triangulatePoints, solvePNP

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
    keypoints0, descriptors0 = features[0]
    keypoints1, descriptors1 = features[1]
    matches01=matchDescriptors(descriptors0, descriptors1, ratioThreshold=0.4)
    R_initial,t_initial, points0, points1 = estimatePose( keypoints0,keypoints1, matches01,cameraMatrix )  #EST relative pose between img 0 and img 1.

    #save camera poses: first img at origin, second img from essential matrix
    cameraPoses = []
    cameraPoses.append(( np.eye(3), np.zeros((3,1))))  #pose for image 0.
    cameraPoses.append((R_initial, t_initial)) #pose for image 1.
    
    #PART4: Triangulation and 3D Point Cloud Construction (4 marks) - trangulatePoints lacks documentation on opencv.
    points3D_initial = triangulatePoints( cameraPoses[0][0],  cameraPoses[0][1],cameraPoses[1][0], cameraPoses[1][1],points0, points1, cameraMatrix)
    pointCloud =     points3D_initial.tolist()  
    associations = {}#mapping from image/keypoint index to  3D point.
    for (idx0,  idx1), point3D in zip(matches01, points3D_initial):
        associations[(0, idx0)] = point3D
        associations[(1, idx1)] = point3D
    
    #PART 4: PROCESS IMG2->IMG29
    #match features btw image i-1 and i, built correspondences, use pnp
    for i in range(2,numberOfImages):
        keypointsPrev,descriptorsPrev = features[i-1]
        keypointsCurr, descriptorsCurr = features[i]
        
       
        matchesCurrent = matchDescriptors(descriptorsPrev, descriptorsCurr, ratioThreshold=0.4)
        
        #build 2D-3D correspondences from image i-1.
        objectPoints = []  # 3D points.
        imagePoints = []   # 2D points in the current image.
        for match in matchesCurrent:
            if (i-1, match[0]) in associations:
                objectPoints.append(associations[ (i -  1,  match[0])])
                imagePoints.append(keypointsCurr[match[1]].pt)
        
        #iff we have enough correspondences, use PnP to compute the current camera pose.
        #https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html needs atleast 6 points to solve pnp problem.
        #if 6 then enough correspondence.
        if len(objectPoints) >= 6:
            R_current,t_current =  solvePNP(objectPoints,imagePoints, cameraMatrix )
            cameraPoses.append((R_current, t_current))
        else:
            #if not enough reuse previous pose.
            cameraPoses.append(cameraPoses[-1])
            continue
        
        #triangulate new 3D points between img i-1 and i
        #build the 2D points for the previous img
        pointsPrev2D_list = []
        for match in matchesCurrent:
            indexPrev = match[0]
            #get 2D point from the previous img's keypoints.
            pointPrev = keypointsPrev[indexPrev].pt
            pointsPrev2D_list.append(pointPrev)
        #convert the list to a NumPy arr.
        pointsPrev2D =  np.float32(pointsPrev2D_list )

        #build 2D points for    the current image.
        pointsCurr2D_list   = []
        for match in matchesCurrent:
            indexCurr = match[1]
            #get 2D point from  current imgs's kps.
            pointCurr =keypointsCurr[indexCurr].pt
            pointsCurr2D_list.append(pointCurr)
        pointsCurr2D =  np.float32(pointsCurr2D_list )         #convert to a NumPy arr.
        newPoints3D =   triangulatePoints(cameraPoses[i - 1][0],cameraPoses[i - 1][1], cameraPoses[i][0], cameraPoses[i][1], pointsPrev2D,pointsCurr2D, cameraMatrix )
        #add new 3D points to the global cloud and update association map.
        for match ,   pt3D in zip(matchesCurrent, newPoints3D):
            associations[(i-1, match[0])] = pt3D
            associations[(i, match[1])] = pt3D
            pointCloud.append( pt3D.tolist())
    
    #Step 5: Write the final point cloud to a PLY file.
    writePLY("mycloud.ply", pointCloud)
    #print("Saved mycloud.ply")
    #print(len(pointCloud), "points.")

main()
