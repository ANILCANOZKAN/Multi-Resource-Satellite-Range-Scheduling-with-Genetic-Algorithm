import random
import matplotlib.pyplot as plt

class window:
    #görünürlük pencerelerinin sınıfı
    def __init__(self):
        self.start = random.randint(0, 714)
        self.end = random.randint(self.start, self.start+5)

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

def groundStationConflicts(tasks, task, chromosome, servedTasks):
    isConflict = False
    conflictIndex = -1
    for i in range(100):
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
    servedTasks = [1 for i in range(100)]
    for i in range(100):
        if(servedTasks[i] == 1):
            isConflict = groundStationConflicts(tasks, tasks[chromosome[i]], chromosome, servedTasks)
            if(isConflict[0]):
                if(tasks[chromosome[i]].priorty > tasks[chromosome[isConflict[1]]].priorty):
                    servedTasks[i] = 0
                else:
                    servedTasks[isConflict[1]] = 0
    return chromosome,servedTasks
def calculateFitness(editedChromosome, editedServeState, tasks):
    fitness = 0
    for i in range(len(editedChromosome)):
        taskId = editedChromosome[i]
        taskServeState = editedServeState[i]
        fitness = fitness+(tasks[taskId].priorty*taskServeState)
    return fitness
def geneticAlgorithm(population,tasks):
    iterations = 0
    bestFitness = -1
    bestChromosome = []
    bestChromosomeServedTasks = []
    while(iterations <1):
        editedGen = []
        editedServeState = []
        fitness = []
        for i in range(100):
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
        iterations += 1
    return bestFitness, bestChromosome, bestChromosomeServedTasks

shiftTime = 3
tasks = [task(id=i) for i in range(200)]
maxFitness = findMaxFitness(tasks)
firstPopulation = [random.sample(range(0, 200), 100) for i in range(100)]
print("Maksimum fitness değeri: ", maxFitness)
result = geneticAlgorithm(firstPopulation,tasks)
print("En iyi fitness: ", result[0])
print("Sıralanmış görevler: ", result[1])
print("Görevlerin hizmet durumu: ", result[2])

for i in range(100):
    x = [tasks[result[1][i]].visibilityWindow.start,tasks[result[1][i]].visibilityWindow.end]
# corresponding y axis values
    y = [tasks[result[1][i]].satId, tasks[result[1][i]].satId]
# plotting the points
    plt.plot(x, y)

plt.yticks(list(range(0,30)))

# naming the x axis
plt.xlabel('Zaman(dk)')
# naming the y axis
plt.ylabel('Uydu')



# giving a title to my graph
plt.title('Hizmet Verilen Görevler')


# function to show the plot
plt.show()