# detect_match.py
# reference: https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
#https://www.geeksforgeeks.org/sift-interest-point-detector-using-python-opencv/# ----------------
# - Detect keypoints and compute descriptors (using ORB).
# - BRUTE FORCE MATCHER 
# - Match keypoints between images (considering consecutive pairs).
# - Filter matches (e.g., using ratio tests).



import cv2
import numpy as np

def detect_and_match(images):
    """
    Detects keypoints and matches for consecutive image pairs.
    
    For each consecutive pair (images[i] and images[i+1]):
      - Converts images to grayscale.
      - Detects keypoints and computes ORB descriptors.
      - Uses a BFMatcher with Hamming distance and applies the ratio test.
    Returns a list of dictionaries (one per pair) with:
      - 'img1', 'img2': the original images.
      - 'kp1', 'kp2': keypoints for each image.
      - 'matches': list of filtered matches.
    """

    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    match_results = []
    for i in range(len(images) - 1):
        img1_gray = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(images[i+1], cv2.COLOR_BGR2GRAY)
        
        kp1, des1 = orb.detectAndCompute(img1_gray, None)
        kp2, des2 = orb.detectAndCompute(img2_gray, None)
        knn_matches = bf.knnMatch(des1, des2, k=2)
        ratio_thresh = 0.75
        good_matches = []
        for m, n in knn_matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
        good_matches = sorted(good_matches, key=lambda x: x.distance)
        match_results.append({
            "img1": images[i],
            "img2": images[i+1],
            "kp1": kp1,
            "kp2": kp2,
            "matches": good_matches
        })
    
    return match_results


    '''
def detect_and_match(images):
    """
    Detects keypoints and matches for consecutive image pairs using SIFT descriptors.
    
    For each consecutive pair (images[i] and images[i+1]):
      - Converts images to grayscale.
      - Detects keypoints and computes SIFT descriptors.
      - Uses a BFMatcher (default NORM_L2) and applies Lowe's ratio test.
    Returns a list of dictionaries (one per pair) with:
      - 'img1', 'img2': the original images.
      - 'kp1', 'kp2': keypoints for each image.
      - 'matches': list of filtered DMatch objects.
    """
    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # Create BFMatcher with default parameters (L2 norm)
    bf = cv2.BFMatcher()
    
    match_results = []
    
    for i in range(len(images) - 1):
        # Convert images to grayscale
        img1_gray = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(images[i+1], cv2.COLOR_BGR2GRAY)
        
        # Detect keypoints and compute SIFT descriptors
        kp1, des1 = sift.detectAndCompute(img1_gray, None)
        kp2, des2 = sift.detectAndCompute(img2_gray, None)
        
        # Obtain the two best matches for each descriptor
        knn_matches = bf.knnMatch(des1, des2, k=2)
        ratio_thresh = 0.75
        good_matches = []
        for m, n in knn_matches:
            # Apply Lowe's ratio test
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
        
        # Sort the good matches by ascending distance
        good_matches = sorted(good_matches, key=lambda x: x.distance)
        
        match_results.append({
            "img1": images[i],
            "img2": images[i+1],
            "kp1": kp1,
            "kp2": kp2,
            "matches": good_matches
        })
    
    return match_results
    '''