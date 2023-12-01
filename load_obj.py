import open3d as o3d
import numpy as np

# 读取OBJ文件
def load_obj_with_lines(filename):
    vertices = []
    lines = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                # 处理顶点信息
                vertex = list(map(float, line.strip().split()[1:]))
                vertices.append(vertex)
            elif line.startswith('l '):
                # 处理线信息
                line_indices = list(map(int, line.strip().split()[1:]))
                adjusted_indices = [index - 1 for index in line_indices]
                lines.append(adjusted_indices)

    return np.array(vertices), np.array(lines)

# 加载OBJ文件中的顶点和线信息
vertices, lines = load_obj_with_lines('curves.obj')

# 创建Open3D的LineSet对象
line_set = o3d.geometry.LineSet()
line_set.points = o3d.utility.Vector3dVector(vertices)
line_set.lines = o3d.utility.Vector2iVector(lines)

# 可视化线模型
o3d.visualization.draw_geometries([line_set])
