import numpy as np
import matplotlib.pyplot as plt

# 数据列表
data = [0, 0, 0, 0, 5, 12, 45, 62, 64, 55, 26, 23, 8]

# 将数据列表转换为NumPy数组
data_np = np.array(data)

# 创建一个布尔数组，表示哪些点的值不为0
non_zero_mask = data_np != 0

# 创建一个新的NumPy数组，其中仅包含值不为0的点
non_zero_data = data_np[non_zero_mask]

# 创建一个包含x轴坐标的NumPy数组
x_values = np.arange(len(data))

# 创建一个包含x轴坐标的NumPy数组，其中仅包含值不为0的点
non_zero_x_values = x_values[non_zero_mask]

# 创建一个新的Matplotlib图形
fig, ax = plt.subplots()

# 绘制折线图，其中仅包含值不为0的点
ax.plot(non_zero_x_values, non_zero_data)

# 显示图形
plt.show()
