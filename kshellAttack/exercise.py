# -*- coding: utf-8 -*-
# @Time : 2021/6/4 16:00
# @Author : Mao Yongchao
# @Site : 
# @File : exercise.py
# @Software: PyCharm

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import math
import random
import pickle

from sklearn.metrics import confusion_matrix
import genetic as AP
import RLmain as QL
from matplotlib.gridspec import GridSpec


# 该函数为根据连边信息生成图
def generate_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


# 该函数为k-shell分解算法
def k_shell(graph_copy):
    graph = nx.Graph(graph_copy)  # 复制一个图可以是一个networkx的图或者边集
    importance_dict = defaultdict(list)
    k = 1  # 初始k值
    while len(graph.degree):  # 返回节点的个数
        while True:
            level_node_list = []
            for item in graph.degree:  # 列表元祖，元组前面是节点编号，后面是节点的度
                if item[1] <= k:
                    level_node_list.append(item[0])
            graph.remove_nodes_from(level_node_list)
            importance_dict[k].extend(level_node_list)
            if not len(graph.degree):
                return importance_dict
            if min(graph.degree, key=lambda x: x[1])[1] > k:
                break
        k = min(graph.degree, key=lambda x: x[1])[1]
    return importance_dict


# 该函数为模拟退火攻击
def annealing_attack(attack_number, edge_len, k_distribution_orignal, edges):
    edges = list(edges)
    edges_copy_trans = edges[:]
    acc_old = 1.0
    for m in tqdm(range(attack_number)):  # 攻击次数，借鉴强化学习的那个图展示攻击
        T = 100  # 初温
        Tmin = 20  # 稳态温度
        t = 0
        while T >= Tmin:
            for i in range(100):

                combind_code = []  # 保证交叉的可行性也就是重连的两条边不存在公共顶点
                for i in range(len(edges_copy_trans) - 1):
                    for j in range(i + 1, len(edges_copy_trans)):
                        if len(set(edges_copy_trans[i]).intersection(set(edges_copy_trans[j]))) != 0:
                            continue
                        combind_code.append((i, j))
                a = random.sample(combind_code, 1)[0]  # (,)
                # prepare_attack_edge = [edges_copy[a[0]],edges_copy[a[1]]]
                e_one = edges_copy_trans[a[0]]
                e_two = edges_copy_trans[a[1]]

                e_one_new_cros = (e_one[0], e_two[1])
                e_two_new_cros = (e_two[0], e_one[1])
                e_one_new_direc = (e_one[0], e_two[0])
                e_two_new_direc = (e_one[1], e_two[1])
                cros_label = 0  # 等于0表示可以进行交叉重连
                direc_label = 0  # 等于0表示可以顶点直连
                for x in edges_copy_trans:
                    if set(e_one_new_cros) == set(x) or set(e_two_new_cros) == set(x):
                        e_one_new = e_one
                        e_two_new = e_two
                        cros_label = 1
                        break
                for x in edges_copy_trans:
                    if set(e_one_new_direc) == set(x) or set(e_two_new_direc) == set(x):
                        e_one_new = e_one
                        e_two_new = e_two
                        direc_label = 1
                        break
                if cros_label == 0 and direc_label == 0:
                    if random.random() < 0.5:
                        e_one_new = e_one_new_cros
                        e_two_new = e_two_new_cros
                    else:
                        e_one_new = e_one_new_direc
                        e_two_new = e_two_new_direc
                if cros_label == 0 and direc_label == 1:
                    e_one_new = e_one_new_cros
                    e_two_new = e_two_new_cros
                if cros_label == 1 and direc_label == 0:
                    e_one_new = e_one_new_direc
                    e_two_new = e_two_new_direc
                if cros_label == 1 and direc_label == 1:
                    continue

                edges_copy_trans[a[0]] = e_one_new
                edges_copy_trans[a[1]] = e_two_new
                # G = generate_graph(edges_copy_trans)
                k_distribution = k_shell(edges_copy_trans)  # 计算攻击以后的图k值
                acc_new = accuracy(k_distribution_orignal, k_distribution)
                if acc_new < acc_old:  # 分类精度下降
                    acc_old = acc_new
                else:
                    p = math.exp(-(acc_new - acc_old) / T)  # 概率要小于1
                    r = random.uniform(0, 1)  # 产生[0,1]区间的浮点数，
                    if r < p:  # 以一定的概率接受更改
                        acc_old = acc_new

                    else:
                        edges_copy_trans[a[0]] = e_one
                        edges_copy_trans[a[1]] = e_two
            # t=t+1
            T = T * 0.85

    attack_edge_number = 0
    for i in edges_copy_trans:
        for j in edges:
            if set(i) == set(j):
                attack_edge_number = attack_edge_number + 1
                break
    attack_edge_number = edge_len - attack_edge_number
    attack_acc = 1.0 - acc_old
    return attack_acc, attack_edge_number, edges_copy_trans  # 分别返回攻击精度、攻击的边的个数、攻击后的图


