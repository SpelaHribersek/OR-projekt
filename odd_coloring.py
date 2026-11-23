"""
Liho barvanje grafov (odd coloring).
Metoda: vracanje (backtracking). Graf je slovar {vozlisce: seznam sosedov}.
"""
from collections import deque


def G_to_adj(G):
    """Sage graf -> slovar sosedov."""
    return {v: list(G.neighbors(v)) for v in G.vertices(sort=False)}

def is_odd_coloring(adj, col): 
    # adj je seznam sosednosti grafa
    # col je slovar, ki vsakemu vozliscu doloca barvo
    """NEODVISNO preverjanje: ali je col liho barvanje grafa adj?"""
    for v in adj: # za vsako vozlisce
        for u in adj[v]: # za vsakega soseda od vozlisca v
            if col[u] == col[v]: # ce je barva enaka vrnemo False
                return False                  
        if adj[v]:  # preverjamo, ce ima vozlisce vsaj enega soseda
            cnt = {} # stejemo pojavitve barv
            for u in adj[v]: # za vsakega soseda
                cnt[col[u]] = cnt.get(col[u], 0) + 1 # pristejemo ena barvi, ki jo ima sosed
                # get() pogleda, ali ta kljuc ze obstaja v slovarju
                # ce ja, pristejemo 1, sicer vzamemo 0 in pristejemo 1
            if not any(c % 2 == 1 for c in cnt.values()): # ce nobena barva ni liha vrnemo False
                return False                    
    return True # sicer vrnemo True

# POVEZANE KOMPONENTE GRAFA
def _components(adj):
    seen, comps = set(), [] 
    # seen je mnozica vozlisc, ki smo jih ze obiskali
    # comps je seznam, v katerega bomo shranjevali povezane komponente
    for s in adj: # gremo cez vsa vozlisca grafa
        if s in seen: # ce smo s ze videli, gremo naprej
            continue
        comp, q = [], deque([s])
        # comp = [] – seznam za vozlisca trenutne komponente
        # q = deque([s]) – vrsto, v katero damo zacetno vozlisce s
        seen.add(s) # s oznacimo kot viden
        while q: # dokler vrsta ni prazna
            v = q.popleft() # odstranimo prvo vozlisce v vrsti in ga shranimo v v
            comp.append(v) # to vozlisce dodamo v trenutno povezano komponento
            for u in adj[v]: # za vsakega soseda od v
                if u not in seen: # ce u se nismo obiskali
                    seen.add(u) # ga damo v seen
                    q.append(u) # in dodamo v vrsto
        comps.append(comp) # komponento, ki smo jo nasli damo v comps
    return comps


