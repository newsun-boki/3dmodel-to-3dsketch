import OpenEXR, Imath, numpy
import matplotlib.pyplot as plt

def main(file_name):
    # 打开EXR文件
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    golden = OpenEXR.InputFile(file_name)

    # 获取数据窗口
    dw = golden.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # 从R通道中读取数据
    redstr = golden.channel('R', pt)
    red = numpy.fromstring(redstr, dtype=numpy.float32)
    red.shape = (size[1], size[0])  # 将数据重塑为图像形状

    red_min = red.min()
    # 移除最大值（或其他异常值）
    max_value = red.max()
    red[red == max_value] = red_min  # 将最大值替换为0或其他合适的值

    # 归一化处理
    # red_min = red.min()
    red_max = red.max()
    red_normalized = (red - red_min) / (red_max - red_min)  # 归一化到 [0, 1]
    bg_value =-red_min /  red_max - red_min
    red_normalized[red_normalized == 0] = 1
    # tolerance = 1e-2 # 定义容忍度
    # red_normalized[numpy.isclose(red_normalized, max_value, rtol=tolerance)] = -0.1
    # 显示图像
    # ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'gray']
    plt.matshow(red_normalized, cmap='gray')  # 使用 ‘plasma’'viridis' 色图进行显示，也可以使用其他色图
    plt.colorbar()  # 添加颜色条以显示值与颜色的对应关系
    plt.title("Normalized R Channel")  # 设置图像标题
    plt.show()  # 显示图像

if __name__ == "__main__":
    for i in range(5):
        file_name = f"/Users/wuzhu/Downloads/wooden-chair-ply/output/exr/small_chair/{i}.exr"
        main(file_name)