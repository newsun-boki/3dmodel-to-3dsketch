#!/bin/bash

# 循环从0到16
for number in {0..16}
do
    # 执行Python脚本并传递参数
    python all_direction_show_model.py --number $number
done