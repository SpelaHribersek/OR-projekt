# Osnovna koda za iskanje lihega barvanja
Iščemo liho barvanje vozlišča z najmanjšim številom barv. Uporabljamo backtracking, ker je 
CLP za tak problem neroden (ker dobim ogromno število spremenljivk).

Najprej graf iz sage pretvorimo v slovar (ključi so vozlišča, vrednosti so seznami sosednosti).

1. **Preverjanje barvanja (is_odd_coloring)**
Preveri, ali je določeno barvanje pravilno. Pogleda, ali imajo sosednja vozlišča različne barve in ali je izpolnjen pogoj lihega števila pojavitev barv med sosedi.
2. **Iskanje povezanih komponent (_components)**
Graf razdeli na manjše, med seboj nepovezane dele. Pri tem uporablja algoritem BFS (iskanje v širino).
3. **Iskanje barv ene komponente (_odd_coloring_connected)**
Poskuša različnim vozliščem dodeliti barve. Uporablja rekurzijo in backtracking (vračanje nazaj), da preizkuša možnosti in zavrže tiste, ki ne ustrezajo pravilom.
4. **Barvanje celotnega grafa (odd_coloring)**
Pokliče prejšnjo funkcijo za vsako povezano komponento in združi njihove rezultate.
5. **Iskanje najmanjšega števila barv (odd_chromatic_number)**
Začne z eno barvo in postopoma povečuje število barv, dokler ne najde veljavnega barvanja. Vrne najmanjše število barv in barvanje.

## Testiranje kode za iskanje lihega barvanja
V splošnem velja, da je kromatično število enako 3, če je število vozlišč deljivo s 3. Cikel 5 ima kromatično število 5. Sicer
pa je kromatično število 4.

V datoteki test_odd_osnovno.py najprej zapišemo funkcije za ustvarjanje ciklov, polnih grafov in zvezd.

Potem pa testiramo:
- Preverimo cikle s 3-30 vozlišči. Če zadovoljijo zgornje pogoje vrne `1) cikli C3..C30 OK`.
- Naprej testiramo polne grafe z 2-7 vozlišči. Pri polnem grafu mora vsako vozlišče imeti drugačno barvo kot vsa druga vozlišča.
Zato testiramo, da je `odd_chromatic_number(complete(n))[0] == n`. Če to drži za vsak graf, vrne `"2) polni grafi K2..K7 OK"`.
- Testiramo še zvezde z 1-8 listi. Pravilo je, da potrebujemo 2 barvi, če je listov sodo (središče eno barvo in vsi listi drugo), in 3 barve, če je listov sodo (središče eno barvo in list dve, sicer ne bi imela nobena barva lihega števila vozlišč). če pravili držita, vrne `"3) zvezde OK"`.
- Na koncu lahko testiramo še z grobo silo. Najprej zapišemo funkcijo brute, ki preizkuša vse kombinacije barv vozlišč na grafu in preverja, če je to liho barvanje. Vrne najmanjše število barv, ki ga je lahko uporabil. Potem pa ustvarimo vse možne grafe z največ 5 vozlišči in primerjamo rezultate z našo funkcijo in grobo silo.

Testiramo tako, da v terminal v pythonu napišemo: `python3 test_odd_osnovno.py`. Test nam pokaže, da funkcija deluje pravilno.

