import itertools
from odd_coloring import *


# CIKLI
def cycle(n):
    return {i: [(i-1) % n, (i+1) % n] for i in range(n)}
# % n poskrbi, da se cikel sklene: zadnje vozlišče je povezano s prvim.
# za i določimo njegova soseda (vozlišči i-1 in i+1)


# POLNI GRAFI
def complete(n):
    return {i: [j for j in range(n) if j != i] for i in range(n)} # vsako vozlišče i ima za sosede vsa vozlišča razen sebe


# ZVEZDE (eno središče in več listov)
def star(n):                       # sredisce 0, n listov
    adj = {0: list(range(1, n + 1))} # središče ima za sosede vsa ostala vozlišča
    for i in range(1, n + 1): # vsak list ima za soseda samo središče
        adj[i] = [0]
    return adj


# 1) cikli: kr.st. = 3 (3|n), 5 (n=5), sicer 4
for n in range(3, 31):
    exp = 3 if n % 3 == 0 else (5 if n == 5 else 4)
    assert odd_chromatic_number(cycle(n))[0] == exp, ("cikel", n)
print("1) cikli C3..C30 OK")

# 2) polni grafi: kr.st.(K_n) = n
for n in range(2, 8):
    assert odd_chromatic_number(complete(n))[0] == n, ("K", n)
print("2) polni grafi K2..K7 OK")

# 3) zvezde: liho stevilo listov -> 2 barvi, sodo -> 3 barve
for n in range(1, 9):
    exp = 2 if n % 2 == 1 else 3
    assert odd_chromatic_number(star(n))[0] == exp, ("zvezda", n)
print("3) zvezde OK")


# 4) groba sila na VSEH grafih do 5 vozlisc
def brute(adj):
    vs = list(adj) # seznam vseh vozlišč
    for k in range(1, len(vs) + 1): # zanka čez število barv (od 1 do števila vozlišč)
        for cols in itertools.product(range(k), repeat=len(vs)): # vse možne razporeditve barv za vozlišča
            if is_odd_coloring(adj, dict(zip(vs, cols))): # ali je trenutna razporeditev barv pravilna
                return k # Ker preizkušamo število barv od najmanjšega navzgor, je to tudi najmanjše število barv, ki ga potrebujemo.
    return 0

# Ustvarjanje vseh grafov z največ 5 vozlišči in preverjanje ujemanja z grobo silo
for n in range(1, 6):
    pairs = list(itertools.combinations(range(n), 2))  # ustvarimo vse možne pare vozlišč
    for mask in range(2 ** len(pairs)): # ustvarimo vse možne kombinacije povezav
        adj = {i: [] for i in range(n)} # prazen graf, v katerem so vsa vozlišča že prisotna, vendar še nimajo povezav
        for b, (u, v) in enumerate(pairs): # gremo skozi vse možne povezave
            if mask >> b & 1:  # preverimo, ali je b-ta možna povezava vključena v graf
                adj[u].append(v); adj[v].append(u) # povežemo vozlišči
        assert odd_chromatic_number(adj)[0] == brute(adj), (n, mask) # primerjamo rezultate dveh različnih pristopov
print("4) groba sila, vsi grafi do 5 vozlisc OK")