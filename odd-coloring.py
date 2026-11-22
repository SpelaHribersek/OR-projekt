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
    # col je slovar, ki vsakemu vozlišču določa barvo
    """NEODVISNO preverjanje: ali je col liho barvanje grafa adj?"""
    for v in adj: # za vsako vozlišče
        for u in adj[v]: # za vsakega soseda od vozlišča v
            if col[u] == col[v]: # če je barva enaka vrnemo False
                return False                  
        if adj[v]:  # preverimo, da ima vozlišče vsaj enega soseda
            cnt = {} # štejemo pojavitve barv
            for u in adj[v]: # za vsakega soseda preverimo
                cnt[col[u]] = cnt.get(col[u], 0) + 1 # prištejemo en barvi, ki jo ima sosed
            if not any(c % 2 == 1 for c in cnt.values()): # če nobena barva ni liha vrnemo False
                return False                    
    return True

# POVEZANE KOMPONENTE GRAFA
def _components(adj):
    seen, comps = set(), [] 
    # seen je množica vozlišč, ki smo jih že obiskali
    # comps je seznam, v katerega bomo shranjevali povezane komponente
    for s in adj: # gremo čez vsa vozlišča grafa
        if s in seen: # če smo s že videli, gremo naprej
            continue
        comp, q = [], deque([s])
        # comp = [] – seznam za vozlišča trenutne komponente
        # q = deque([s]) – vrsto, v katero damo začetno vozlišče s
        seen.add(s) # s označimo kot viden
        while q: # dokler vrsta ni prazna
            v = q.popleft() # odstranimo prvo vozlišče v vrsti in ga shranimo v v
            comp.append(v) # to vozlišče dodamo v trenutno povezano komponento
            for u in adj[v]: # za vsakega soseda od v
                if u not in seen: # če u še nismo obiskali
                    seen.add(u) # ga damo v seen
                    q.append(u) # in dodamo v vrsti
        comps.append(comp) # komponento, ki smo jo našli damo v comps
    return comps


# cilj je najti liho barvanje povezane komponente grafa z največ k različnimi barvami
# Če ga najde, vrne slovar col, v katerem je je ob vsakem vozlišču zapisana njegova barva.
# Sicer vrne None. 
def _odd_coloring_connected(adj, comp, k):
    # adj – slovar sosednosti grafa.
    # comp – seznam vozlišč ene povezane komponente.
    # k – največje dovoljeno število različnih barv.
    start = max(comp, key=lambda v: len(adj[v]))   # začnemo pri vozlišču z največ sosedi
    # To je koristno, ker ima vozlišče z veliko sosedi navadno več omejitev pri izbiri barve.
    order, seen, q = [], {start}, deque([start])
    # order = vrstni red obiskovanja vozlišč
    # seen = že obiskana vozlišča
    # q = vrsta za BFS
    while q:        # dokler vrsta ni prazna
        v = q.popleft() # vzamemo prvo vozlišče iz vrste
        order.append(v) # dodamo ga v seznam order
        for u in adj[v]: # pregledamo sosede vozlišča
            if u not in seen: # če še ni bil obiskan
                seen.add(u) # ga damo med obiskane
                q.append(u) # ga dodamo v vrsto

    col = {} # pripravimo prazen slovar, v katerega bomo shranjevali barve vozlišč

    # To je pomožna funkcija, ki preveri, ali ima vozlišče x med svojimi sosedi
    # vsaj eno barvo, ki se pojavi liho mnogokrat.
    def ok_odd(x):
        """Ali ima x (ko so vsi sosedje pobarvani) barvo, ki se pojavi liho krat?"""
        if not adj[x]: # Če nima sosedov, potem vrnemo True
            return True
        cnt = {} # ustvarimo prazen slovar za štetje barv sosedov
        for u in adj[x]: # preštejemo kolikorat se posamezna barva pojavi med sosedi
            cnt[col[u]] = cnt.get(col[u], 0) + 1
        return any(c % 2 == 1 for c in cnt.values()) 

    def extend(i, m):    
        # i = indeks vozlišča v seznamu order, ki ga trenutno barvamo
        # m = število različnih barv, ki smo jih do zdaj uporabili
        if i == len(order):
             # če je i enak dolžini seznama order, smo pobarvali vsa vozlišča (vrnemo True)
            return True
        v = order[i] # izberemo vozlišče, ki ga bomo zdaj poskusili pobarvati
        forbidden = {col[u] for u in adj[v] if u in col}
        # forbidden so barve, ki jih že imajo pobarvani sosedi vozlišča v
        for c in range(min(m + 1, k)):      
        # poskusimo prvo barvo, ki nam je na voljo (odpravimo simetrijo)
            if c in forbidden:
                continue  # Če je barva c že uporabljena pri katerem od pobarvanih sosedov, jo preskočimo.
            col[v] = c # dodelimo barvo
            good = True # predpostavimo, da je trenutno barvanje dobro
            for x in [v] + adj[v]:
                if x in col and all(u in col for u in adj[x]) and not ok_odd(x):
                    # x in col: ali je x že pobarvan
                    # all(u in col for u in adj[x]): ali so vsi sosedi x že pobarvani
                    # not ok_odd(x): ali ima vozlišče x med svojimi sosedi vsaj eno barvo, ki se pojavi liho mnogokrat
                    good = False
                    break
                # Če vsi ti pogoji držijo, so kršeni pogoji za liho barvanje. 
            if good and extend(i + 1, max(m, c + 1)):
                # Če je bilo okej, potem nadaljujemo:
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
        sub = _odd_coloring_connected(adj, comp, k) # določimo liho barvanje komponente
        if sub is None: # če za katerokoliko komponento ne najdemo lihega barvanja, vrnemo None
            return None
        result.update(sub) # če smo našli barvanje, dodamo v result
    return result


# Ta funkcija poišče liho kromatično število grafa in ustrezno barvanje.
def odd_chromatic_number(adj):
    """chi_o(G) in ustrezno barvanje. Graf brez vozlisc ima chi_o = 0."""
    if not adj: # Če graf nima vozlišč, vrnemo kromatično št. 0 in barvanje kot prazen slovar.
        return 0, {}
    k = 1 # Začnemo z eno barvo. 
    while True: # Ponavljamo, dokler ne najdemo ustreznega barvanja.
        col = odd_coloring(adj, k) # A lahko pobarvamo graf?
        if col is not None: # Če ga lahko:
            assert is_odd_coloring(adj, col)        # varnostno preverjanje
            return k, col # vrnemo najmanjše št. barv in ustrezno barvanje
        k += 1 # sicer št. barv povečamo za 1
