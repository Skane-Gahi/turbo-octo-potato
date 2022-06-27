import numpy as np
import random


#   PARAMETERS ###############################################
V = 8
INDIVIDUAL = 8

MAX_ITER = 20
NB_COLIS = 50

#   TRAFFIC ##################################################
MATIN = [1.7, 2.2]
MIDI = [0.8, 1.2]
APRES_MIDI = [1.25, 1.7]
NUIT = [0.6, 1]

# CALCUL DU NOMBRE DE CAMIONS ################################
VOLUME_COLIS = [1, 3, 5, 8]
CAPACITE_CAMION = 20

def TableauColis(nb_colis):
  tableau = {}
  tableau[0] = random.randint(0, int(nb_colis/2))
  tableau[1] = random.randint(0, int(nb_colis-tableau[0]))
  tableau[2] = random.randint(0, int(nb_colis-(tableau[0]+tableau[1])))
  tableau[3] = nb_colis-(tableau[0]+tableau[1]+tableau[2])
  return tableau

def NombreCamion(tableau_colis):
  nb_camion = 1
  capacite = 0
  listeCapacite = []

  for i in range(3, -1, -1):
    for colis in range(tableau_colis[i]):
      if capacite + VOLUME_COLIS[i] < CAPACITE_CAMION:
        capacite += VOLUME_COLIS[i]
      else:
        nb_camion += 1
        listeCapacite.append(capacite)
        capacite = 0 + VOLUME_COLIS[i]

  listeCapacite.append(capacite)
  print(nb_camion)
  print(listeCapacite)
  return nb_camion

tableau_colis = TableauColis(NB_COLIS)
print(tableau_colis)
k = NombreCamion(tableau_colis)

def matrice_poids(v, periode):
  arr = np.empty((v, v), dtype='int32')
  for i in range(0,v):
    for j in range(0,v):
      if j != i:
        arr[i][j] = round(random.randint(1, 100) * random.uniform(periode[0], periode[1]))
      else:
        arr[i][j] = 0
  
  return arr

MATRICE_POIDS = matrice_poids(V, MIDI)

# Generation #################################################
def Population(nb_node, nb_individual):
    pop = []
    for _ in range(0, nb_individual):
        # randomList = [0]
        randomList = random.sample(range(1, nb_node), nb_node-1)
        # randomList.extend([0])
        truckIdx = [random.randrange(1, V-1) for _ in range(k-1)]
        while truckIdx in pop:
            truckIdx = [(random.randrange(1, V-1) for _ in range(k-1))]
        pop.append([randomList, truckIdx])
    
    return pop

#   Only for new gen ########################################
def individu(nb_node):
    
    # randomList = [0]
    randomList = random.sample(range(1, nb_node), nb_node-1)
    # randomList.extend([0])
    truckIdx = [random.randrange(1, V-1) for _ in range(k-1)]

    return [randomList, truckIdx]

#   Fitness #################################################
def get_sum(element):
    totalSum = 0
    #   Ajout du depot à l'interieur (fin du 1 camion, debut du 2ème, ...)
    for index in element[1]:
        for i in range(0,2):
            element[0].insert(index, 0)
    #   Ajout du depot au debut et à la fin
    element[0].append(0)
    element[0].insert(0, 0)

    for i in range(len(element[0])-1):
        if i < (len(element[0])-1):
            totalSum += MATRICE_POIDS[element[0][i]][element[0][i+1]]
    
    #  Enleve le depot
    element[0].pop(0)
    element[0].pop(-1)
    #   Enlève le depot à l'interieur (fin du 1 camion, debut du 2ème, ...)
    for index in element[1]:
        for i in range(0,2):
            element[0].pop(index)
    return totalSum

def Fitness(pop):
    pop.sort(key=get_sum, reverse=False)
    return pop


#   Crossover ###############################################
def sub_crossover(i1, i2):
    rdmStartIdx = random.randint(0, len(i1[0])-2)
    rdmLength = random.randint(2, (len(i1[0]))-rdmStartIdx)
    idxList = list(range(rdmStartIdx, rdmStartIdx+rdmLength))
    child = [0] * (len(i1[0]))
   
    for i in idxList:
        child[i] = i1[0][i]
    for i in range(0, len(i2[0])):
        if child[i] == 0:
            if i2[0][i] not in child:
                child[i] = i2[0][i]
            else:
                for j in idxList:     
                    if i2[0][j] not in child:
                        child[i] = i2[0][j]
          
    rdmTruckIdx = random.randint(0, 1)
    truckIdx = i1[1] if rdmTruckIdx == 0 else i2[1]
    return [child, truckIdx]

def Crossover(pop):
    n_pop = []
    for i in range(len(pop)):
       
        if i == 0:
            n_pop.append(pop[i])
        else:
            n_pop.append(sub_crossover(pop[0], pop[i]))
       
    return n_pop


#   Mutation ################################################
def Mutation(pop):
    n = 0
    for i in pop:
        if n > 0:
            rdmIdx1 = random.randint(0, len(i[0])-1)
            rdmIdx2 = random.randint(0, len(i[0])-1)
            tmp = i[0][rdmIdx1]
            i[0][rdmIdx1] = i[0][rdmIdx2]
            i[0][rdmIdx2] = tmp
        n += 1

    return pop

#   NEW_POPULATION ############################################
def NewPopulation(pop):
    n_pop = []
    for i in range(len(pop)):
        if i < (len(pop)/2):
            n_pop.append(pop[i])
        else:
            n_pop.append(individu(V))

    return n_pop


# Loop ########################################################
def Loop(pop):
    if pop == []:
        pop = Population(V, INDIVIDUAL)
    else:
        pop = Fitness(pop)
        pop = Crossover(pop)
        pop = Mutation(pop)
        pop = NewPopulation(pop)
        
    return pop

# print(MATRICE_POIDS)
# pop = Population(V, INDIVIDUAL)
# print('Default : ', pop, '\n')
# pop = Fitness(pop)
# print('Fitness : ', pop, '\n')
# pop = Crossover(pop)
# print('Crossover : ', pop, '\n')
# pop = Mutation(pop)
# print('Mutation : ', pop, '\n')
# pop = NewPopulation(pop)
# print('New Gen : ', pop, '\n')