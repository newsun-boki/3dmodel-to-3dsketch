import Imath
import OpenEXR
import argparse
import array
import numpy as np
import os
import open3d as o3d

import cv2

def callback(x):
    print(x)

def edge_detection(image_path):
    image = cv2.imread(image_path)
    # 转换图像为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 进行高斯模糊，消除噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 使用Canny方法进行边缘检测
    edges = cv2.Canny(blurred, 6, 40)
    if False:
        img = gray
        canny = cv2.Canny(img, 85, 255) 

        cv2.namedWindow('image') # make a window with name 'image'
        cv2.createTrackbar('L', 'image', 0, 255, callback) #lower threshold trackbar for window 'image
        cv2.createTrackbar('U', 'image', 0, 255, callback) #upper threshold trackbar for window 'image

        while(1):
            numpy_horizontal_concat = np.concatenate((img, canny), axis=1) # to display image side by side
            cv2.imshow('image', numpy_horizontal_concat)
            k = cv2.waitKey(1) & 0xFF
            if k == 27: #escape key
                break
            l = cv2.getTrackbarPos('L', 'image')
            u = cv2.getTrackbarPos('U', 'image')

            canny = cv2.Canny(img, l, u)

        cv2.destroyAllWindows()
    return edges

def read_exr(exr_path, height, width):
    file = OpenEXR.InputFile(exr_path)
    depth_arr = array.array('f', file.channel('R', Imath.PixelType(Imath.PixelType.FLOAT)))
    depth = np.array(depth_arr).reshape((height, width))
    depth[depth < 0] = 0
    depth[np.isinf(depth)] = 0
    return depth


def depth2pcd(depth, intrinsics, pose):
    inv_K = np.linalg.inv(intrinsics)
    inv_K[2, 2] = -1
    depth = np.flipud(depth) # 将矩阵进行上下翻转
    y, x = np.where(depth < 65504) # 返回索引
    # image coordinates -> camera coordinates
    points = np.dot(inv_K, np.stack([x, y, np.ones_like(x)] * depth[y, x], 0))
    # camera coordinates -> world coordinates
    points = np.dot(pose, np.concatenate([points, np.ones((1, points.shape[1]))], 0)).T[:, :3]
    return points


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('list_file')
    parser.add_argument('--intrinsics_file',default="output/intrinsics.txt")
    parser.add_argument('--output_dir',default="output")
    parser.add_argument('--num_scans', type=int, default=50)
    args = parser.parse_args()
    model_dir = 'plys/buildings'
    # model_list = ['building_big'] # 不包含后缀名
    model_list= [os.path.splitext(f)[0] for f in os.listdir(model_dir) if os.path.isfile(os.path.join(model_dir, f))]
    intrinsics = np.loadtxt(args.intrinsics_file)
    width = int(intrinsics[0, 2] * 2)
    height = int(intrinsics[1, 2] * 2)

    for model_id in model_list:
        depth_dir = os.path.join(args.output_dir, 'depth', model_id)
        pcd_dir = os.path.join(args.output_dir, 'pcd', model_id)
        if os.path.exists(depth_dir):
            os.system('rm -rf %s' % depth_dir)
        if os.path.exists(pcd_dir):
            os.system('rm -rf %s' % pcd_dir)
        os.makedirs(depth_dir, exist_ok=True)
        os.makedirs(pcd_dir, exist_ok=True)
        for i in range(args.num_scans):
            print(f"processing image {i}")
            exr_path = os.path.join(args.output_dir, 'exr', model_id, '%d.exr' % i)
            pose_path = os.path.join(args.output_dir, 'pose', model_id, '%d.txt' % i)
            rgb_path = os.path.join(args.output_dir, 'exr', model_id, '%d.png' % i)#把rgb图放到exr里去了
            edges = edge_detection(rgb_path)
            # print(edges.shape)
            # cv2.imshow("11",edges)
            # cv2.waitKey(0)
            depth = read_exr(exr_path, height, width)
            depth[edges == 0] = 0
            depth_img = o3d.geometry.Image(np.uint16(depth * 1000))
            o3d.io.write_image(os.path.join(depth_dir, '%d.png' % i), depth_img)

            pose = np.loadtxt(pose_path)
            points = depth2pcd(depth, intrinsics, pose)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            o3d.io.write_point_cloud(os.path.join(pcd_dir, '%d.ply' % i), pcd)
        print(f"{model_id} done")