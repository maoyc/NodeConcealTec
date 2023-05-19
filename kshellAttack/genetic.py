# -*- coding: utf-8 -*-
# @Time : 2021/6/4 16:00
# @Author : Mao Yongchao
# @Site : 
# @File : genetic.py
# @Software: PyCharm
# import copy
import random
from collections import defaultdict
import pickle
# import matplotlib.pyplot as plt
import networkx as nx
# from matplotlib.gridspec import GridSpec
from tqdm import tqdm
import xlwt

"""
individuals也就是chromosome,需要注意的是population has a fixed size,用端点来指引边貌似是可行的。
"""


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


def generate_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


# 该函数为k-shell分解算法
def k_shell(graph_copy):
    graph = nx.Graph(graph_copy)  # 复制一个图
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


# k-shell的分解精度,该返回值越大，则攻击效果越差
def accuracy(k_distribution_orignal, k_distribution):
    acc_absolute = 0
    node_number = 0
    for key in sorted(k_distribution.keys()):
        acc_absolute = acc_absolute + len(set(k_distribution_orignal[key]) & set(k_distribution[key]))  # 精度的位置放在哪里是个关键
        node_number = node_number + len(k_distribution[key])

    acc_attack = acc_absolute / node_number
    return acc_attack


def decode(edges, gen):  # gen=[(,),(,)],存的是改变的边的的端点表示。该函数是在当前基因下重连边生成的新图。
    edges_copy_trans = list(edges)

    e_one = gen[0]  # 第一条边（，）
    e_two = gen[1]  # 第二条边（，）
    e_one_index = [i for i, v in enumerate(edges_copy_trans) if set(v) == set(e_one)]
    e_two_index = [i for i, v in enumerate(edges_copy_trans) if set(v) == set(e_two)]
    if e_one_index == [] or e_two_index == []:  # 当前情况下准备重连的两条边不存在，则不执行重连，该基因无效
        return edges_copy_trans

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
    if cros_label == 0 and direc_label == 0:  # 随机重连或直连
        if random.random() < 0.5:
            e_one_new = e_one_new_cros
            e_two_new = e_two_new_cros
        else:
            e_one_new = e_one_new_direc
            e_two_new = e_two_new_direc
    if cros_label == 0 and direc_label == 1:  # 执行交叉重连
        e_one_new = e_one_new_cros
        e_two_new = e_two_new_cros
    if cros_label == 1 and direc_label == 0:  # 执行直连重连
        e_one_new = e_one_new_direc
        e_two_new = e_two_new_direc

    edges_copy_trans[e_one_index[0]] = e_one_new
    edges_copy_trans[e_two_index[0]] = e_two_new
    return edges_copy_trans


def construction_gen(edges):
    combind_code = []  # 保证交叉的可行性也就是重连的两条边不存在公共顶点
    for i in range(len(edges) - 1):
        for j in range(i + 1, len(edges)):
            if len(set(edges[i]).intersection(set(edges[j]))) != 0:
                continue
            combind_code.append((i, j))
    a = random.sample(combind_code, 1)[0]  # 类型为（，）去除准备攻击的边的序号，接下来映射为真实边的索引
    gen = [edges[a[0]], edges[a[1]]]  # 真实节点的边，[(),()]类型，（）存的是边的两个端点
    return gen


def generate_initial(num_total, len_chroms, edges):  # 染色体的组成均是第一次干净的边,初始迭代的时候保证组合可行性
    gen_edges = edges[:]
    initial_population = []  # 包含多个染色体[[[(),()],[(),()]],[]]类型
    chroms = []
    for i in range(num_total):  # 初始种群包含染色体的个数
        for j in range(len_chroms):
            gen = construction_gen(gen_edges)
            chroms.append(gen)  # gen的类型为[(),()],chroms类型为[[],[],]
            gen_edges = decode(gen_edges, gen)
        initial_population.append(chroms)
        gen_edges = edges[:]
        chroms = []
    return initial_population  # 初始种群


def sufficiency(initial, len_chroms, edges, k_distribution_orignal):  # 适应度函数是攻击成功率，越大越好
    edges = list(edges)
    scores = []  # 存储的是每个染色体体的适应度
    for j in range(len(initial)):  # 遍历每一个染色体
        edges_copy_trans = edges[:]
        for i in range(len_chroms):  # 遍历染色体中的每一个基因，基因存储的是准备重连边两条边（，）
            e_one = initial[j][i][0]  # 第一条边（，）
            e_two = initial[j][i][1]  # 第二条边（，）

            e_one_index = [k for k, v in enumerate(edges_copy_trans) if set(v) == set(e_one)]
            e_two_index = [k for k, v in enumerate(edges_copy_trans) if set(v) == set(e_two)]
            if e_one_index == [] or e_two_index == []:  # 无效的基因当前攻击图即不重连边
                continue

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
            elif cros_label == 0 and direc_label == 1:
                e_one_new = e_one_new_cros
                e_two_new = e_two_new_cros
            elif cros_label == 1 and direc_label == 0:
                e_one_new = e_one_new_direc
                e_two_new = e_two_new_direc
            else:
                continue  # 标记选择的两个边失效，虽然没有公共顶点但是既不能重连也不能直连。

            edges_copy_trans[e_one_index[0]] = e_one_new
            edges_copy_trans[e_two_index[0]] = e_two_new
        G = generate_graph(edges_copy_trans)
        k_distribution = k_shell(G)
        acc_new = 1.0 - accuracy(k_distribution_orignal, k_distribution)
        scores.append(acc_new)
    a = sum(scores)
    scores = [scores[i] / a for i in range(len(scores))]  # 每一个基因的适应度归一化,

    return scores


