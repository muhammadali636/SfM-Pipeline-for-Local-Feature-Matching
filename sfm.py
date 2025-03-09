#sfm.py: Detect and match keypoints between images, Recover camera poses (rotations and translations), Triangulate 3D points from the matched 2D keypoints, Incrementally register additional images and expand your 3D point cloud, Output your reconstruction as a .ply file,
#contains the calculations and the big guns.

import numpy as np
import cv2



