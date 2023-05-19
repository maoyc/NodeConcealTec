import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义幂函数
def power_function(x, a, b):
    return a * np.power(x, b)

# 三个点的坐标
x = np.array([0, 300, 1000])
y = np.array([0.02, 0.055, 0.0652])

# 使用curve_fit函数进行拟合
popt, pcov = curve_fit(power_function, x, y, maxfev=10000)

# 生成1000个点
x_new = np.linspace(0, 1000, 1000)
y_new = power_function(x_new, *popt)

# 将y值减去0.02，并限制在0.02到0.0652之间
y_new = np.clip(y_new - 0.02, 0, 0.0452) + 0.02

# 加入一些噪声
noise = np.random.normal(0, 0.001, size=len(x_new))
y_new = y_new + noise

# 绘制拟合曲线和原始数据点
plt.plot(x, y, 'o', label='原始数据点')
plt.plot(x_new, y_new, label='拟合曲线')
plt.ylim((0, 0.07)) # 设置y轴范围
plt.legend()
plt.show()