def selection(pop, scores, elitesize):  # 存储的是每个个体的适应度
    next_population = []
    sort_scores = sorted(scores, reverse=True)  # 适应度值从大到小排序。复制了scores的地址
    for i in range(elitesize):
        a = scores.index(sort_scores[i])
        next_population.append(pop[a])
    mid_adp = []
    mid_number = 0
    for i in range(len(scores)):  # 构建轮盘赌
        mid_number = scores[i] + mid_number
        mid_adp.append(mid_number)

    for i in range(len(scores) - elitesize):  # 控制选择的染色体。
        rand = random.uniform(0, 1)
        for j in range(len(scores)):
            if rand < mid_adp[j]:
                next_population.append(pop[j])
                break
            else:
                continue
    return next_population


def cross(next_population, cross_pro, elitesize):  # cross_pro为交叉概率,Python函数不要返回形参，否则容易出现问题
    next_population_copy = next_population[:]
    chroms_len = len(next_population[0])
    move = elitesize  # 当前基因移动的位置,最前面的是精英注意的
    while move < len(next_population) - 1:  # 减去1是因为move不能移到最后一个个体，如果种群个数是奇数（偶数），精英个体是偶数（奇数），则种群最后一个个体可能就被抛弃了。
        cur_pro = random.random()
        if cur_pro > cross_pro:  # 表示不进行交叉，不交叉的可能性要尽量小
            move += 2
            continue
        parent1 = move
        parent2 = move + 1
        index1 = random.randint(1, chroms_len - 2)  # 包括上下限，右侧是倒数第二个基因。注意下标索引
        index2 = random.randint(index1, chroms_len - 2)

        if index1 == index2:
            continue
        temp_gen1 = next_population_copy[parent1][index1:index2 + 1]  # +1是因为要包含右侧
        temp_gen2 = next_population_copy[parent2][index1:index2 + 1]
        temp_parent1 = next_population_copy[parent1][:]
        temp_parent2 = next_population_copy[parent2][:]
        temp_parent1[index1:index2 + 1] = temp_gen2
        temp_parent2[index1:index2 + 1] = temp_gen1
        pos = index1 + len(temp_gen1)  # 插入杂交基因片段的结束位置，被索引位置后加了一个1
        conflict1_ids, conflict2_ids = [], []
        for i, v in enumerate(temp_parent1):  # 原来存在的边更改消失但是又有可能回来。
            for w in temp_parent1[index1:pos]:
                if set(v[0]) == set(w[0]) or set(v[0]) == set(w[1]):
                    if set(v[1]) == set(w[0]) or set(v[1]) == set(w[1]):
                        if i not in list(range(index1, pos)):
                            conflict1_ids.append(i)

        for i, v in enumerate(temp_parent2):
            for w in temp_parent2[index1:pos]:
                if set(v[0]) == set(w[0]) or set(v[0]) == set(w[1]):
                    if set(v[1]) == set(w[0]) or set(v[1]) == set(w[1]):
                        if i not in list(range(index1, pos)):
                            conflict2_ids.append(i)

        for i, j in zip(conflict1_ids, conflict2_ids):
            temp_parent1[i], temp_parent2[j] = temp_parent2[j], temp_parent1[i]

        next_population_copy[parent1] = temp_parent1
        next_population_copy[parent2] = temp_parent2
        move += 2

    return next_population_copy  # 返回的交叉以后的基因。交叉变异均要保证不会出现公共顶点


def mutation(edges, next_population, mutation_pro):
    n = len(next_population)
    gens_len = len(next_population[0])  # 染色体长度
    for i in range(n):
        cur_pro = random.random()
        if cur_pro > mutation_pro:  # 只有很小的概率变异
            continue
        index1 = random.randint(1, gens_len - 2)  # 变异发生的位置
        variation_gen = construction_gen(edges)  # 这里的变异最好加一个不能有重连边
        next_population[i][index1] = variation_gen
    return next_population


"""
edges为图的原始邻边信息，num_total为染色体的个数，len_gen为染色体的长度，染色体的类型为[(), ()], ()
里为待更改连接的边
k_distribution_orignal为干净图的k_shell分布，字典形式。
cross_pop为交叉概率，mutation_pro为变异概率，edges_len为图中边的个数。
number_genetic为繁殖的次数
"""


