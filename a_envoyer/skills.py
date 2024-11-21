

class Skills:
    #Pour tout le monde;
    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    #pour les mages:
    def heal(self,target):
        """Soigne les points de vie une unité alliée à portée"""

    #pour les voleurs:
    def invisibility(self):
        """Porte l'anneau et se rend invisible (et donc intouchable) des unités ennemies"""
        #chaque tour invisible coûte des points de bouclier (ça fatigue!), puis des points de vie quand le bouclier est à 0.

    #pour les guerriers:
    def bow(self):
        """Attaque à longue portée avec un arc"""