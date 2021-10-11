import pandas as pnd
import numpy as np
from itertools import permutations
import matplotlib.pyplot as plt
from datetime import datetime

start_time = datetime.now()

"""
Definerer variablene df (dataframe med de respektive avstandene), N (antall byer jeg vil besøke),
cities_lst og cities_lst_prm (hhv. byrepresentasjons liste fra 0 til N-1 og alle mulige rekkefølge-kombinasjoner av disse).
"""
df = pnd.read_csv("european_cities.csv", delimiter = ";")
N = 10
cities_lst = list(range(N))
cities_lst_prm = list(permutations(cities_lst))

"""
For hver enkelt rekkefølge-kombinasjon i cities_lst_prm, summeres avstandene i en nøstet for loop for å finne
total distanse for gjeldende kombinasjon. Sjekker deretter om gjeldene distanse er kortere enn den foregående
og velger i så fall denne som shrt_act_seq (korteste rutevalg).
"""
shrt_act_seq = cities_lst_prm[0]
min_dist_sum = 100000
for i in range(len(cities_lst_prm)):
    sum = 0
    for j in range(len(cities_lst_prm[i]) - 1):
        k = cities_lst_prm[i][j]
        l = cities_lst_prm[i][j+1]
        sum += (df.iloc[k][l])
    k = cities_lst_prm[i][0]
    sum += (df.iloc[l][k])
    if sum < min_dist_sum:
        min_dist_sum = sum
        shrt_act_seq = cities_lst_prm[i]

"""
Legger bynavnene (i dataframens rekkefølge) i en liste (city_names_lst) og
appender de med respektive indekser fra shrt_act_seq i shrt_tour.
"""
city_names_lst = list(df.columns)
shrt_tour = []
for i in shrt_act_seq:
    shrt_tour.append(city_names_lst[i])
shrt_tour.append(shrt_tour[0])

tot_dist = int(min_dist_sum)
print(f"Shortest travelling distance is {tot_dist} km. ({N} first cities in the table)")
print("Shortest route city-sequence is {}.".format(", ".join(shrt_tour)))
print()

end_time = datetime.now()
print(f"Execution time: {end_time - start_time}")

t = [0.12, 0.15, 0.5, 3.4, 26, 300, 3060]
nmb_cit = [4, 5, 6, 7, 8, 9, 10]

fig = plt.figure(figsize = (6, 4), dpi = 130)
plt.title("Execution time for increasing\nnumber of cities in exhaustive search")
plt.xlabel("Time (s)")
plt.ylabel("Number of cities")
plt.plot(nmb_cit, t, "o")
plt.grid()
fig.savefig("exec_time_plt", dpi = 130)
plt.show()


"""
Lager en liste (time_evo) med tidstegene mellom de økende tidene for økende antall byer
for å finne et gjennomsnittlig forhold mellom økningen i tid fra n til n+1 antall byer.
Deretter multipliserer jeg dette forholdet med gjeldende tid 14 ganger fra og med gjeldende tid for 10 byer.
"""
time_evo = []
for i in range(len(t) - 1):
    dt = t[i+1] - t[i]
    time_evo.append(dt)

def avg(lst):
    return np.sum(lst)/len(lst)

time_evo_rel = [time_evo[1]/time_evo[0], time_evo[2]/time_evo[1], time_evo[3]/time_evo[2], time_evo[4]/time_evo[3], time_evo[5]/time_evo[4]]

t_s = 3060
for i in range(14):
    t_s = t_s*avg(time_evo_rel)

t_m = t_s/60
t_h = t_m/60
t_d = t_h/24
t_y = int(t_d/365)

print()
print(f"Exhaustive search on 24 cities would take approximatily {t_s} seconds. (ish {t_y} years).")