def genetic_algorithm_attack(edges, k_distribution_orignal, number_genetic=50, elitesize=1, num_total=16,
                             len_chroms=30,
                             cross_pro=0.4, mutation_pro=0.4):  # edges为networkx生成的edges
    edges = list(edges)
    max_attack = 0  # 攻击精度的阈值。
    for i in tqdm(range(1)):
        population = generate_initial(num_total, len_chroms, edges)  # 初代总群[[],[],[]]
        for step in range(number_genetic):  # 例如准备遗传100次
            fit_scores = sufficiency(population, len_chroms, edges, k_distribution_orignal)  # 越大攻击效果越好
            print("fit_scores:",fit_scores)
            population = selection(population, fit_scores, elitesize)
            population = cross(population, cross_pro, elitesize)
            population = mutation(edges, population, mutation_pro)
            fit_arr = sufficiency(population, len_chroms, edges, k_distribution_orignal)  # 做完工作以后还需要进一步求适应度值
            best_chroms_idx = fit_arr.index(max(fit_arr))  # 寻找最优的染色体
            if fit_arr[best_chroms_idx] > max_attack:
                max_attack = fit_arr[best_chroms_idx]
                best_chroms = population[best_chroms_idx]
                print()
    new_edges = edges[:]  # 列表复制会存在这样的问题，要特别注意。
    for v in best_chroms:
        new_edges = decode(new_edges, v)
    return new_edges  # 最终攻击后的图[(),()]


if __name__ == '__main__':
    # 定义文件名字
    name = "ban300_0.1"
    # 数据保存
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet_hybird = workbook.add_sheet(name)

    # 写入excel
    # 参数对应 行, 列, 值
    # worksheet0.write(1, 0, acc_genetic)

    runTimes = 5  # 定义遗传算法运行次数

    for i in range(3, 4, 1):
        title = 'number_genetic=50, elitesize=1, num_total=' + str(i) + ', len_chroms=21'
        worksheet_hybird.write(0, i - 3, title)
        worksheet_hybird.write(0, i - 2, "ASR")
        worksheet_hybird.write(0, i - 1, "LCR")
        worksheet_hybird.write(0, i - 0, "LPN")

        for j in range(runTimes):  # 设置算法跑几遍
            filename = 'data/' + name + '.txt'
            # pickle格式
            # file = open(filename, "rb")
            # edges = pickle.load(file)
            # G = generate_graph(edges)

            # txt格式
            G = nx.Graph()
            with open(filename) as file:
                for line in file:
                    head, tail = [int(x) for x in line.split(' ')]
                    G.add_edge(head, tail)

            print(G)
            edges = G.edges
            nodes = G.nodes
            edges_len = len(edges)
            # 原始图
            k_distribution_orignal = k_shell(G)
            print("k_distribution_orignal:", k_distribution_orignal)
            k_before_attack = {value: key for key, values in dict(k_distribution_orignal).items() for value in values}
            node_original = color_map(G, k_distribution_orignal)

            # 遗传算法攻击
            new_edges = genetic_algorithm_attack(edges, k_distribution_orignal)
            graph_geneticattack = generate_graph(new_edges)
            k_distribution_geneticattack = k_shell(graph_geneticattack)
            print("k_distribution_attack:", k_distribution_geneticattack)
            k_after_attack = {value: key for key, values in dict(k_distribution_geneticattack).items() for value in
                              values}
            acc_genetic = 1.0 - accuracy(k_distribution_orignal, k_distribution_geneticattack)
            nodecolor_genetic = color_map(graph_geneticattack, k_distribution_geneticattack)
            edgenumber_genetic = attack_edge_number_computation(edges, new_edges)
            node_change_genetic = degree_isdifferent(G, graph_geneticattack)
            print("gentic_Accurate_attack:{},number_attack:{}".format(acc_genetic, edgenumber_genetic))
            print("is node degree change after genetic:{}".format(node_change_genetic))

            # 创建节点列表
            nodes_all = list(set(list(k_before_attack.keys()) + list(k_after_attack.keys())))

            # 计算k-shell值下降的节点数量
            count = 0
            for node in nodes_all:
                if k_after_attack.get(node, 0) != k_before_attack.get(node, 0):
                    count += 1
            # 计算k-shell下降的节点比例
            ASR = count / len(nodes_all)
            print("ASR攻击后k-shell值下降的节点数量占总节点数量的比例为：", ASR)

            # 计算攻击前后图中不同的边
            LCR = edgenumber_genetic / edges_len
            print("攻击前后图中不同的边数为：", edgenumber_genetic)
            print("LCR占总边数的比例为：", LCR)

            # 更改多少个链接才能平均成功攻击一个节点
            LPN = edgenumber_genetic / count
            print("LPN:", LPN)

            worksheet_hybird.write(j + 1, i - 3, acc_genetic)
            worksheet_hybird.write(j + 1, i - 2, ASR)
            worksheet_hybird.write(j + 1, i - 1, LCR)
            worksheet_hybird.write(j + 1, i - 0, LPN)

    # 保存
    # workbook.save(name + '1.xls')

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
