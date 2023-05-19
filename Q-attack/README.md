# Q-Attack

# How to run examples

python community_deception_via_ga.py --dataset karate --model LP --attack_num 8 -- iterNum 500
1. --dataset 数据集：karate、dolphins、football、polbooks
2. --model 社团检测算法：
            'INF': infomap,
            'LP': label_propagation,  
            'FG': fastgreedy,
            'WT': walktrap,
            'LE': leading_eigenvector,
            'LU': multilevel,
            'EB': edgebetweenness
3. --attack_num 攻击次数
4. --iterNum 算法迭代次数

# Result
程序运行日志保存至log/attack/ga-attack/下，包含最终生成的对抗网络（gml文件）以及，500次迭代的种群最优个体的fitness值与对应的对抗网络的模块度，以及平均模块度与fitness