# 该函数为k-shell可视化
def color_map(graph, distribution):
    colormap = []
    for node in graph:
        for key, values in distribution.items():
            if key == 1:
                if node in values:
                    colormap.append('red')
            if key == 2:
                if node in values:
                    colormap.append('blue')
            if key == 3:
                if node in values:
                    colormap.append('green')
    return colormap


# k-shell的分类精度,该返回值越大，则攻击效果越差
def accuracy(k_distribution_orignal, k_distribution):
    acc_absolute = 0
    node_number = 0
    for key in sorted(k_distribution_orignal.keys()):
        acc_absolute = acc_absolute + len(set(k_distribution_orignal[key]) & set(k_distribution[key]))  # 精度的位置放在哪里是个关键
        node_number = node_number + len(k_distribution_orignal[key])
    acc_attack = acc_absolute / node_number
    return acc_attack


# 此函数为随机攻击
def random_attack(edges, k_distribution_orignal, edges_len):
    edges = list(edges)
    edges_copy_trans = edges[:]  # 保留上次攻击后参数的图
    acc_old = 1.0

    for i in tqdm(range(5)):  # 攻击5次,更改过后的边再更改回去
        for j in range(len(edges_copy_trans) - 1):
            for k in range(j + 1, len(edges_copy_trans)):
                e_one = edges_copy_trans[j]
                e_two = edges_copy_trans[k]
                if e_one[0] == e_two[1] or e_two[0] == e_one[1]:  # 有公共点，不交叉
                    continue
                elif e_one[0] == e_two[0] or e_two[1] == e_one[1]:
                    continue
                else:
                    if random.random() < 0.5:
                        e_one_new = (e_one[0], e_two[1])
                        e_two_new = (e_two[0], e_one[1])
                    else:
                        e_one_new = (e_one[0], e_two[0])
                        e_two_new = (e_one[1], e_two[1])
                for i in edges_copy_trans:
                    if set(e_one_new) == set(i) or set(e_two_new) == set(i):
                        flag = False
                        break
                    else:
                        flag = True
                        continue
                if not flag:  # 表示重连以后出现已有边，则跳出本次循环
                    continue
                edges_copy_trans[j] = e_one_new
                edges_copy_trans[k] = e_two_new
                k_distribution = k_shell(edges_copy_trans)
                acc_new = accuracy(k_distribution_orignal, k_distribution)

                if acc_new < acc_old:
                    acc_old = acc_new
                else:  # 重连边以后分类精度没有发生变化，是否以一定的概率决定是否决定重连边，因为有可能重连以后对后续的选择有帮助
                    edges_copy_trans[j] = e_one
                    edges_copy_trans[k] = e_two

    attack_edge_number = 0
    for i in edges_copy_trans:
        for j in edges:
            if set(i) == set(j):
                attack_edge_number = attack_edge_number + 1
                break
    attack_edge_number = edges_len - attack_edge_number
    attack_acc = 1.0 - acc_old
    return attack_acc, attack_edge_number, edges_copy_trans


# 此函数暂时用不到
def node_k(graph, distribution):
    node_list_k = []
    for node in graph:
        for key, values in distribution.items():
            if node in values:
                a = '0x{:02X}'.format(key)
                colo = '#FF00' + a[2:]
                node_list_k.append(colo)
                break
        continue

    return node_list_k


# 该函数为混淆矩阵
def confusionmatrix_fuc(k_distribution_original, k_distribution, nodes):
    true_label = []
    pred_label = []
    for i in sorted(nodes):
        for key, value in k_distribution_original.items():
            if i in value:
                true_label.append(key)
                break
        for key, value in k_distribution.items():
            if i in value:
                pred_label.append(key)
                break
    confusionmatrix = confusion_matrix(true_label, pred_label)

    return confusionmatrix


def attack_edge_number_computation(edges, attack_edges):
    similar_edge_number = 0
    for i in attack_edges:
        for j in edges:
            if set(i) == set(j):
                similar_edge_number = similar_edge_number + 1
                break
    attack_edge_number = len(edges) - similar_edge_number
    return attack_edge_number


def degree_isdifferent(original_G, attack_G):
    node_number = []
    original_nod = sorted(list(original_G.nodes))
    attack_nod = sorted(list(attack_G.nodes))
    if set(original_nod) != set(attack_nod):
        return True
    for i in range(len(original_nod)):
        if original_G.degree(original_nod[i]) != attack_G.degree(original_nod[i]):
            node_number.append(i)
            continue
    if node_number:
        return True
    else:
        return False


