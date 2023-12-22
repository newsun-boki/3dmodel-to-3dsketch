import open3d as o3d
import numpy as np
import imageio

video_filename = "obj_rotation.mp4"

# 加载OBJ文件中的顶点和线信息
mesh = o3d.io.read_triangle_mesh("plys/model.obj")


# 可视化线模型
# o3d.visualization.draw_geometries([mesh])


vis = o3d.visualization.Visualizer()
vis.create_window()

# 将点云添加到可视化窗口
vis.add_geometry(mesh)

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
view_ctl.rotate(0, 6*180)
# 开始旋转动画
for i in range(int(num_frames)):
    
    # 每次旋转一个小角度
    view_ctl.rotate(rotation_speed, 0)
    vis.update_geometry(mesh)
    vis.poll_events()
    vis.update_renderer()
    
    # 捕获当前窗口作为图像
    image = vis.capture_screen_float_buffer(False)
    image = np.asarray(image)
    image = (image * 255).astype(np.uint8)  # 将图像从浮点数转换为8位整数格式
    frames.append(image)

# 结束动画后关闭窗口
vis.destroy_window()

# 使用imageio将帧写入视频文件
writer = imageio.get_writer(video_filename, fps=30)  # 设置视频帧率
for frame in frames:
    writer.append_data(frame)
writer.close()

print(f"视频已保存为 {video_filename}")