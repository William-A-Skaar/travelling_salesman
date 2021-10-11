import pandas as pnd
import numpy as np
from datetime import datetime
import random as rnd

df = pnd.read_csv("european_cities.csv", delimiter = ";")
N = 10

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
    for i in range(N):
        k = tour_[i]
        l = tour_[i+1]
        sum += (df.iloc[k][l])
    return sum

"""
Funksjon som genererer alle mulige nabokombinasjoner av argumentet ved å bytte om på to og to nabo indekser. Etter hvert enkelt nabobytte
legges det nye naboalternativet i neig_lst. Siste loop sjekker om den finner en kortere rute en gjeldende "best" og setter i så fall best til
å være det nye alternativet. Deretter returneres den beste etterfølgeren.
"""
def generate_neig_and_choose_best(current_tour):
    best = current_tour
    neig_lst = []
    neig_lst.append(current_tour)
    for i in range(len(current_tour) - 1):
        tour_neig = current_tour.copy()
        a = current_tour[i]; b = current_tour[i+1]
        tour_neig[i] = b; tour_neig[i+1] = a
        """
        if:
        Dersom vi bytter om på index [0] og [1] i current_tour
        har vi fått en ny startby. Da må også siste element
        settes lik det nye første elementet for å slutte runden.

        elif:
        Dersom vi bytter om på index [-2] og [-1] i current_tour
        har vi fått en ny sluttby. Denne må da naturligvis også
        velges som startby for at runden skal sluttesself.

        else:
        Ellers forandres verken startbyen eller sluttbyen og vi
        appender altså den nye naboen direkte:
        """
        if i == 0:
            tour_neig[-1] = tour_neig[0]
            neig_lst.append(tour_neig)
        elif i == len(current_tour) - 2:
            tour_neig[0] = tour_neig[-1]
            neig_lst.append(tour_neig)
        else:
            neig_lst.append(tour_neig)
    for i in range(len(neig_lst) - 1):
        if tour_lenght(neig_lst[i+1]) < tour_lenght(best):
            best = neig_lst[i+1].copy()
    return best

"""
Til slutt settes en random rutealternativ som beste alternativ. Det lages naboer og dersom det finnes en nabo som er bedre
enn gjeldende beste alternativ, settes denne som nytt gjeldende beste alternativ før prossessen gjentas. Dette gjentas helt
til det ikke finnes noen bedre naboer enn det gjeldende beste alternativet. current_best_tour vil være lokalt topppunkt i
"området" til rnd_strt. Dermed søker vi med 20 forskjellige tilfeldig valgte rnd_strt og noterer dårligste, beste og
gjennomsnittlig resultat.
"""
tours_lst = []
cit_dist_lst = []
ex_time_lst = []
for i in range(20):
    start_time = datetime.now()
    rnd_strt = rand_strt_tour()
    current_best_tour = rnd_strt.copy()
    best_neighbour = generate_neig_and_choose_best(current_best_tour)
    while tour_lenght(best_neighbour) < tour_lenght(current_best_tour):
        current_best_tour = best_neighbour.copy()
        best_neighbour = generate_neig_and_choose_best(current_best_tour)
    end_time = datetime.now()
    ex_time = end_time - start_time
    tours_lst.append(current_best_tour)
    cit_dist_lst.append(tour_lenght(current_best_tour))
    ex_time_lst.append(ex_time)

tot_time = 0
for i in range(len(ex_time_lst)):
    tot_time += ex_time_lst[i].microseconds

best_dist = min(cit_dist_lst)
mean_dist = int(sum(cit_dist_lst)/len(cit_dist_lst))
worst_dist = max(cit_dist_lst)
stand_runtime_ms = tot_time/len(ex_time_lst) # microseconds
stand_runtime_s = round(stand_runtime_ms*1e-6, 3) # seconds with 3 decimals

print(f"Longest distance = {int(worst_dist)} km")
print(f"Average distance = {int(mean_dist)} km")
print(f"Shortest distance = {int(best_dist)} km")
print(f"Standard deviation of the runs = {stand_runtime_s} seconds")
