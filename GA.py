import pandas as pnd
import numpy as np
from datetime import datetime
import random as rnd

df = pnd.read_csv("european_cities.csv", delimiter = ";")
N = 7

"""
Funksjon som genererer en tilfeldig valgt rute innom samtlige byer. i for loopen velges en tilfeldig by og legges til
i "solution" før den slettes fra cities_lst så den ikke kan velges igjen på nytt. Til slutt returneres solution (et tilfeldig rutevalg).
"""
def rand_strt_tour():
    solution = []
    cities_lst = list(range(N))
    for i in range(N):
        rand_cit = cities_lst[rnd.randint(0, len(cities_lst) - 1)]
        solution.append(rand_cit)
        cities_lst.remove(rand_cit)
    solution.append(solution[0])
    return solution


"""
Funksjon som regner ut rutedistansen ved at "sum" summeres opp med de respektive avstandene mellom n-te og n+1-te indeks i
argumentet. returnerer til slutt total rutedistanse (sum).
"""
def tour_lenght(tour_):
    sum = 0
    for i in range(len(tour_) - 1):
        k = tour_[i]
        l = tour_[i+1]
        sum += (df.iloc[k][l])
    return sum

"""
Funksjon som genererer en populasjon med alternative ruter. Tar inn "size" (ønsket størrelse på populasjon).
pop_lst returneres som en liste med alternative ruter.
"""
def gen_pop(size):
    pop_lst = []
    i = 0
    while i < size:
        rand_tour = rand_strt_tour()
        if rand_tour not in pop_lst:
            pop_lst.append(rand_tour)
            i += 1
    return pop_lst

"""
Funksjon som evaluerer fitness-en til hver av alternativene i populasjonen og returnerer en liste med hhv respektive
fitness verdier. fitness verdiene er rett og slett rutedistansen så jo mindre verdi, jo bedre fitness.
"""
def fitness(pop):
    fitness_lst = []
    for i in range(len(pop)):
        fitness_lst.append(tour_lenght(pop[i]))
    return fitness_lst

"""
Funksjon som velger to tilfeldige foreldre blant 30% av de beste rutealternativene i populasjonen, basert på fitness verdien.
Returnerer parent_a og parent_b som to lister med lengde 2, med rutealternativet som index 0 og dets fitness i index 1.
"""
def select(pop):
    thirty_prc = int(0.3*len(pop))
    elite_pop = []
    pop_ = pop.copy()
    fitness_lst = fitness(pop_)
    for i in range(thirty_prc):
        best_fit = min(fitness_lst)
        best_index = fitness_lst.index(best_fit)
        best_tour = pop_[best_index]
        elite_pop.append([best_tour, best_fit])
        fitness_lst.remove(best_fit)
        pop_.remove(best_tour)
    parent_a = elite_pop[rnd.randint(0, len(elite_pop) - 1)]
    elite_pop.remove(parent_a)
    parent_b = elite_pop[rnd.randint(0, len(elite_pop) - 1)]
    return parent_a, parent_b

"""
Funskjon som lager to avkom fra to foreldre, ved å kutte de to rutealternativene ved en tilfeldig valgt
indeks, får så å lime sammen første del av parent_t_a med andre del av parent_t_b og første del av parent_t_b
med andre del av parent_t_a. Deretter forkemmer en mutasjon ved en 50/50 tilfeldighet.
"""
def crossover_and_mutate(p_a, p_b):
    parent_t_a = p_a[0]
    parent_t_b = p_b[0]
    k = rnd.randint(1, len(parent_t_a) - 1)
    offspring_a = parent_t_a[:k] + parent_t_b[k:]
    offspring_b = parent_t_b[:k] + parent_t_a[k:]
    if rnd.random() > 0.5:
        a_ = offspring_a[-1]; b_ = offspring_a[-2]
        offspring_a[-1] = b_; offspring_a[-2] = a_
        a_ = offspring_b[-1]; b_ = offspring_b[-2]
        offspring_b[-1] = b_; offspring_b[-2] = a_
    return offspring_a, offspring_b

start_time = datetime.now()

def run(number_gen, lim_fitness, pop_size):
    population = gen_pop(pop_size)
    for i in range(number_gen):
        parent_a, parent_b = select(population)
        offspring_a, offspring_b = crossover_and_mutate(parent_a, parent_b)
        population.append(offspring_a); population.append(offspring_b)
        fitness_lst = fitness(population)
        if min(fitness_lst) <= lim_fitness:
            index = fitness_lst.index(min(fitness_lst))
            return f"Shortest route found in {i} generations: {population[index]}. Distance = {int(tour_lenght(population[index]))} km."
        worst_index = fitness_lst.index(max(fitness_lst))
        worst_t = population[worst_index]
        worst_f = fitness_lst[worst_index]
        population.remove(worst_t)
        fitness_lst.remove(worst_f)
        worst_index = fitness_lst.index(max(fitness_lst))
        worst_t = population[worst_index]
        worst_f = fitness_lst[worst_index]
        population.remove(worst_t)
        fitness_lst.remove(worst_f)
    index = fitness_lst.index(min(fitness_lst))
    return f"Shortest route found in {number_gen} generations: {population[index]}. Distance = {int(tour_lenght(population[index]))} km."

print(run(50, 5487, 20))

end_time = datetime.now()
print(f"Execution time: {end_time - start_time}")
