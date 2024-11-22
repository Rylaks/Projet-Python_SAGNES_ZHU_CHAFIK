class Skills:
    #Pour tout le monde:
    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            if target.defense_shield >= self.attack_power:
                target.defense_shield -= self.attack_power
            else:
                target.defense_shield = 0
                target.health -= self.attack_power - target.defense_shield


    #pour les mages:
    def heal(self,target,value):
        """Soigne les points de vie d'une unité alliée à portée, et utilise du mana"""
        if target.team == "player":
            target.health += value
            self.mana -= value
        else:
            raise TypeError ("Cette compétence ne peut être utiliser que sur des unités alliées")

    #pour les voleurs:
    def invisibility(self):
        """Porte l'anneau et se rend invisible (et donc intouchable) des unités ennemies"""
        #chaque tour invisible coûte des points de bouclier (ça fatigue!), puis des points de vie quand le bouclier est à 0.
        if self.defense_shield > 0:
            self.defense_shield -= 1
        else:
            self.health -= 1

    #pour les guerriers:
    def bow(self,target):
        """Attaque à longue portée avec un arc"""
        if abs(self.x - target.x) <= 4 and abs(self.y - target.y) <= 4:
            if target.defense_shield >= round(self.attack_power*0.5):
                target.defense_shield -= round(self.attack_power*0.5)
            else:
                target.defense_shield = 0
                target.health -= round((self.attack_power - target.defense_shield)*0.5)