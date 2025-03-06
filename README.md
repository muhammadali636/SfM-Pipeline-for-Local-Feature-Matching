

Detect and match keypoints between images,
Recover camera poses (rotations and translations),
Triangulate 3D points from the matched 2D keypoints,
Incrementally register additional images and expand your 3D point cloud,
Output your reconstruction as a .ply file,
Finally, visualize it with the provided viewer.


# CIS*4720 - Assignment 2: Structure from Motion (SfM) Pipeline
# ================================================================
# NOTE: Do NOT implement the bonus Multi-View Stereo (MVS) part.

# Step 1: Image Reading and Preprocessing
# -----------------------------------------
# - Load all .jpg images from the given directory.
# - Sort the images by filename (or known sequence order).
# - Read the camera intrinsics (calibration matrix) from K.txt.

# Step 2: Feature Detection and Matching
# -----------------------------------------
# - Decide on a feature detector/descriptor: SIFT or ORB (choose whichever is easier).
# - For each image, detect keypoints and compute descriptors.
# - Match keypoints between consecutive image pairs.
# - Apply a ratio test or another heuristic to filter out poor matches.
#   (Document your filtering criteria in importantnotes.pdf)

# Step 3: Pose Estimation for the First Two Images
# -----------------------------------------
# - Use the matching keypoints from the first two images.
# - Compute the essential matrix using the camera intrinsics.
# - Recover the relative rotation and translation (camera pose) between these images.

# Step 4: Triangulation and 3D Point Cloud Construction
# -----------------------------------------
# - Triangulate the 2D matched keypoints using the camera poses from Step 3.
# - Convert the resulting homogeneous coordinates to 3D points.
# - Keep track of the 3D points and associate them with their corresponding 2D features.

# Step 5: Pose Estimation for Subsequent Images
# -----------------------------------------
# - For each new image:
#     - Match its features to the existing 3D points (tracked from previous images).
#     - Use PnP with RANSAC to estimate the new camera pose.
#     - Triangulate additional points using the new pose and add them to the point cloud.

# Step 6: Output and Visualization
# -----------------------------------------
# - Export the final 3D point cloud, including color information, to a .ply file.
# - Verify the reconstruction using the provided viewer:
#     e.g., run "python showloud.py mycloud.ply" to display your point cloud.

# IMPORTANT:
# - Organize your code into modular functions (e.g., image loading, feature matching, pose estimation, triangulation, export).
# - Document your approach and any design decisions in your report (importantnotes.pdf).


comments from prof:
"I have mentioned this in class several times, but I understand that there are other priorities including work and other courses, and those who prefer alternative modes for learning - so I am mentioning this here:
Assignment 2 has an unusual quality in that the output will generally look quite bad until everything is absolutely perfect. A matrix might not be transposed when it should be, a vector might not be normalized based on the 4th dimension of it's homogenous coordinates, pose matrices expected as inputs may be reversed in the order they are passed in to a function. There are many, many places where something small can go wrong. Therefore, I want to be very clear: If your output doesn't look anything like the sample cloud provided, or even like anything sensible, this is not a disaster. I expect that many submissions will have this characteristic. If your thinking, logic and code is mostly correct, you can still do well on the assignment. Of course, you will likely do a little better if everything is correct, but don't think of this in black and white terms as it's possible to do very well even if your output isn't great"