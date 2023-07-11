import random
import numpy as np
maze = [['P', 'B', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['P', 'B', 'P', 'B', 'P', 'B', 'P', 'B'],
        ['P', 'P', 'P', 'B', 'P', 'P', 'B', 'P'],
        ['B', 'B', 'B', 'B', 'P', 'P', 'P', 'B'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'B']]



def calFitness(queueFit,queueIndex):
    for i in range(len(population)):
        fitness=0
        for j in range(len(population[i])):
            if population[i][j]!=target[j]:
                fitness+=1
        queueFit.append(fitness)
        queueIndex.append(i)
    return queueFit,queueIndex

def mutateChild(individual):
    newGene=random.choice(genes)
    while newGene in individual:
        newGene=random.choice(genes)
    index=random.randint(1,len(individual)-1)
    return individual[:index]+[newGene]+individual[index+1:]

def sortFitness(queueFit,queueIndex):
    tempFit=np.array(queueFit)
    tempIndex=np.array(queueIndex)
    sort=np.argsort(tempFit)
    queueFit=list(tempFit[sort])
    queueIndex=list(tempIndex[sort])
    return queueFit,queueIndex

def crossover(queueFit,queueIndex):
    index=random.randint(1,len(target)-2)

    firstChormosome=population[queueIndex[0]]
    secondChormosome=population[queueIndex[1]]
    childFirst=firstChormosome[:index]+secondChormosome[index:]
    childSecond=secondChormosome[:index]+firstChormosome[index:]
    
    if random.random()>0.1:
        childFirst=mutateChild(childFirst)
    if random.random()>0.1:
        childSecond=mutateChild(childSecond)
    
    population.append(childFirst)
    population.append(childSecond)

    queueFit,queueIndex=calFitness(queueFit,queueIndex)
    queueFit,queueIndex=sortFitness(queueFit,queueIndex)
    return queueFit,queueIndex

# [fitness, chromo]

def runGenetic():
    queueFit=[]
    queueIndex=[]
    queueFit,queueIndex=calFitness(queueFit,queueIndex)
    queueFit,queueIndex=sortFitness(queueFit,queueIndex)
    count=0
    while target!=population[queueIndex[0]] and count<=1000:
        queueFit,queueIndex=crossover(queueFit,queueIndex)
        queueFit=queueFit[:2]
        queueIndex=queueIndex[:2]
        count+=1
        print(population[queueIndex[0]],len(target)-queueFit[0])
    if count==1001:
        print('1000 Generations Reached!')
        print(population[queueIndex[0]],len(target)-queueFit[0])
    else:
        print('Target Path found at',count,'iterations.')



target=[(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)]
genes=[(0,0),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(1,0),(1,2),(1,4),(1,6),(2,0),(2,1),(2,2),(2,4),(2,5),(2,7),(3,4),(3,5),(3,6),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)]
size=100
population=[[] for i in range(size)]
i=0
while i<size:
    population[i].append((0,0))
    j=0
    while j<len(target)-2:
        index=random.randint(0,len(genes)-1)
        if genes[index]==(0,0) or genes[index]==(0,7):
            continue
        if genes[index] in population[i]:
            continue
        population[i].append(genes[index])
        j+=1
    population[i].append((0,7))
    i+=1

c=0
# for rows in population:
#     if len(rows)==len(target):
#         c+=1
# print(c)
# print(random.random())
runGenetic()



















