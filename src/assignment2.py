#assignment2.py: main driver

#driver to run sfm pipeline.
# - Initialize the pipeline.
# - Load and sort images from the "images/" folder.
# - Read camera intrinsics from K.txt.

#call all functions in the correct order to build the SfM pipeline.
# - Verify your reconstruction by running: python showloud.py mycloud.ply
# - Document your filtering approach and any design decisions in importantnotes.pdf

import utils

# - Load images from the "images/" folder.
images = util.load_images()
# - Read the calibration matrix from K.txt.
K = util.read_calibration_matrix()

# - Call the following modules in order:
#   1. detect_match.py to detect and match keypoints.
#   2. pose_estimation.py to recover camera poses for the first image pair.
#   3. triangulation.py to triangulate 3D points from matched keypoints.
#   4. incremental_registration.py to register additional images and add new points.
# - Export the final point cloud to mycloud.ply and visualize it with showloud.py.
