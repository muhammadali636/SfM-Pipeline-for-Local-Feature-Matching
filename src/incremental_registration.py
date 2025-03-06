
# incremental_registration.py
# -----------------------------
# - For each new image:
#     - Match features to the already known 3D points.
#     - Use PnP with RANSAC to estimate the new camera pose.
#     - Triangulate new points and add them to the overall point cloud.
#
