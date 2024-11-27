from unit import *

"""
- Grass terrain ce terrain est visible, on peut savoir quelle grille est de l'herbe, ce que je veux implémenter c'est deux effets pour la grille d'herbe : 1. quand un personnage passe à travers cette grille : le personnage devient invisible et double sa vitesse ; 2. quand un personnage reste finalement dans cette grille, il ne devient pas invisible, le personnage est montré mais s'il reste plus de 2 rounds ou plus, sa valeur de vie sera +. 10.人物经过这个格子的时候：人物会变得不可见，并且速度会增加一倍；2. 人物最后停留在这个格子的时候，并不会隐身，会显示这个人物，但如果他停留超过2回合以上，生命值会+10

- 1.un terrain rocailleux génère des rochers sur une case, alors tous les personnages sauf Guerrier ne peuvent pas traverser cette case, donc si le personnage avance de 4 cases, mais que la case 2 est rocailleuse, le personnage ne peut faire qu'un pas et s'arrêter sur la case avant la case rocailleuse. 2. pour Guerrier, il peut soit ignorer les rochers, soit les écraser, donc si le personnage est maintenant Guerrier, et qu'il veut avancer de 4 cases, il ne peut faire qu'un pas et s'arrêter sur la case avant la case rocailleuse. 3. pour Guerrier, il peut ignorer les rochers, soit les écraser. Si le personnage est un Guerrier et qu'il veut avancer de 4 cases, mais que la deuxième case est rocheuse, il peut détruire le rocher sur cette case, de sorte que cette case ne soit plus rocheuse, et il peut alors avancer de 4 cases comme d'habitude.. 对于Guerrier，他可以无视岩石，或者说他可以撞碎岩石，假如说人物现在是Guerrier，要前进四格，但第2格是岩石，他就可以毁掉这个格子的岩石，就这个格子不再是岩石了，然后他照样可以前进4格

- Eau : le personnage sera ralenti de trente pour cent lors de son passage ; s'il reste sur cette grille pendant plus de deux tours, il perdra 10 points de sang.
"""

class Terrain:
    def __init__(self):
        self.visible = True  # 是否影响单位可见性
        self.able = True

    def apply_effect(self, unit):
        """应用地形对单位的效果，子类会具体实现"""
        pass

    def remove_effect(self, unit):
        """移除地形对单位的影响，如果有持续效果的话"""
        pass

class Bush(Terrain):
    def __init__(self):
        super().__init__()
        self.visible = True  # 草丛是可视的

    def apply_effect(self, unit):
        """单位经过草丛时调用此方法"""
        unit.invisible = True  # 使单位变得不可见
        unit.speed *= 2  # 速度增加一倍
        unit.turns_in_bush = 0  # 初始化在草丛中的回合数

    def stay_effect(self, unit):
        """单位停留在草丛时的效果"""
        unit.turns_in_bush += 1  # 增加在草丛中的回合数
        unit.invisible = False  # 停留时变得可见
        if unit.turns_in_bush > 2:
            unit.health += 10  # 如果停留超过两回合，生命值增加

    def remove_effect(self, unit):
        """单位离开草丛时调用此方法"""
        unit.invisible = False  # 使单位变得可见
        unit.speed /= 2  # 恢复原速度
        unit.turns_in_bush = 0  # 重置在草丛中的回合数

class Rock(Terrain):
    def __init__(self):
        super().__init__()
        self.passable = False  # 默认不可通过

    def apply_effect(self, unit):
        """处理单位尝试进入岩石格子的逻辑"""
        if isinstance(unit, Guerrier):
            self.passable = True  # Guerrier可以破坏岩石使其变为可通行
            return True  # 允许Guerrier继续移动
        return False  # 其他单位不能通过岩石

    def remove_effect(self, unit):
        """单位离开岩石格子的逻辑"""
        # 如果需要的话可以在这里添加额外的逻辑
        pass

class Water(Terrain):
    def __init__(self):
        super().__init__()
        self.visible = True  # 水是可视的

    def apply_effect(self, unit):
        """单位经过水时调用此方法"""
        unit.speed *= 0.7  # 减速30%
        unit.turns_in_water = 0  # 初始化在水中的回合数

    def stay_effect(self, unit):
        """单位停留在水中时的效果"""
        unit.turns_in_water += 1  # 增加在水中的回合数
        if unit.turns_in_water > 2:
            unit.health -= 10  # 如果停留超过两回合，生命值减少10

    def remove_effect(self, unit):
        """单位离开水时调用此方法"""
        unit.speed /= 0.7  # 恢复原速度
        unit.turns_in_water = 0  # 重置在水中的回合数

