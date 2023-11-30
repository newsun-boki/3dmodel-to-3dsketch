##将点云转化为npy
import numpy as np
from plyfile import PlyData, PlyElement
import pandas as pd
import os
file_dir = 'output/pcd/small_chair/0.ply'  #文件的路径
npy_dir = 'output/npy/small_chair'
os.makedirs(npy_dir,exist_ok=True)

plydata = PlyData.read(file_dir)  # 读取文件
data = plydata.elements[0].data  # 读取数据
data_pd = pd.DataFrame(data)  # 转换成DataFrame, 因为DataFrame可以解析结构化的数据
print(data_pd.shape)
pcl = np.zeros(data_pd.shape, dtype=np.float32)  # 初始化储存数据的array
property_names = data[0].dtype.names  # 读取property的名字
for i, name in enumerate(property_names):  # 按property读取数据，这样可以保证读出的数据是同样的数据类型。
    pcl[:, i] = data_pd[name]
i = 0
np.save(os.path.join(npy_dir,'%d.npy' % i),pcl)
print(pcl.shape)
