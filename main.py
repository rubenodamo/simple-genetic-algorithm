#Importing the necessary modules
import numpy as np
import random as rd
from random import randint

#Formatting the output
reset = "\033[0;0m"
bold = "\033[1m"
italics = '\x1B[3m'
underline = '\033[4m'
blue = '\033[94m'
hblack = '\033[40m'
red = '\033[91m'
green = '\033[32m'

#Declaring and initialising variables
item_number = np.arange(1, 11)
item_numberArray = []
item_nameArray = []
weightArray = []
valueArray = []

#Title
print("{0}{1}{2}Luggage Checker{3}\n{4}{5}By Ruben{3}\n".format(
    bold, underline, blue, reset, italics, green))

#Collecting user input
for i in range(10):
    item_numberArray.append(item_number[i])
    item_name = input("{1}Enter item {0}{2}: ".format((i + 1), bold, reset))
    item_nameArray.append(item_name)
    w = int(
        input("{1}Enter the weight of {0} (kg){2}: ".format(
            item_name, bold, reset)))
    while w > 23 or w < 0:
        print("{0}Invalid Input. Weight of {1} is out of range.{2}".format(
            red, item_name, reset))
        w = int(
            input("{1}Enter the weight of {0}{2}: ".format(
                item_name, bold, reset)))
    weightArray.append(w)
    v = int(
        input("{1}Enter the value of {0} (VALUE: 1-100){2}: ".format(
            item_name, bold, reset)))
    while v > 100 or w < 1:
        print("{0}Invalid Input. Value of {1} is out of range.{2}".format(
            red, item_name, reset))
        v = int(
            input("{1}Enter the value of {0} (VALUE: 1-100){2}: ".format(
                item_name, bold, reset)))
    valueArray.append(v)
    print('\n')

suitcase_threshold = 23  #Maximum weight that the suitcase can hold
weight = np.array(weightArray)
value = np.array(valueArray)

#Outputting information in tabular format
print('\n{0}{1}Your items:{2}\n'.format(bold, blue, reset))
print('%-10s%-28s%-10s%-10s' %
      ("\033[40;32mITEM NO.", "ITEM NAME", "WEIGHT", "VALUE\033[0;0m"))
for i in range((item_number.shape[0])):
    print('%-10d%-25s%-10d%-10d' % (item_numberArray[i], item_nameArray[i],
                                    weightArray[i], valueArray[i]))

#Declaring initial population
solutions_per_pop = 8  #has to be less than total num of items (10)
pop_size = (solutions_per_pop, item_number.shape[0])
print("{1}Population size = {0}{2}".format(pop_size, bold, reset))
initial_population = np.random.randint(2, size=pop_size)
initial_population = initial_population.astype(int)
num_generations = 50
print("{1}Initial population: \n{0}{2}".format(initial_population, bold,
                                               reset))


#Function which calculates the fitness of each individual/gene
def cal_fitness(weight, value, population, threshold):
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        S1 = np.sum(population[i] * value)
        S2 = np.sum(population[i] * weight)
        #Compares the sum of weight x item to the threshold (23kg)
        if S2 <= threshold:
            fitness[i] = S1
        else:
            fitness[i] = 0
    return fitness.astype(int)


#Function which selects fittest individuals which will undergo crossover
def selection(fitness, num_parents, population):
    fitness = list(fitness)
    parents = np.empty((num_parents, population.shape[1]))
    #Uses roulette wheel selection
    for i in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        parents[i, :] = population[max_fitness_idx[0][0], :]
        fitness[max_fitness_idx[0][0]] = -999999
    return parents


#Function in which crossover occurs between the two parents
def crossover(parents, num_offsprings):
    offsprings = np.empty((num_offsprings, parents.shape[1]))
    crossover_point = int(parents.shape[1] / 2)  #common point on both parents
    crossover_rate = 0.8
    i = 0
    while (parents.shape[0] < num_offsprings):
        parent1_index = i % parents.shape[0]
        parent2_index = (i + 1) % parents.shape[0]
        x = rd.random()
        if x > crossover_rate:
            continue
        parent1_index = i % parents.shape[0]
        parent2_index = (i + 1) % parents.shape[0]
        offsprings[i, 0:crossover_point] = parents[parent1_index,
                                                   0:crossover_point]
        offsprings[i, crossover_point:] = parents[parent2_index,
                                                  crossover_point:]
        i = +1
    return offsprings


#Mutation fuction using bit-flip technique
def mutation(offsprings):
    mutants = np.empty((offsprings.shape))
    mutation_rate = 0.4
    for i in range(mutants.shape[0]):
        random_value = rd.random()
        mutants[i, :] = offsprings[i, :]
        if random_value > mutation_rate:
            continue
        int_random_value = randint(0, offsprings.shape[1] - 1)
        if mutants[i, int_random_value] == 0:
            mutants[i, int_random_value] = 1
        else:
            mutants[i, int_random_value] = 0
    return mutants


#Calling functions + optimising parameters
def optimise(weight, value, population, pop_size, num_generations, threshold):
    parameters, fitness_history = [], []
    num_parents = int(pop_size[0] / 2)
    num_offsprings = pop_size[0] - num_parents
    for i in range(num_generations):
        #Intialsing the variables returned from the functions called
        fitness = cal_fitness(weight, value, population, threshold)
        fitness_history.append(fitness)
        parents = selection(fitness, num_parents, population)
        offsprings = crossover(parents, num_offsprings)
        mutants = mutation(offsprings)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants
    print("{1}Last generation:{2} \n{0}\n".format(population, bold, reset))
    fitness_last_gen = cal_fitness(weight, value, population, threshold)
    print("{1}Fitness of the last generation:{2} \n{0}\n".format(
        fitness_last_gen, bold, reset))
    max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
    parameters.append(population[max_fitness[0][0], :])
    return parameters, fitness_history


parameters, fitness_history = optimise(weight, value, initial_population,
                                       pop_size, num_generations,
                                       suitcase_threshold)
print("{1}The optimized parameters for the given inputs are: \n{0}{2}".format(
    parameters, bold, reset))
selected_items = item_number * parameters
print("\n{0}{1}The items you should carry, otherwise pay extra! Goodbye!{2}".
      format(blue, bold, reset))

print('%-10s%-28s%-10s%-10s' %
      ("\033[40;32mITEM NO.", "ITEM NAME", "WEIGHT", "VALUE\033[0;0m"))
for i in range(selected_items.shape[1]):
    if selected_items[0][i] != 0:

        #Outputs the optimised parameters and the items the user should carry
        print('%-10d%-25s%-10d%-10d' %
              (selected_items[0][i], item_nameArray[i], weightArray[i],
               valueArray[i]))
