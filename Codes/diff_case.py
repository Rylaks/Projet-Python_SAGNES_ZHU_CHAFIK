class Terrain:
    NORMAL = 0 # case normale， 
    BUSH = 1 # case bush， les personnages entrent deviennent invisibles, puis la vitesse de déplacement augmente, si rester dans l’herbe pendant une longue période (3 tours) augmente 1 point de vie.
    ROCK = 2 # case rock les personnages  ne peut pas passer à travers cette grille, puis le guerrier peut briser les roches, mais ce tour il ne peut pas se déplacer et faire d’autres mouvements
    WATER = 3 # case water,le personnage va ralentir en entrant et un peu de vie sera déduit s’il reste longtemps dans l’eau (2 tours)


   
    