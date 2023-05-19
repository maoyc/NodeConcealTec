import random
import numpy as np
import matplotlib.pyplot as plt

# 适应度函数：最小化函数f(x) = x^2
def fitness_function(x):
    return x ** 2

# 初始化种群
def init_population(size, chromosome_length):
    return np.random.uniform(-10, 10, (size, chromosome_length))

# 选择算子：轮盘赌选择
def selection(population):
    total_fitness = sum(fitness_function(x) for x in population)
    r = random.uniform(0, total_fitness)
    partial_sum = 0
    for x in population:
        partial_sum += fitness_function(x)
        if np.any(partial_sum >= r):
            return x

# 交叉算子：随机值交叉
def crossover(parent1, parent2):
    child1 = (parent1 + parent2) / 2 + np.random.uniform(-1, 1, parent1.shape)
    child2 = (parent1 + parent2) / 2 - np.random.uniform(-1, 1, parent1.shape)
    return child1, child2

# 变异算子：随机变异
def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] += np.random.uniform(-1, 1)
    return individual

# 遗传算法主函数
def genetic_algorithm(population_size, num_generations, chromosome_length, mutation_rate):
    population = init_population(population_size, chromosome_length)
    fitness_history = []
    for i in range(num_generations):
        new_population = []
        for j in range(population_size // 2):
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutation(child1, mutation_rate))
            new_population.append(mutation(child2, mutation_rate))
        population = np.array(new_population)
        best_individual = min(population, key=lambda x: fitness_function(x)[0])
        fitness_history.append(max(fitness_function(best_individual))/100)
        print("Generation {}, Best fitness: {}".format(i, fitness_history[-1]))

    print(num_generations,fitness_history)
    # 绘制适应度历史记录曲线
    plt.plot(range(num_generations), fitness_history)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness History')
    plt.show()
    return fitness_history

if __name__ == '__main__':

    population_size = 50
    num_generations = 1000
    chromosome_length = 20
    mutation_rate = 0.1

    fitness_history = genetic_algorithm(population_size, num_generations, chromosome_length, mutation_rate)

