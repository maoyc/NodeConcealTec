import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import warnings
warnings.filterwarnings("ignore") #过滤掉警告的意思
# from pyforest import *


#图片显示中文
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] =False #减号unicode编码

config = {
    "font.family": 'serif',
    "font.size": 10,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)

# 读取 excel 文件
df = pd.read_excel('comm_conceal.xlsx')

# 获取第一列数据
col1 = df.iloc[1:, 3].tolist()
print(col1)
col2 = df.iloc[1:, 4].tolist()
print(col2)
col3 = df.iloc[1:, 5].tolist()
print(col3)
col4 = df.iloc[1:, 6].tolist()
print(col4)
col5 = df.iloc[1:, 7].tolist()
print(col5)
col6 = df.iloc[1:, 8].tolist()
print(col6)
col7 = df.iloc[1:, 9].tolist()
print(col7)

cd_attack = []
for i in range(0, len(col1), 4):
    cd_attack.append([col1[i], col1[i+1], col1[i+2], col1[i+3]])
print(cd_attack)
cgn = []
for i in range(0, len(col2), 4):
    cgn.append([col2[i], col2[i+1], col2[i+2], col2[i+3]])
print(cgn)
q_attack = []
for i in range(0, len(col3), 4):
    q_attack.append([col3[i], col3[i+1], col3[i+2], col3[i+3]])
print(q_attack)
dice = []
for i in range(0, len(col4), 4):
    dice.append([col4[i], col4[i+1], col4[i+2], col4[i+3]])
print(dice)
neural = []
for i in range(0, len(col5), 4):
    neural.append([col5[i], col5[i+1], col5[i+2], col5[i+3]])
print(neural)
safeness = []
for i in range(0, len(col6), 4):
    safeness.append([col6[i], col6[i+1], col6[i+2], col6[i+3]])
print(safeness)
random = []
for i in range(0, len(col7), 4):
    random.append([col7[i], col7[i+1], col7[i+2], col7[i+3]])
print(random)

# ax = plt.subplots(figsize=(20, 16))#调整画布大小
# plt.subplot(1,7,1)   #221亦可
# ax_0 = sns.heatmap(cd_attack,cmap=sns.cubehelix_palette(15,rot=-.2,reverse=True), vmax=.8, square=True, cbar=False)#画热力图   annot=True 表示显示系数
# plt.title('CD-ATTACK')
#
# plt.subplot(1,7,2)   #221亦可
# ax_1 = sns.heatmap(cgn,cmap=sns.cubehelix_palette(15,rot=-.2,reverse=True), vmax=.8, square=True, cbar=False)#画热力图   annot=True 表示显示系数
# plt.yticks([])
# plt.title('CGN')
#
# plt.subplot(1,7,3)   #221亦可
# ax_2 = sns.heatmap(q_attack,cmap=sns.cubehelix_palette(15,rot=-.2,reverse=True), vmax=.8, square=True, cbar=False)#画热力图   annot=True 表示显示系数
# plt.yticks([])
# plt.title('Q-Attack')
#
# plt.subplot(1,7,4)   #221亦可
# ax_3 = sns.heatmap(dice,cmap=sns.cubehelix_palette(15,rot=-.2,reverse=True), vmax=.8, square=True, cbar=False)#画热力图   annot=True 表示显示系数
# plt.yticks([])
# plt.title('DICE')
#
# plt.subplot(1,7,5)   #221亦可
# ax_4 = sns.heatmap(neural,cmap=sns.cubehelix_palette(15,rot=-.2,reverse=True), vmax=.8, square=True, cbar=False)#画热力图   annot=True 表示显示系数
# plt.yticks([])
# plt.title('NEURAL')
#
# plt.subplot(1,7,6)   #221亦可
# ax_5 = sns.heatmap(safeness,cmap=sns.cubehelix_palette(15,rot=-.2,reverse=True), vmax=.8, square=True, cbar=False)#画热力图   annot=True 表示显示系数
# plt.yticks([])
# plt.title('safeness')
#
# plt.subplot(1,7,7)   #221亦可
# ax_6 = sns.heatmap(random,cmap=sns.cubehelix_palette(15,rot=-.2,reverse=True), vmax=.8, square=True, cbar=False)#画热力图   annot=True 表示显示系数
# plt.yticks([])
# plt.title('random')

