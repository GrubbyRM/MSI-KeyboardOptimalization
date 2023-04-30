import random

populationSize = 100
crossoverRate = 0.8
mutationRate = 0.01
generations = 30

numKeys = 26
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
keys = list(alphabet)

keysFrequency = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
keyDistance = [[]]

def InitializePopulation():
    population = []
    for x in range(populationSize):
        individual = random.sample(range(numKeys), numKeys)
        population.append(individual)
    
    return population

def CalculateTotalEffort(layout):
    totalEffort = 0
    for x in range(numKeys):
        for y in range(numKeys):
            totalEffort += keysFrequency[x] * keysFrequency[y] * keyDistance[layout[x]][layout[y]]
    return totalEffort

def EvaluateFitness(population):
    fitness = []
    for x in range(populationSize):
        fitness.append(CalculateTotalEffort(population[x]))
    return fitness

def Selection(population, fitness):
    contestant1 = population[random.randint(0, populationSize - 1)]
    contestant2 = population[random.randint(0, populationSize - 1)]

    return contestant1 if fitness[population.index(contestant1)] <= fitness[population.index(contestant2)] else contestant2

def OrderCrossover(parent1, parent2):
    crossoverPoint1 = random.randint(1, numKeys - 3)
    crossoverPoint2 = random.randint(crossoverPoint1, numKeys - 2)

    offspring = [-1] * numKeys

    for x in range(crossoverPoint1, crossoverPoint2):
        offspring[x] = parent1[x]

    index = crossoverPoint2
    for i in range(numKeys):
        if parent2[i] not in offspring:
            offspring[index] = parent2[i]
            index = (index + 1) % numKeys

    return offspring
    
def Mutate(individual):
    mutationPoint1 = random.randint(0, numKeys - 1)
    mutationPoint2 = random.randint(0, numKeys - 1)

    # zamień pozycje dwóch losowych klawiszy w indywidualnej permutacji
    individual[mutationPoint1], individual[mutationPoint2] = individual[mutationPoint2], individual[mutationPoint1]

def CalculateKeyDistances():
    QWERTY = [    "1234567890",    "QWERTYUIOP",    "ASDFGHJKL",    "ZXCVBNM"]
    keyCoordsX = [0] * numKeys
    keyCoordsY = [0] * numKeys

    for x in range(len(QWERTY)):
        for y in range(len(QWERTY[x])):
            index = ord(QWERTY[x][y]) - ord('A')

            if index >= 0 and index < numKeys:
                keyCoordsX[index] = y
                keyCoordsY[index] = x

    distances = [[0 for i in range(numKeys)] for j in range(numKeys)]
    for x in range(numKeys):
        for y in range(numKeys):
            distances[x][y] = ((keyCoordsX[x] - keyCoordsX[y]) ** 2 + (keyCoordsY[x] - keyCoordsY[y]) ** 2) ** 0.5
    return distances

def main():
    global keyDistance
    keyDistance = CalculateKeyDistances()
    population = InitializePopulation()

    for generation in range(generations):
        fitness = EvaluateFitness(population)
        newPopulation = []

        for x in range(populationSize):
            parent1 = Selection(population, fitness)
            parent2 = Selection(population, fitness)

            offspring = []
            if random.random() < crossoverRate:
                offspring = OrderCrossover(parent1, parent2)
            else:
                offspring = list(parent1)

            Mutate(offspring)
            newPopulation.append(offspring)
        
        bestIndex = fitness.index(min(fitness))
        bestIndividual = population[bestIndex]

        print(f"Generation: {generation+1}, Best Layout: {''.join([keys[i] for i in bestIndividual])}, Total Effort: {fitness[bestIndex]}")

        population = newPopulation

if __name__ == '__main__':
    main()