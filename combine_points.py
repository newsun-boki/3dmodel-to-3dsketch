import open3d as o3d
import os
model_dir = 'plys/buildings'
    # model_list = ['building_big'] # 不包含后缀名
model_list= [os.path.splitext(f)[0] for f in os.listdir(model_dir) if os.path.isfile(os.path.join(model_dir, f))]
output_dir = "output"
for model_id in model_list:
    model_id = '2'
    combined_pcd = o3d.geometry.PointCloud()
    for i in range(50):  # 从0.ply到20.ply
        ply_filename = f"output/pcd/{model_id}/{i}.ply"  # 格式化文件名
        print(f"Reading {ply_filename}...")
        pcd = o3d.io.read_point_cloud(ply_filename)  # 读取点云
        combined_pcd += pcd  # 将当前点云加到并集中

    # 读取PLY文件
    # 可视化原始点云
    # o3d.io.write_point_cloud("combined0.ply", combined_pcd)
    # o3d.visualization.draw_geometries([combined_pcd], window_name="Original Point Cloud")
    pcd_points = combined_pcd.voxel_down_sample(voxel_size=0.01)
    cl, ind = pcd_points.remove_statistical_outlier(nb_neighbors=20, std_ratio=1)
    pcd_points = pcd_points.select_by_index(ind)
    # o3d.visualization.draw_geometries([pcd_points], window_name="Original Point Cloud")
    # o3d.io.write_point_cloud("combined1.ply", pcd_points)
    # 应用统计滤波器去除噪点
    # combined2_dir = os.path.join(output_dir, 'combined2', model_id)
    # os.makedirs(combined2_dir, exist_ok=True)
    cl, ind = pcd_points.remove_statistical_outlier(nb_neighbors=20, std_ratio=0.001)
    pcd_points = pcd_points.select_by_index(ind)
    # cl, ind = pcd_points.remove_statistical_outlier(nb_neighbors=20, std_ratio=0.1)
    # pcd_points = pcd_points.select_by_index(ind)
    o3d.visualization.draw_geometries([pcd_points], window_name="Processed Point Cloud")
    # o3d.io.write_point_cloud(os.path.join(combined2_dir,"combined2.ply"), pcd_points)
    break
    pcd_points = pcd_points.voxel_down_sample(voxel_size=0.1)
    # o3d.visualization.draw_geometries([pcd_points], window_name="Original Point Cloud")
    # o3d.io.write_point_cloud("combined3.ply", pcd_points)

    # cl, ind = pcd_points.remove_statistical_outlier(nb_neighbors=20, std_ratio=2)
    # pcd_points = pcd_points.select_by_index(ind)
    # o3d.visualization.draw_geometries([pcd_points], window_name="Original Point Cloud")
    pcd_tree = o3d.geometry.KDTreeFlann(pcd_points)

    # 定义连接点的距离阈值
    radius = 1  # 根据你的数据集调整这个值

    # 存储连接线的数组
    lines = []

    # 对于点云中的每个点，找到在给定半径内的邻居并创建线段
    for i in range(len(pcd_points.points)):
        [k, idx, d] = pcd_tree.search_radius_vector_3d(pcd_points.points[i], radius)
        for j,id in enumerate(idx):
            if id != i:  # 避免自身连接
                lines.append([i, id])
            if(j > 5):
                break
    # 创建一个线集对象来表示曲线网络
    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(pcd_points.points),
        lines=o3d.utility.Vector2iVector(lines),
    )

    # 可视化曲线网络
    # o3d.visualization.draw_geometries([line_set], window_name="3D Curve Network")
    # o3d.io.write_line_set("line_set.ply", line_set)
    print("done")
    break