vmin = 0.6
vmax = 1.0
# sns.set_style('whitegrid', {'font.sans-serif': ['simhei','FangSong']})
fig, axs = plt.subplots(ncols=8, gridspec_kw=dict(width_ratios=[2,2,2,2,2,2,2,0.2]))


ax0=sns.heatmap(cd_attack, linewidths=.4, xticklabels=['FG', 'LP', 'LOU', 'INF'],yticklabels=['BA300','ER300','WS300', 'BA10000', 'ER10000','WS10000','685-Bus','Circuit','USAir97','US-Grid','DBLP','PubMed'],cbar=False, ax=axs[0], vmin=vmin)
ax0.set_title('CD-ATTACK')
ax1=sns.heatmap(cgn, linewidths=.4, xticklabels=['FG', 'LP', 'LOU', 'INF'], yticklabels=False, cbar=False, ax=axs[1], vmax=vmax)
ax1.set_title('CGN')
ax2=sns.heatmap(q_attack, linewidths=.4, xticklabels=['FG', 'LP', 'LOU', 'INF'], yticklabels=False, cbar=False, ax=axs[2])
ax2.set_title('Q-Attack')
ax3=sns.heatmap(dice, linewidths=.4, xticklabels=['FG', 'LP', 'LOU', 'INF'], yticklabels=False, cbar=False, ax=axs[3])
ax3.set_title('DICE')
ax4=sns.heatmap(neural, linewidths=.4, xticklabels=['FG', 'LP', 'LOU', 'INF'], yticklabels=False, cbar=False, ax=axs[4])
ax4.set_title('NEURAL')
ax5=sns.heatmap(safeness, linewidths=.4, xticklabels=['FG', 'LP', 'LOU', 'INF'], yticklabels=False, cbar=False, ax=axs[5])
ax5.set_title('SAFENESS')
ax6=sns.heatmap(random, linewidths=.4, xticklabels=['FG', 'LP', 'LOU', 'INF'], yticklabels=False, cbar=False, ax=axs[6])
ax6.set_title('RANDOM')



fig.colorbar(axs[1].collections[0], cax=axs[7])
axs[7].set_ylabel("NMI", rotation=-90, va="bottom")

# 设置刻度字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# 设置主刻度的标签， 带入主刻度旋转角度和字体大小参数
# ax_0.set_xticklabels(['FG', 'LP', 'ML', 'INF'], rotation=45, fontsize=12)
# ax_1.set_xticklabels(['FG', 'LP', 'ML', 'INF'], rotation=45, fontsize=12)
# ax_2.set_xticklabels(['FG', 'LP', 'ML', 'INF'], rotation=45, fontsize=12)
# ax_3.set_xticklabels(['FG', 'LP', 'ML', 'INF'], rotation=45, fontsize=12)
# ax_4.set_xticklabels(['FG', 'LP', 'ML', 'INF'], rotation=45, fontsize=12)
# ax_5.set_xticklabels(['FG', 'LP', 'ML', 'INF'], rotation=45, fontsize=12)
# ax_6.set_xticklabels(['FG', 'LP', 'ML', 'INF'], rotation=45, fontsize=12)
# ax_0.set_yticklabels(['ba300','er300','ws300', 'ba10000', 'er10000','ws10000','bus','circuit','USAir','power','DBLP','Pubmed'], rotation=45, fontsize=12)   # 不显示‘five’
# plt.savefig(r'C:/Users/hello/Desktop/comm_heatmap', dpi=200, bbox_inches='tight')
plt.show()
