import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
pcd = o3d.io.read_point_cloud("combined3.ply")
pcd = pcd.voxel_down_sample(voxel_size=0.3)

# 可视化曲线网络
o3d.visualization.draw_geometries([pcd], window_name="3D Curve Network")