#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: jjzhou012
@contact: jjzhou012@163.com
@file: community_deception_via_ga.py
@time: 2020/7/22 9:15
@desc:   GA实现， 针对节点进行重连边扰动，即针对同一节点进行 邻居节点的删边和非邻居节点的增边（删边加边为一次扰动）， 设定扰动次数，生成扰动图，观测模块度的变化
'''

import csv
import copy
import math
import random
import argparse
import datetime
import os
from graph_op import *
from communityDetection_op import *
from metric_op import *
LARGE_Nets = ['wiki-cham', 'twitch-EN', 'facebook', 'github', 'finance', 'dblp']

class Q_Attack():

    def __init__(self, dataset, cdm, popsize, attack_num, Pc, Pm, recombine_rate, output_file):
        '''

        :param dataset:
        :param cdm:
        :param popsize:     个体（染色体DNA）数量, num of dna
        :param attack_num:   攻击（基因gene）数量,  num of gene
        :param Pc:          crossover rate
        :param Pm:          mutation rate
        :param recombine_rate:
        :param graph_file:
        :param output_file:
        '''

        # GA参数
        self.pop_size = popsize
        self.Pc = Pc  # 交叉率
        self.Pm = Pm  # 变异率
        self.recombine_rate = recombine_rate  # pop重组率
        # 路径信息
        # self.graph_file = '../data/{}/{}.gml'.format(bmname, bmname)  # 数据集路径
        if dataset not in LARGE_Nets:
            self.graph_file = 'data/{}/{}.gml'.format(dataset, dataset)
        else:
            self.graph_file = 'data/large-net/{}.gml'.format(dataset)
        self.output_file = output_file  # 输出路径
        # 图信息
        self.bmname = dataset
        self.cdm = cdm
        self.attack_num = attack_num  # 攻击次数

        self.g = nx.read_gml(self.graph_file, label='id')
        self.labels_true = list(nx.get_node_attributes(self.g, 'commID').values())
        self.g = graph_to_undirected_unweighted(self.g)

        self.G = convert_networkx_to_igraph(self.g)


        # 原始图模块度计算
        init_Q = 0
        for i in range(10):
            self.initCommunities = community_method_dict[cdm].__wrapped__(self.labels_true, self.G)
            init_Q += self.G.modularity(self.initCommunities)
        init_Q /= 10
        print("原始图模块度： ", init_Q)

        # 种群初始化, 生成DNA{del_edge、add_edge、Q、fitness}
        self.init_pop()

    def init_pop(self):
        """
        种群初始化
        :return:
        """
        # pop init
        self.pop = {}
        self.nodeList = list(self.g.nodes())
        # 生成个体
        for i in range(self.pop_size):
            # 一个个体为一个DNA
            DNA = {"del_edge": [],  # 删边 element: [(attack_node, del_node),...]
                   "add_edge": [],  # 增边 element: [(attack_node, add_node),...]
                   "Q": float,  # 模块度
                   "fitness": float}  # 适应度
            index = 0  # 对应索引
            while len(DNA["del_edge"]) < self.attack_num:
                try:
                    # 随机选择攻击点
                    attack_node = random.choice(self.nodeList)
                    # 邻居节点 && 非邻居节点
                    neighborList = list(self.g.neighbors(attack_node))
                    nonneighborList = list(nx.non_neighbors(self.g, attack_node))
                    # nonneighborList.remove(attack_node)
                    # 随机邻居节点--->删边

                    del_node = random.choice(neighborList)
                    # 随机非邻节点--->加边
                    add_node = random.choice(nonneighborList)
                except:
                    continue
                # 构成基因 --->  (del_node -- attack_node -- add_node)   ---> del_edge: (attack_node, del_node)
                #                                                       ---> add_edge: (attack_node, add_node)
                # 防止重复的基因片段
                if (attack_node, del_node) not in DNA["del_edge"] and (del_node, attack_node) not in DNA["del_edge"] \
                        and (attack_node, add_node) not in DNA["add_edge"] and (add_node, attack_node) not in DNA["add_edge"]:
                    DNA["del_edge"].append((attack_node, del_node))
                    DNA["add_edge"].append((attack_node, add_node))
            # print(DNA["del_edge"])
            # print(DNA["add_edge"])
            # break
            self.pop[i] = copy.deepcopy(DNA)
        # 计算Q、fitness
        self.cal_fitness()
        # print("初始种群：", self.pop)

    """
    此处加入了个人的修改
    """
    def cal_fitness(self):
        """
        计算DNA 适应度
        :return:  更新DNA，加入Q、fitness
        """
        # print(len(self.pop.items()))
        for ind, DNA in self.pop.items():
            attack_G = copy.deepcopy(self.G)
            # adj = nx.adjacency_matrix(self.g)
            # 根据gene更新adj
            attack_G = rewire_graph(attack_G, add_edges=DNA['add_edge'], del_edges=DNA['del_edge'])


            """
            此处有修改，与原程序不同，加入了求平均的过程
            """
            Q = 0
            for i in range(1):
                # communities = community_method_dict[self.cdm](self.labels_true, attack_G, 'nmi')
                communities = community_method_dict[self.cdm].__wrapped__(self.labels_true, attack_G)
                Q += attack_G.modularity(communities)  # 模块度
                # Q += communities
            Q /= 1
            # if Q < 0:
            #     print(attack_G)
            #     exit(0)

            # 更新DNA
            DNA["Q"] = Q
            # # DNA["fitness"] = 2 * math.exp(-Q)  ### 优化目标
            DNA["fitness"] = math.exp(-Q)
            # DNA["fitness"] = math.sqrt(Q)
            # new_DNA = {"del_edge": copy.deepcopy(DNA["del_edge"]),
            #            "add_edge": copy.deepcopy(DNA["add_edge"]),
            #            "Q": Q,
            #            "fitness": Q}
            # # 更新pop
            # self.pop[ind] = copy.deepcopy(new_DNA)
        # print("重新计算：", self.pop)

    def select(self):
        """
        轮盘赌 选择种群个体
        :param fitness:  种群个体适应度集合
        :param pop:
        :return:
        """
        self.selected_pop = {}
        scoreSum = sum([DNA['fitness'] for DNA in self.pop.values()])
        DNA_index = np.arange(self.pop_size)
        scores = [self.pop[i]['fitness'] / scoreSum for i in DNA_index]
        # print(scores)
        for i in range(self.pop_size):
            idx = np.random.choice(DNA_index, 1, False, scores)[0]
            # print(idx)
            self.selected_pop[i] = copy.deepcopy(self.pop[idx])
        # exit(0)

        # print(self.pop)
        # print(self.selected_pop)
        # exit(0)

    def crossover(self):
        """
        生成交叉后的pop
        :return:  交叉后的pop
        """
        for i in range(self.pop_size // 2):
            crossRateRand = random.random()
            if crossRateRand <= self.Pc:
                self.pop[i * 2], self.pop[i * 2 + 1] = self.dna_crossover()
            else:
                while True:
                    # 选择两个不同的DNA
                    DNA_1_index = random.randint(0, self.pop_size - 1)
                    DNA_2_index = random.randint(0, self.pop_size - 1)
                    if self.selected_pop[DNA_1_index] != self.selected_pop[DNA_2_index]:
                        break

                self.pop[i * 2], self.pop[i * 2 + 1] = copy.deepcopy(self.selected_pop[DNA_1_index]), \
                                                       copy.deepcopy(self.selected_pop[DNA_2_index])
        # print("DNA交叉", self.pop)

    def dna_crossover(self):
        """
        dna的交叉：     单点交叉
        :return:      交叉后的两条DNA
        """
        # 从selected_pop中随机选取两个不同的DNA交叉
        while True:
            # 选择两个不同的DNA
            while True:
                DNA_1_index = random.randint(0, self.pop_size - 1)
                DNA_2_index = random.randint(0, self.pop_size - 1)
                if self.selected_pop[DNA_1_index] != self.selected_pop[DNA_2_index]:
                    break
            # 判断能否交叉
            # 随机一个交叉点
            crossPointRand = random.randint(1, self.attack_num - 1)
            # 复制DNA
            DNA_1 = copy.deepcopy(self.selected_pop[DNA_1_index])
            DNA_2 = copy.deepcopy(self.selected_pop[DNA_2_index])
            # 切片
            DNA_1_del_A = DNA_1["del_edge"][:crossPointRand]
            DNA_1_add_A = DNA_1["add_edge"][:crossPointRand]
            DNA_1_del_B = DNA_1["del_edge"][crossPointRand:]
            DNA_1_add_B = DNA_1["add_edge"][crossPointRand:]
            DNA_2_del_A = DNA_2["del_edge"][:crossPointRand]
            DNA_2_add_A = DNA_2["add_edge"][:crossPointRand]
            DNA_2_del_B = DNA_2["del_edge"][crossPointRand:]
            DNA_2_add_B = DNA_2["add_edge"][crossPointRand:]
            # 基因查重
            sum = 0
            for i in range(self.attack_num - crossPointRand):
                if (DNA_1_del_B[i] not in DNA_2_del_A) and (DNA_1_add_B[i] not in DNA_2_add_A) and \
                        ((DNA_1_del_B[i][1], DNA_1_del_B[i][0]) not in DNA_2_del_A) and \
                        ((DNA_1_add_B[i][1], DNA_1_add_B[i][0]) not in DNA_2_add_A) and \
                        (DNA_2_del_B[i] not in DNA_1_del_A) and (DNA_2_add_B[i] not in DNA_1_add_A) and \
                        ((DNA_2_del_B[i][1], DNA_2_del_B[i][0]) not in DNA_1_del_A) and \
                        ((DNA_2_add_B[i][1], DNA_2_add_B[i][0]) not in DNA_1_add_A):
                    sum += 1
                else:
                    continue
            if sum == (self.attack_num - crossPointRand):
                break
        # 交叉
        new_DNA_1_del = DNA_1_del_A + DNA_2_del_B
        new_DNA_1_add = DNA_1_add_A + DNA_2_add_B
        new_DNA_2_del = DNA_2_del_A + DNA_1_del_B
        new_DNA_2_add = DNA_2_add_A + DNA_1_add_B

        new_DNA_1 = {"del_edge": copy.deepcopy(new_DNA_1_del),
                     "add_edge": copy.deepcopy(new_DNA_1_add),
                     "Q": 0.0,
                     "fitness": 0.0}
        new_DNA_2 = {"del_edge": copy.deepcopy(new_DNA_2_del),
                     "add_edge": copy.deepcopy(new_DNA_2_add),
                     "Q": 0.0,
                     "fitness": 0.0}
        return new_DNA_1, new_DNA_2

    def mutation(self):
        """
        变异： 定义三种变异操作： del_edge变异、add_edge变异、重连边变异
        :return:
        """
        # pop = copy.deepcopy(self.pop)
        for ind, DNA in self.pop.items():
            for j in range(self.attack_num):
                #
                mutationRateRand = random.random()
                if mutationRateRand <= self.Pm:
                    attack_node = DNA["del_edge"][j][0]

                    # 三种变异等概率
                    select_which_mutation = random.randint(0, 2)
                    # 1
                    # del_edge 变异
                    if select_which_mutation == 0:
                        # print("bianyi_0")
                        # 目标节点的所有邻居节点
                        neighborList = list(self.g.neighbors(attack_node))
                        # 已存在于DNA基因中的目标节点的邻居节点
                        gene_neighborList = [DNA["del_edge"][k][1] for k in range(self.attack_num) if
                                             DNA["del_edge"][k][0] == attack_node]
                        # 可选择变异的节点
                        mutation_neighborList = list(set(neighborList) - set(gene_neighborList))
                        # 若无可选择变异的邻居节点, 则无法变异, 移动到下一个基因
                        if len(mutation_neighborList) == 0:
                            continue
                        # 随机选点变异   需要查重
                        while True:
                            del_mutation_node = random.choice(mutation_neighborList)
                            mutation_neighborList.remove(del_mutation_node)
                            # 判断相应的基因片段是否已存在
                            if (del_mutation_node, attack_node) not in DNA["del_edge"]:
                                DNA["del_edge"][j] = (attack_node, del_mutation_node)
                                # print("bianyi_0")
                                # update self.pop
                                # self.pop[ind]["del_edge"][j] = (attack_node, del_mutation_node)
                                break
                            if len(mutation_neighborList) == 0:
                                break
                    # 2
                    # add_edge 变异
                    elif select_which_mutation == 1:
                        # print("bianyi_1")
                        # 目标节点的所有邻居节点
                        neighborList = list(self.g.neighbors(attack_node))
                        # 目标节点的所有非邻居节点
                        nonneighborList = list(nx.non_neighbors(self.g, attack_node))
                        # nonneighborList.remove(attack_node)
                        # 已存在于DNA基因中的目标节点的非邻居节点
                        gene_nonneighborList = [DNA["add_edge"][k][1] for k in range(self.attack_num) if
                                                DNA["add_edge"][k][0] == attack_node]
                        # 可选择变异的节点
                        mutation_nonneighborList = list(set(nonneighborList) - set(gene_nonneighborList))
                        # 若无可选择变异的邻居节点, 则无法变异, 移动到下一个基因
                        if len(mutation_nonneighborList) == 0:
                            continue
                        # 随机选点变异   需要查重
                        while True:
                            add_mutation_node = random.choice(mutation_nonneighborList)
                            mutation_nonneighborList.remove(add_mutation_node)
                            # 判断相应的基因片段是否已存在
                            if (add_mutation_node, attack_node) not in DNA["add_edge"]:
                                DNA["add_edge"][j] = (attack_node, add_mutation_node)
                                # print("bianyi_1")
                                # self.pop[ind]["add_edge"][j] = (attack_node, add_mutation_node)
                                break
                            if len(mutation_nonneighborList) == 0:
                                break
                    # 3
                    # 重连边变异
                    elif select_which_mutation == 2:
                        # print("bianyi_2")
                        while True:
                            # 随机attack_node
                            target_node = random.choice(list(self.g.nodes()))
                            # 目标节点的所有邻居节点
                            neighborList = list(self.g.neighbors(target_node))
                            # 已存在于DNA基因中的目标节点的邻居节点
                            gene_neighborList = [DNA["del_edge"][k][1] for k in range(self.attack_num) if
                                                 DNA["del_edge"][k][0] == target_node]
                            # 可选择变异的邻节点
                            mutation_neighborList = list(set(neighborList) - set(gene_neighborList))
                            # 目标节点的所有非邻居节点
                            nonneighborList = list(nx.non_neighbors(self.g, target_node))
                            # nonneighborList.remove(target_node)
                            # nx.non_neighbors(self.g, target_node)
                            # 已存在于DNA基因中的目标节点的非邻居节点
                            gene_nonneighborList = [DNA["add_edge"][k][1] for k in range(self.attack_num) if
                                                    DNA["add_edge"][k][0] == target_node]
                            # 可选择变异的非邻居节点
                            mutation_nonneighborList = list(set(nonneighborList) - set(gene_nonneighborList))
                            # 若无可选择变异的邻居或非邻居节点, 则无法变异, 移动到下一个基因
                            if len(mutation_neighborList) == 0 or len(mutation_nonneighborList) == 0:
                                continue
                            # 随机选点变异   需要查重
                            # 选择删除点
                            del_mutation_node = random.choice(mutation_neighborList)
                            mutation_neighborList.remove(del_mutation_node)
                            # 选择增加点
                            add_mutation_node = random.choice(mutation_nonneighborList)
                            mutation_nonneighborList.remove(add_mutation_node)
                            if (del_mutation_node, target_node) not in DNA["del_edge"] and (
                                    add_mutation_node, target_node) not in DNA["add_edge"]:
                                DNA["del_edge"][j] = (target_node, del_mutation_node)
                                DNA["add_edge"][j] = (target_node, add_mutation_node)
                                # print("bianyi_2")
                                # self.pop[ind]["del_edge"][j] = (target_node, del_mutation_node)
                                # self.pop[ind]["del_edge"][j] = (target_node, add_mutation_node)
                                break
                            if len(mutation_neighborList) == 0 or len(mutation_nonneighborList) == 0:
                                break
        # print("基因突变：", self.pop)

    def pop_recombine(self):
        # 父代排序
        last_fitness_list = sorted(self.last_pop.items(), key=lambda item: item[1]["fitness"], reverse=True)  # last_pop: 按fitness从大到小排序
        # 子代排序
        now_fitness_list = sorted(self.pop.items(), key=lambda item: item[1]["fitness"], reverse=False)  # pop: 按fitness从小到大排序
        # print("last_pop_best_Q: ", last_fitness_list[0][1]["Q"])
        # print("now_pop_best_Q: ", now_fitness_list[-1][1]["Q"])
        # 重组长度
        recombine_size = int(self.pop_size * self.recombine_rate)
        # 重组
        recombine_pop = copy.deepcopy(last_fitness_list[:recombine_size]) + copy.deepcopy(now_fitness_list[recombine_size:])

        # re_pop_list = sorted(dict(recombine_pop).items(), key=lambda item: item[1]["fitness"], reverse=True)
        # print(re_pop_list)

        self.pop = {}
        # 因为重组后索引可能重复，不能直接转列表，需要重新赋予索引
        for i in range(len(recombine_pop)):
            self.pop[i] = copy.deepcopy(recombine_pop[i][1])

        # self.pop = dict(copy.deepcopy(recombine_pop))
        # print("种群重组：", self.pop)

    def output_info(self, now_iter_num, iter_num):
        now_fitness_list = sorted(self.pop.items(), key=lambda item: item[1]["fitness"], reverse=True)
        # print(now_fitness_list)
        best_attack = copy.deepcopy(now_fitness_list[0])
        # print(best_attack)
        best_QValue = best_attack[1]["Q"]
        best_fitness = best_attack[1]["fitness"]
        best_del = best_attack[1]["del_edge"]
        best_add = best_attack[1]["add_edge"]

        print("best_fitness: ", best_fitness)
        print("best_QValue: ", best_QValue)
        average_QValue = sum([item[1]["Q"] for item in now_fitness_list]) / self.pop_size
        average_fitness = sum([item[1]["fitness"] for item in now_fitness_list]) / self.pop_size
        print("average_fitness: ", average_fitness)
        print("average_QValue: ", average_QValue)

        self.output_list = [now_iter_num, best_fitness, average_fitness, best_QValue, average_QValue, best_del, best_add]

        # save update graph
        if now_iter_num == iter_num:
            new_g = copy.deepcopy(self.g)
            new_g.add_edges_from(best_add)
            new_g.remove_edges_from(best_del)
            # atts = nx.get_node_attributes(new_g, 'commID')
            # print(atts)
            # atts = {k: {'commID': str(v)} for k, v in atts.items()}
            # nx.set_node_attributes(new_g, atts)
            # nx.write_graphml(new_g, self.output_file[:-7] + '{}.gml'.format(self.output_file.split('/')[-2]))

    def run(self, iter_num):
        """
        进化迭代， 1.轮盘赌选择 ---> 2.交叉  ---> 3.变异  ---> 4.种群重组
        :param iter_num:
        :return:
        """
        with open(self.output_file, "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["iter_num", "best_fitness", "average_fitness", "best_QValue", "average_QValue", "del_edge", "add_edge"])

            for i in range(iter_num):
                print("iter num:" + str(i + 1) + ".................................")
                # 保存上一代种群信息
                self.last_pop = copy.deepcopy(self.pop)
                # 轮盘赌选择DNA组成pop
                self.select()  # return self.selected_pop

                if self.attack_num > 1:
                    # 交叉
                    self.crossover()  # 更新 self.pop  中的 del_edge、add_edge
                # 变异
                self.mutation()  # 更新 self.pop  中的 del_edge、add_edge
                # 计算fitness
                self.cal_fitness()  # 更新 self.pop 中的 Q、fitness
                # 种群重组
                self.pop_recombine()  # 更新 self.pop
                # 打印保存每代最优
                self.output_info(now_iter_num=i + 1, iter_num=iter_num)  # return self.output_list

                writer.writerow(self.output_list)

        csv_file.close()


def get_para():
    parser = argparse.ArgumentParser(description='manual to this script')
    # file para
    # parser.add_argument('--dataset', help="name of benchmark dataset", required=False, type=str, default='karate')
    parser.add_argument('--dataset', help="name of benchmark dataset", required=False, type=str, default='football')
    parser.add_argument('--model', help="community detection method", required=True, type=str, default=None)
    parser.add_argument('--attack_num', help="upper threshold of attack budget", required=True, type=int, default=None)
    parser.add_argument('--iterNum', help="number of attack iterator", required=True, type=int, default=100)
    parser.add_argument('--attack_method', help="method of attack cdm", required=False, type=str, default='Q-Attack')
    parser.add_argument('--primary_task', help="", required=False, type=str, default='network_clustering')
    args = parser.parse_args()
    return args

def main(i):
    args = get_para()
    bmname = args.dataset
    cdm = args.model
    attack_num = args.attack_num
    popsize = 100
    Pc = 0.8
    Pm = 0.1
    recombine_rate = 0.1
    iterNum = args.iterNum
    log_dir = 'log/attack/ga-attack/adv1_ga_{}_{}_Cost-{}_iter-{}-{}/'.format(bmname, cdm, attack_num, iterNum, datetime.datetime.now().strftime("%Y-%m-%d"))
    if not os.path.exists(log_dir): os.makedirs(log_dir)
    output_file = log_dir + 'log{}.csv'.format(i)

    save_graph = output_file[:-7] + '{}.gml'.format(output_file.split('/')[-2])

    rega = Q_Attack(dataset=bmname,
                    cdm=cdm,
                    popsize=popsize,
                    Pc=Pc, Pm=Pm,
                    recombine_rate=recombine_rate,
                    attack_num=attack_num,
                    output_file=output_file).run(iter_num=iterNum)

    if bmname not in LARGE_Nets:
        file = 'data/{}/{}.gml'.format(bmname, bmname)
    else:
        file = 'data/large-net/{}.gml'.format(bmname)
    g = nx.read_gml(file, label='id')
    labels_true = list(nx.get_node_attributes(g, 'commID').values())
    G = IG.Read_GML(file)

    """
    此处有修改，计算十次指标，取平均值
    """
    orig_qqq = 0
    orig_nmi = 0
    orig_ari = 0
    orig_ff1 = 0
    for i in range(1):
        community = community_method_dict[cdm].__wrapped__(labels_true, input=G)
        qqq, nmi, ari, ff1 = evaluate_results(G, community, labels_true)
        orig_qqq += qqq
        orig_nmi += nmi
        orig_ari += ari
        orig_ff1 += ff1
    orig_qqq /= 1
    orig_nmi /= 1
    orig_ari /= 1
    orig_ff1 /= 1
    # community = community_method_dict[cdm].__wrapped__(labels_true, input=G)
    # orig_qqq, orig_nmi, orig_ari, orig_ff1 = evaluate_results(G, community, labels_true)
    print('=====================================')
    print('Metrics of original network:.......  ')
    print('orig qqq: {:.3}'.format(orig_qqq))
    print('orig nmi: {:.3}'.format(orig_nmi))
    print('orig_ari: {:.3}'.format(orig_ari))
    print('orig_f1 : {:.3}'.format(orig_ff1))
    print('=====================================\n')

    # try:
    #     attack_g.graph.popitem()
    #     attack_g.graph.popitem()
    #     nx.write_gml(attack_g, save_graph)
    # except:
    #     pass
    #
    # attack_g = nx.read_gml(save_graph, label='id')
    # attack_G = IG.Read_GML(save_graph)
    #
    #
    # """
    # 此处有修改，计算十次指标，取平均值
    # """
    # qqq = 0
    # nmi = 0
    # ari = 0
    # ff1 = 0
    # for i in range(10):
    #     att_community = community_method_dict[cdm].__wrapped__(labels_true, attack_G)
    #     qq, nm, ar, ff = evaluate_results(attack_g, att_community, labels_true)
    #     qqq += qq
    #     nmi += nm
    #     ari += ar
    #     ff1 += ff
    # qqq /= 10
    # nmi /= 10
    # ari /= 10
    # ff1 /= 10
    # # att_community =  community_method_dict[cdm].__wrapped__(labels_true, attack_G)
    # # qqq, nmi, ari, ff1 = evaluate_results(attack_g, att_community, labels_true)
    #
    # print('=====================================')
    # print('Metrics of adversarial network:.......  ')
    # print('attack qqq: {:.3}'.format(qqq))
    # print('attack nmi: {:.3}'.format(nmi))
    # print('attack ari: {:.3}'.format(ari))
    # print('attack f1 : {:.3}'.format(ff1))
    # print('=====================================\n')

if __name__ == '__main__':
    for i in range(1):
        main(i)