if __name__ == '__main__':
    file = open("dolphin.pkl", "rb")
    edges = pickle.load(file)

    G = generate_graph(edges)
    edges = G.edges
    nodes = G.nodes
    edges_len = len(edges)
    # 原始图
    k_distribution_orignal = k_shell(G)
    node_original = color_map(G, k_distribution_orignal)

    # 模拟退火攻击
    # acc_anneal, edgenumber_anneal, edge_anneal = annealing_attack(5, edges_len, k_distribution_orignal, edges)
    # graph_annealattack = generate_graph(edge_anneal)
    # k_distribution_annealattack = k_shell(graph_annealattack)
    # nodecolor_aneal = color_map(graph_annealattack, k_distribution_annealattack)
    # node_change_anneal = degree_isdifferent(G, graph_annealattack)
    # print("anneal_Accurate_attack:{},number_attack:{}".format(acc_anneal, edgenumber_anneal))
    # print("is node degree change after anneal:{}".format(node_change_anneal))
    # confusionmatrix_anneal = confusionmatrix_fuc(k_distribution_orignal,k_distribution_annealattack,nodes)
    # print(k_distribution_annealattack)
    # print(confusionmatrix_anneal)

    # 全局攻击
    acc_random, edgenumber_random, edge_random = random_attack(edges, k_distribution_orignal, edges_len)
    graph_randomattack = generate_graph(edge_random)
    k_distribution_randomattack = k_shell(graph_randomattack)
    nodecolor_random = color_map(graph_randomattack, k_distribution_randomattack)
    node_change_random = degree_isdifferent(G, graph_randomattack)
    print("random_Accurate_attack:{},number_attack:{}".format(acc_random, edgenumber_random))
    print("is node degree change after random:{}".format(node_change_random))
    confusionmatrix_anneal = confusionmatrix_fuc(k_distribution_orignal,k_distribution_randomattack,nodes)
    print(k_distribution_randomattack)
    print(confusionmatrix_anneal)

    # 遗传算法攻击
    # new_edges = AP.genetic_algorithm_attack(edges, k_distribution_orignal)
    # graph_geneticattack = generate_graph(new_edges)
    # k_distribution_geneticattack = k_shell(graph_geneticattack)
    # acc_genetic = 1.0 - accuracy(k_distribution_orignal, k_distribution_geneticattack)
    # nodecolor_genetic = color_map(graph_geneticattack, k_distribution_geneticattack)
    # edgenumber_genetic = attack_edge_number_computation(edges, new_edges)
    # node_change_genetic = degree_isdifferent(G, graph_geneticattack)
    # print("gentic_Accurate_attack:{},number_attack:{}".format(acc_genetic, edgenumber_genetic))
    # print("is node degree change after genetic:{}".format(node_change_genetic))

    # 强化学习算法攻击
    # ql_edges = QL.QLearning_attack(edges)
    # graph_QLattack = generate_graph(ql_edges)
    # k_distribution_QLattack = k_shell(graph_QLattack)
    # acc_QL = 1.0 - accuracy(k_distribution_orignal, k_distribution_QLattack)
    # nodecolor_QL = color_map(graph_QLattack, k_distribution_QLattack)
    # edgenumber_QL = attack_edge_number_computation(edges, ql_edges)
    # node_change_QL = degree_isdifferent(G, graph_QLattack)
    # print("QL_Accurate_attack:{},number_attack:{}".format(acc_QL, edgenumber_QL))
    # print("is node degree change after QL:{}".format(node_change_QL))

    # 画图
    # figure1 = plt.figure(constrained_layout=True)
    # gs = GridSpec(3, 2, figure=figure1)
    # ax1 = figure1.add_subplot(gs[0, 0])
    # ax1.set_title("originalgraph")
    # ax2 = figure1.add_subplot(gs[0, 1])
    # ax2.set_title("annealattack graph")
    # ax3 = figure1.add_subplot(gs[1, 0])
    # ax3.set_title("randomattack graph")
    # ax4 = figure1.add_subplot(gs[1, 1])
    # ax4.set_title("geneticattack graph")
    # ax5 = figure1.add_subplot(gs[2, :])
    # ax5.set_title("reinforce learning attack graph")

    # nx.drawing.nx_pylab.draw_networkx(G, ax=ax1, node_color=node_original, with_labels=True)
    # nx.drawing.nx_pylab.draw_networkx(graph_annealattack, ax=ax2, node_color=nodecolor_aneal, with_labels=True)
    # nx.drawing.nx_pylab.draw_networkx(graph_randomattack, ax=ax3, node_color=nodecolor_random, with_labels=True)
    # nx.drawing.nx_pylab.draw_networkx(graph_geneticattack, ax=ax4, node_color=nodecolor_genetic, with_labels=True)
    # nx.drawing.nx_pylab.draw_networkx(graph_QLattack, ax=ax5, node_color=nodecolor_QL, with_labels=True)
    # plt.show()
