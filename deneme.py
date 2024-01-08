import random
import matplotlib.pyplot as plt
import operator


class window:
    #görünürlük pencerelerinin sınıfı
    def __init__(self):
        self.start = random.randint(0, 1434)
        self.end = random.randint(self.start, 1440)

class task:
    #görevlerin sınıfı
    def __init__(self, id):
        self.id = id
        self.priorty = random.randint(0, 9)
        self.satId = random.randint(0, 30)
        self.gndStId = random.randint(0, 9)
        self.visibilityWindow = window()

def findMaxFitness(tasks):
    sum = 0
    for i in range(len(tasks)):
        sum = tasks[i].priorty+sum
    return sum

def satelliteConflicts(tasks,task, chromosome, servedTasks):
    isConflict = False
    conflictIndex = -1
    chromosomeSize = len(chromosome)
    for i in range(chromosomeSize):
        if (tasks[chromosome[i]].satId == task.satId):
            if (tasks[chromosome[i]].id == task.id):
                continue
            if (servedTasks[i] == 0):
                continue
            if (task.visibilityWindow.end > tasks[chromosome[i]].visibilityWindow.start):
                if (tasks[chromosome[i]].visibilityWindow.end > task.visibilityWindow.start):
                    isConflict = True
                    conflictIndex = i
                    break
    return isConflict, conflictIndex
def groundStationConflicts(tasks, task, chromosome, servedTasks):
    isConflict = False
    conflictIndex = -1
    chromosomeSize = len(chromosome)
    for i in range(chromosomeSize):
        if (tasks[chromosome[i]].gndStId == task.gndStId):
            if (tasks[chromosome[i]].id == task.id):
                continue
            if (servedTasks[i] == 0):
                continue
            if (task.visibilityWindow.end + shiftTime > tasks[chromosome[i]].visibilityWindow.start):
                if (tasks[chromosome[i]].visibilityWindow.end + shiftTime > task.visibilityWindow.start):
                    isConflict = True
                    conflictIndex = i
                    break
    return isConflict, conflictIndex
def checkConflicts(chromosome, tasks):
    chromosomeSize = len(chromosome)
    servedTasks = [1 for i in range(chromosomeSize)]
    for i in range(chromosomeSize):
        if(servedTasks[i] == 1):
            isConflict, conflictIndex = satelliteConflicts(tasks, tasks[chromosome[i]], chromosome, servedTasks)
            if (isConflict):
                if (tasks[chromosome[i]].priorty > tasks[chromosome[conflictIndex]].priorty):
                    servedTasks[conflictIndex] = 0
                elif (tasks[chromosome[i]].priorty < tasks[chromosome[conflictIndex]].priorty):
                    servedTasks[i] = 0
                else:
                    task1Duration = tasks[chromosome[i]].visibilityWindow.end - tasks[
                        chromosome[i]].visibilityWindow.start
                    task2Duration = tasks[chromosome[conflictIndex]].visibilityWindow.end - tasks[
                        chromosome[conflictIndex]].visibilityWindow.start
                    if (task1Duration > task2Duration):
                        servedTasks[i] = 0
                    else:
                        servedTasks[conflictIndex] = 0
    for i in range(chromosomeSize):
        if(servedTasks[i] == 1):
            isConflict, conflictIndex = groundStationConflicts(tasks, tasks[chromosome[i]], chromosome, servedTasks)
            if(isConflict):
                if(tasks[chromosome[i]].priorty > tasks[chromosome[conflictIndex]].priorty):
                    servedTasks[conflictIndex] = 0
                elif(tasks[chromosome[i]].priorty < tasks[chromosome[conflictIndex]].priorty):
                    servedTasks[i] = 0
                else:
                    task1Duration = tasks[chromosome[i]].visibilityWindow.end - tasks[chromosome[i]].visibilityWindow.start
                    task2Duration = tasks[chromosome[conflictIndex]].visibilityWindow.end - tasks[chromosome[conflictIndex]].visibilityWindow.start
                    if(task1Duration > task2Duration):
                        servedTasks[i] = 0
                    else:
                        servedTasks[conflictIndex] = 0


    return chromosome,servedTasks
def calculateFitness(editedChromosome, editedServeState, tasks):
    fitness = 0
    for i in range(len(editedChromosome)):
        taskId = editedChromosome[i]
        taskServeState = editedServeState[i]
        fitness = fitness+(tasks[taskId].priorty*taskServeState)
    return fitness


def unique_roulette_selection(population, fitness_scores, selected_set):
    total_fitness = sum(fitness_scores)
    normalized_probabilities = [score / total_fitness for score in fitness_scores]

    selected_index = roulette_wheel_spin(unique_normalized_probabilities(normalized_probabilities, selected_set))
    selected_individual = population[selected_index]

    # Mark the selected individual as chosen
    selected_set.add(selected_index)

    return selected_individual


