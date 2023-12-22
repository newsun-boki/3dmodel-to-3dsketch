import cv2
import numpy as np
import os
video_files = os.listdir("output/videos")
if not os.path.exists("output/imgs"):
    os.mkdir("output/imgs")
print(video_files)
for i in range(len(video_files)):
    video_path = os.path.join("output/videos",video_files[i])
    img_dir = os.path.join("output/imgs",video_files[i][:-4])
    print(img_dir)
    os.mkdir(img_dir)
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # 用于保存提取的黑色部分的图像
    black_frames = []
    i = 0
    cnt = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break  # 退出循环，视频已经读取完毕
        i = i + 1
        if(i == 2):
            height, width, _ = frame.shape
            scale_factor = min(1000 / width, 1)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            frame = cv2.resize(frame, (new_width, new_height))
            # 将帧转换为灰度图像
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 使用阈值将黑色部分分离出来（可以根据需要调整阈值）
            _, black_mask = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)
            # _, black_mask = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # 创建一个具有白色背景的图像
            white_background = np.full_like(frame, (255, 255, 255), dtype=np.uint8)

            # 将黑色部分与白色背景相加，从而将背景颜色更改为白色
            white_background_with_black = cv2.add(white_background, frame, mask=black_mask)
            img = cv2.cvtColor(white_background_with_black,cv2.COLOR_RGB2GRAY)

            # 保存提取的黑色部分的图像
            # black_frames.append(black_part)
            
            # cv2.imshow("11",white_background_with_black)
            # cv2.waitKey(0)
            cv2.imwrite(os.path.join(img_dir,str(cnt)+ '.png'), img)
            cnt = cnt + 1
            # print(cnt)
            i = 0

    # 释放视频捕获对象
    cap.release()

    # 保存提取的黑色部分图像为图像文件

    # 关闭OpenCV窗口
    cv2.destroyAllWindows()
