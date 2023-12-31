import open3d as o3d
import numpy as np
import imageio
import os
import argparse
parser = argparse.ArgumentParser()
# parser.add_argument('list_file')
parser.add_argument('--number', type=int, default=0)
args = parser.parse_args()
model_dir = 'plys/buildings'
    # model_list = ['building_big'] # 不包含后缀名
model_list= [os.path.splitext(f)[0] for f in os.listdir(model_dir) if os.path.isfile(os.path.join(model_dir, f))]
output_dir = "output"
if not os.path.exists(os.path.join(output_dir, 'videos')):
    os.mkdir(os.path.join(output_dir, 'videos'))
for model_id in model_list:
    model_id = model_list[args.number]
    # 定义视频保存的路径和名称
    video_filename = os.path.join(output_dir, 'videos', model_id+'.mp4')
    
    combined2_dir = os.path.join(output_dir, 'combined2', model_id)
    ply_path = os.path.join(combined2_dir,"combined2.ply")
    # 加载PLY文件
    # ply_path = "combined2.ply"  # 替换为你的PLY文件路径
    point_cloud = o3d.io.read_point_cloud(ply_path)
    # def custom_draw_geometry_with_rotation(pcd):
    #     def rotate_view(vis):
    #         ctr = vis.get_view_control()
    #         ctr.rotate(10.0, 0.0)
    #         return False
    
    #     o3d.visualization.draw_geometries_with_animation_callback([pcd],
    #                                                               rotate_view)
    # custom_draw_geometry_with_rotation(point_cloud)
    # 创建一个可视化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # 将点云添加到可视化窗口
    vis.add_geometry(point_cloud)

    # 设置旋转的速度和角度
    rotation_speed = 10  # 每次旋转的度数
    num_frames = 5.90* 360 // rotation_speed  # 计算总帧数

    # 准备一个图像列表来存储每一帧
    frames = []

    # 获取视图控制器并设置初始视图点
    view_ctl = vis.get_view_control()
    view_ctl.set_front([0, 0, -1])  # 设置视图的前方向
    view_ctl.set_lookat([0, 0, 0])  # 设置视图的焦点
    view_ctl.set_up([0, -1, 0])     # 设置视图的上方向
    view_ctl.set_zoom(0.8)          # 设置视图的缩放级别
    opt = vis.get_render_option()
    opt.point_size = 5  # 更改点的大小


    # 开始旋转动画
    for i in range(int(num_frames)):
        
        # 每次旋转一个小角度
        view_ctl.rotate(rotation_speed, 0)
        vis.update_geometry(point_cloud)
        vis.poll_events()
        vis.update_renderer()
        
        # 捕获当前窗口作为图像
        image = vis.capture_screen_float_buffer(False)
        image = np.asarray(image)
        image = (image * 255).astype(np.uint8)  # 将图像从浮点数转换为8位整数格式
        frames.append(image)
    # for i in range(int(num_frames)):
    #     # 每次旋转一个小角度
    #     view_ctl.rotate(0, rotation_speed)
    #     vis.update_geometry(point_cloud)
    #     vis.poll_events()
    #     vis.update_renderer()
        
    #     # 捕获当前窗口作为图像
    #     image = vis.capture_screen_float_buffer(False)
    #     image = np.asarray(image)
    #     image = (image * 255).astype(np.uint8)  # 将图像从浮点数转换为8位整数格式
    #     frames.append(image)
    # 结束动画后关闭窗口
    vis.destroy_window()

    # 使用imageio将帧写入视频文件
    writer = imageio.get_writer(video_filename, fps=30)  # 设置视频帧率
    for frame in frames:
        writer.append_data(frame)
    writer.close()

    print(f"视频已保存为 {video_filename}")
    break
