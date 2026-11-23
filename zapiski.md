### Osnovna koda za iskanje lihega barvanja
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