# Cilj je najti liho barvanje povezane komponente grafa z najvec k razlicnimi barvami.
# Ce ga najde, vrne slovar col, v katerem je ob vsakem vozliscu zapisana njegova barva.
# Sicer vrne None. 
def _odd_coloring_connected(adj, comp, k):
    # adj – slovar sosednosti grafa.
    # comp – seznam vozlisc ene povezane komponente.
    # k – najvecje dovoljeno stevilo razlicnih barv.
    start = max(comp, key=lambda v: len(adj[v]))   # zacnemo pri vozliscu z najvec sosedi
    # To je koristno, ker ima vozlisce z veliko sosedi navadno vec omejitev pri izbiri barve.
    order, seen, q = [], {start}, deque([start])
    # order = vrstni red obiskovanja vozlisc
    # seen = ze obiskana vozlisca
    # q = vrsta za BFS
    while q:        # dokler vrsta ni prazna
        v = q.popleft() # vzamemo prvo vozlisce iz vrste
        order.append(v) # dodamo ga v seznam order
        for u in adj[v]: # pregledamo sosede vozlisca
            if u not in seen: # ce se ni bil obiskan
                seen.add(u) # ga damo med obiskane
                q.append(u) # ga dodamo v vrsto

    col = {} # pripravimo prazen slovar, v katerega bomo shranjevali barve vozlisc

    # To je pomozna funkcija, ki preveri, ali ima vozlisce x med svojimi sosedi
    # vsaj eno barvo, ki se pojavi liho mnogokrat.
    def ok_odd(x):
        """Ali ima x (ko so vsi sosedje pobarvani) barvo, ki se pojavi liho krat?"""
        if not adj[x]: # ce nima sosedov, potem vrnemo True
            return True
        cnt = {} # ustvarimo prazen slovar za stetje barv sosedov
        for u in adj[x]: # prestejemo kolikorat se posamezna barva pojavi med sosedi
            cnt[col[u]] = cnt.get(col[u], 0) + 1
        return any(c % 2 == 1 for c in cnt.values()) 

    def extend(i, m):    
        # i = indeks vozlisca v seznamu order, ki ga trenutno barvamo
        # m = stevilo razlicnih barv, ki smo jih do zdaj uporabili
        if i == len(order):
             # ce je i enak dolzini seznama order, smo pobarvali vsa vozlisca (vrnemo True)
            return True
        v = order[i] # Sicer: izberemo vozlisce, ki ga bomo zdaj poskusili pobarvati.
        forbidden = {col[u] for u in adj[v] if u in col}
        # forbidden so barve, ki jih ze imajo pobarvani sosedi vozlisca v
        for c in range(min(m + 1, k)):      
        # poskusimo uporabiti vse ze uporabljene barve 0,1,...,m-1 ali najvec eno novo (m), ampak ne vec kot k
            if c in forbidden:
                continue  # ce je barva c ze uporabljena pri katerem od pobarvanih sosedov, jo preskocimo.
            col[v] = c # Sicer: dodelimo barvo
            good = True # predpostavimo, da je trenutno barvanje dobro

            # Ker smo pobarvali v, se je lahko zgodilo, da je nekemu vozliscu zdaj pobarvana cela soseska. To sta 
            # v sam ali kateri od njegovih sosedov, zato pregledamo ravno ta vozlisca ([v] + adj[v]).
            for x in [v] + adj[v]:
                if all(u in col for u in adj[x]) and not ok_odd(x):
                    # all(u in col for u in adj[x]): ali so vsi sosedi x ze pobarvani
                    # not ok_odd(x): ali vozlisce x med svojimi sosedi nima niti ene barve, ki se pojavi liho mnogokrat
                    good = False
                    break
                # ce vsi ti pogoji drzijo, so krseni pogoji za liho barvanje. 
            if good and extend(i + 1, max(m, c + 1)):
                # ce je bilo okej, potem nadaljujemo:
                # gremo na naslednje vozlisce (i+1) in posodobimo stevilo uporabljenih barv
                return True
            del col[v]
            # Ce trenutna izbira barve ne vodi do resitve, odstranimo barvo trenutnega
            # vozlisca iz slovarja, ker zelimo poskusiti drugo barvo. 
        return False # ce nobena barva ne deluje vrnemo false

    return dict(col) if extend(0, 0) else None
    # Ce extend najde resitev, vrnemo dict(col), sicer vrnemo None. 

def odd_coloring(adj, k):
    """Liho k-barvanje celotnega grafa (slovar vozlisce->barva) ali None."""
    result = {} # prazen slovar, v katerega bomo shranjevali koncno barvanje celotnega grafa
    for comp in _components(adj): # gremo cez vse komponente
        sub = _odd_coloring_connected(adj, comp, k) # dolocimo liho barvanje komponente
        if sub is None: # ce za katerokoliko komponento ne najdemo lihega barvanja, vrnemo None
            return None
        result.update(sub) # ce smo nasli barvanje, dodamo v result
    return result

# Opomba: v sub in result so kljuci vozlisca in vrednosti barve teh vozlisc.


# Ta funkcija poisce liho kromaticno stevilo grafa in ustrezno barvanje.
def odd_chromatic_number(adj):
    if not adj: # ce graf nima vozlisc, vrnemo kromaticno st. 0 in barvanje kot prazen slovar.
        return 0, {}
    k = 1 # Zacnemo z eno barvo. 
    while True: # Ponavljamo, dokler ne najdemo ustreznega barvanja.
        col = odd_coloring(adj, k) # A lahko pobarvamo graf?
        if col is not None: # ce ga lahko:
            assert is_odd_coloring(adj, col)        # varnostno preverjanje (True če je res, sicer vrne napako AssertionError)
            return k, col # vrnemo najmanjse st. barv in ustrezno barvanje
        k += 1 # sicer st. barv povecamo za 1

# col: ključi vozlišča, vrednosti njihove barve
