import bpy
import mathutils
import numpy as np
import os
import sys
import time
import datetime

# 获取当前日期和时间
current_time = datetime.datetime.now()

# 根据需要自定义日期时间格式
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
def random_pose():
    angle_x = np.random.uniform() * 2 * np.pi
    angle_y = np.random.uniform() * 2 * np.pi
    angle_z = np.random.uniform() * 2 * np.pi
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(angle_x), -np.sin(angle_x)],
                   [0, np.sin(angle_x), np.cos(angle_x)]])
    Ry = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                   [0, 1, 0],
                   [-np.sin(angle_y), 0, np.cos(angle_y)]])
    Rz = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                   [np.sin(angle_z), np.cos(angle_z), 0],
                   [0, 0, 1]])
    R = np.dot(Rz, np.dot(Ry, Rx))
    # Set camera pointing to the origin and 1 unit away from the origin
    t = np.expand_dims(R[:, 2]*10, 1)
    pose = np.concatenate([np.concatenate([R, t], 1), [[0, 0, 0, 1]]], 0)
    return pose


def setup_blender(width, height, focal_length):
    ##这里切换为正交视角，因为wonder3d输出模型为正交视角的
    # bpy.ops.view3d.view_persportho()
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

    # 光源位置的列表，每个元素代表一个象限的位置
    light_positions = [
        # (5, 5, 5),
        (5, 5, -5),
        (5, -5, 5),
        # (5, -5, -5),
        (-5, 5, 5),
        (-5, 5, -5),
        # (-5, -5, 5),
        (-5, -5, -5)
    ]

    # 循环添加光源
    for i, position in enumerate(light_positions):
        light = bpy.data.lights.new(name=f'Light_{i}', type='POINT')
        light.energy = 150.0  # 光源强度，根据需要进行调整
        light_obj = bpy.data.objects.new(f'Light_{i}', object_data=light)
        light_obj.location = position
        bpy.context.collection.objects.link(light_obj)
        light.use_shadow = False  # 禁用光源的阴影

    # 设置默认渲染光源为新添加的光源
    # bpy.context.scene.collection.objects.unlink(bpy.context.scene.collection.objects[0])
    # camera
    camera = bpy.data.objects['Camera']
    # camera.data.type = 'ORTHO'
    camera.data.angle = np.arctan(width / 2 / focal_length) * 2
    bpy.data.scenes["Scene"].view_layers['ViewLayer'].use_pass_z
    # render layer
    scene = bpy.context.scene
    scene.render.filepath = 'buffer1'
    scene.render.image_settings.color_depth = '16'
    scene.render.resolution_percentage = 100
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.view_layers['ViewLayer'].use_pass_z = True#这里需要添加一下这个
    # compositor nodes 合成器节点
    scene.use_nodes = True
    tree = scene.node_tree
    rl = tree.nodes.new('CompositorNodeRLayers')
    output = tree.nodes.new('CompositorNodeOutputFile')
    output.base_path = ''
    output.format.file_format = 'OPEN_EXR'
    tree.links.new(rl.outputs['Depth'], output.inputs[0])

    # remove default cube
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()

    return scene, camera, output


if __name__ == '__main__':

    model_dir = 'plys/buildings'
    output_dir = "output"
    num_scans = 50 #扫描次数，自定义即可

    # 设置深度图的宽高和相机焦点，可以修改深度图和点云的分辨率
    nn = 10
    width = 160 * nn
    height = 120 * nn
    focal = 100 * nn
    scene, camera, output = setup_blender(width, height, focal)
    intrinsics = np.array([[focal, 0, width / 2], [0, focal, height / 2], [0, 0, 1]])
    # model_list = os.listdir(model_dir)
    # 获取文件夹内所有文件名（不包含后缀）
    model_list= [os.path.splitext(f)[0] for f in os.listdir(model_dir) if os.path.isfile(os.path.join(model_dir, f))]
    # model_list = ['building_big'] # 不包含后缀名
    open('blender.log', 'w+').close()
    os.system('rm -rf %s' % output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    np.savetxt(os.path.join(output_dir, 'intrinsics.txt'), intrinsics, '%f')
    for model_id in model_list:
        start = time.time()
        exr_dir = os.path.join(output_dir, 'exr', model_id)
        pose_dir = os.path.join(output_dir, 'pose', model_id)
        os.makedirs(exr_dir)
        os.makedirs(pose_dir)
        # Redirect output to log file
        old_os_out = os.dup(1)
        os.close(1)
        os.open('blender.log', os.O_WRONLY)
        # Import mesh model
        model_path = os.path.join(model_dir, model_id + '.ply') # 我的3D模型后缀名是 ply
        bpy.ops.import_mesh.ply(filepath=model_path)
        bpy.ops.transform.resize(value=(5.0, 5.0, 5.0))
        # Rotate model by 90 degrees around x-axis (z-up => y-up) to match ShapeNet's coordinates
        bpy.ops.transform.rotate(value=-np.pi / 2, orient_axis='X')
        # Render
        # 创建一个简单的材质
        mat = bpy.data.materials.new(name="SimpleMat")
        mat.diffuse_color = (1.0, 1.0, 1.0, 1.0)  # 白色
        mat.use_nodes = False  # 关闭节点以使用基础材质设置

        # 应用材质到所有物体
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                if len(obj.data.materials) == 0:
                    obj.data.materials.append(mat)
                else:
                    obj.data.materials[0] = mat
        for i in range(num_scans):
            print(f"number:{i}")
            scene.frame_set(i)
            pose = random_pose()
            camera.matrix_world = mathutils.Matrix(pose)
            print(f"output exr:{output.file_slots[0].path}")
            # 设置输出文件的格式为OpenEXR，并设置文件名
            # scene.render.image_settings.file_format = 'OPEN_EXR'
            # scene.render.image_settings.file_extension = 'exr'
            scene.render.filepath = os.path.join(exr_dir, f'{i}')
            output.file_slots[0].path = os.path.join(exr_dir, '#.exr')
            # output.file_slots[0].path = f'{formatted_time}_frame_{i:04d}'
            bpy.ops.render.render(write_still=True)
            np.savetxt(os.path.join(pose_dir, '%d.txt' % i), pose, '%f')
        # Clean up
        bpy.ops.object.delete()
        for m in bpy.data.meshes:
            bpy.data.meshes.remove(m)
        for m in bpy.data.materials:
            m.user_clear()
            bpy.data.materials.remove(m)

        # Show time
        os.close(1)
        os.dup(old_os_out)
        os.close(old_os_out)
        print('%s done, time=%.4f sec' % (model_id, time.time() - start))