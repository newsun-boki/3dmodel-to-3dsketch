import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
inlier_cloud = o3d.io.read_point_cloud("combined1.ply")
# o3d.visualization.draw_geometries([inlier_cloud], window_name="Original Point Cloud")

# with o3d.utility.VerbosityContextManager(
#         o3d.utility.VerbosityLevel.Debug) as cm:
#     labels = np.array(
#         inlier_cloud.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))

# max_label = labels.max()
# print(f"point cloud has {max_label + 1} clusters")
# colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
# colors[labels < 0] = 0
# inlier_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
# o3d.visualization.draw_geometries([inlier_cloud], window_name="Original Point Cloud")
#### 树形结构获取curve network
# # 构建KD树
pcd_tree = o3d.geometry.KDTreeFlann(inlier_cloud)

# 定义连接点的距离阈值
radius = 1  # 根据你的数据集调整这个值

# 存储连接线的数组
lines = []

# 对于点云中的每个点，找到在给定半径内的邻居并创建线段
for i in range(len(inlier_cloud.points)):
    [k, idx, d] = pcd_tree.search_radius_vector_3d(inlier_cloud.points[i], radius)
    for j,id in enumerate(idx):
        if id != i:  # 避免自身连接
            lines.append([i, id])
        if(j > 2):
            break
# 创建一个线集对象来表示曲线网络
line_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(inlier_cloud.points),
    lines=o3d.utility.Vector2iVector(lines),
)

# 可视化曲线网络
o3d.visualization.draw_geometries([line_set], window_name="3D Curve Network")