def roulette_wheel_spin(probabilities):
    spin = random.uniform(0, 1)
    cumulative_probability = 0

    for i, probability in enumerate(probabilities):
        cumulative_probability += probability
        if spin <= cumulative_probability:
            return i


def unique_normalized_probabilities(normalized_probabilities, selected_set):
    # Adjust probabilities to avoid selecting individuals already chosen
    adjusted_probabilities = normalized_probabilities.copy()

    for index in selected_set:
        adjusted_probabilities[index] = 0

    # Normalize adjusted probabilities
    total_adjusted_probability = sum(adjusted_probabilities)
    if total_adjusted_probability > 0:
        adjusted_probabilities = [prob / total_adjusted_probability for prob in adjusted_probabilities]

    return adjusted_probabilities
def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def unique_crossover(parent1, parent2):
    child1, child2 = one_point_crossover(parent1, parent2)

    # Make genes unique in children
    child1 = make_unique(child1, parent1)
    child2 = make_unique(child2, parent2)

    return child1, child2


def make_unique(child, parent):
    for i in range(len(child)):
        if child[i] in child[:i] + child[i + 1:]:
            unused_genes = [gene for gene in parent if gene not in child]
            child[i] = random.choice(unused_genes)
    return child
def geneticAlgorithm(population,tasks, maxIteration):
    populationSize = len(population)
    iterations = 0
    bestFitness = -1
    bestChromosome = []
    bestChromosomeServedTasks = []
    while(iterations < maxIteration):
        editedGen = []
        editedServeState = []
        fitness = []
        newPopulation = []
        selectedSet = set()
        for i in range(populationSize):
            conflictsResult = checkConflicts(population[i], tasks)
            editedGen = editedGen +[conflictsResult[0]]
            editedServeState = editedServeState + [conflictsResult[1]]
            fitness = fitness + [calculateFitness(editedGen[i], editedServeState[i], tasks)]
            if(fitness[i] >= bestFitness):
                bestFitness = fitness[i]
                bestChromosome = editedGen[i]
                bestChromosomeServedTasks = editedServeState[i]
                if (bestFitness == maxFitness):
                    return bestFitness, bestChromosome, bestChromosomeServedTasks
        for _ in range(populationSize // 2):
            parent1 = unique_roulette_selection(population, fitness,selectedSet)
            parent2 = unique_roulette_selection(population, fitness,selectedSet)
            child1, child2 = unique_crossover(parent1, parent2)
            newPopulation.extend([child1, child2])

        population = newPopulation
        iterations += 1
    return bestFitness, bestChromosome, bestChromosomeServedTasks

shiftTime = 5
maxTask = 150
maxPopulation = 100
maxGene = 100
iterations = 5000
tasks = [task(id=i) for i in range(maxTask)]
maxFitness = findMaxFitness(tasks)
firstPopulation = [random.sample(range(0, maxTask), maxGene) for i in range(maxPopulation)]
print("Maksimum fitness değeri: ", maxFitness)
result = geneticAlgorithm(firstPopulation,tasks, iterations)
print("En iyi fitness: ", result[0])
print("Hizmet verilen görev sayısı: ", operator.countOf(result[2],1))
print("Sıralanmış görevler: ", result[1])
print("Görevlerin hizmet durumu: ", result[2])

for i in range(maxGene):
    if(result[2][i] == 1):
        x = [tasks[result[1][i]].visibilityWindow.start, tasks[result[1][i]].visibilityWindow.end]
        # corresponding y axis values
        y = [tasks[result[1][i]].satId, tasks[result[1][i]].satId]
        # plotting the points
        plt.plot(x, y)

plt.yticks(list(range(0,31)))
# naming the x axis
plt.xlabel('Zaman(dk)')
# naming the y axis
plt.ylabel('Uydu')

# giving a title to my graph
plt.title('Hizmet Verilen Görevler')

# function to show the plot
plt.show()

for i in range(maxGene):
    if (result[2][i] == 1):
        x = [tasks[result[1][i]].visibilityWindow.start,tasks[result[1][i]].visibilityWindow.end]
# corresponding y axis values
        y = [tasks[result[1][i]].gndStId, tasks[result[1][i]].gndStId]
# plotting the points
        plt.plot(x, y)

plt.yticks(list(range(0,10)))
# naming the x axis
plt.xlabel('Zaman(dk)')
# naming the y axis
plt.ylabel('Yer İstasyonları')

# giving a title to my graph
plt.title('Hizmet Verilen Görevler')

# function to show the plot
plt.show()