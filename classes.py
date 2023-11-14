import random
import copy

NAMES = [
    "Sir Maximus Fortunatus","Sir Ludovicus Comedicus","Sir Franciscus Amabilis",
    "Sir Hectorius Jocundus","Sir Ferdinandus Iocosus","Sir Augustus Ridiculus",
    "Sir Ignatius Grotescus","Sir Gaius Ludimagister","Sir Cornelius Chortlus",
    "Sir Bonifacius Gelasinus","Sir Maximilianus Fatuus","Sir Wolfram Ludentus",
    "Sir Leopoldus Quiritis","Sir Rodericus Iocundus","Sir Ulricus Ridiculorum",
    "Sir Baldwinus Risus","Sir Reginaldus Absurdus","Sir Othmar Ludens","Sir Percival Fallicus",
    "Sir Godfrey Facetius","Sir Cedricus Iocosissimus","Sir Darien Saltator",
    "Sir Theobaldus Ridiculus","Sir Baldwin Ridiculificus","Sir Thaddeus Ioculator",
    "Sir Alaricus Absurdissimus","Sir Valerianus Ludentius","Sir Percivalus Ludimagister",
    "Sir Baldwinus Chortulus","Sir Oswin Ridens","Sir Cyprianus Ioculatus",
    "Sir Julianus Fatuus","Sir Egbertus Ludentissimus","Sir Lysander Grotescus"
    ]
SUICIDAL_TENDENCIES = 0.01

class Item():
    def __init__(self,attack,durability):
        self.attack = attack
        self.durability = durability

class Sword(Item):
    pass

class Staff(Item):
    def __init__(self, callback):
        self.callback = callback

class Knight():
    def __init__(self, hp, attack, defense, name="Pepa"):
        self.hp = hp
        self.name = name
        self.attack = attack
        self.defense = defense

    def __str__(self):
        return f"My name is {self.name} and I have {self.hp} HP. I am of a class {type(self).__name__}"
    
class Swordsman(Knight):
    def __init__(self, hp, attack, defense, sword, name="Pepa"):
        super().__init__(hp, attack, defense, name)
        self.sword = sword

    def fight(self, enemy):
        dmg = self.attack + self.sword.attack - enemy.defense
        if self.sword.durability > 0:
            dmg -= self.sword.attack
            self.sword.durability -= 1
        if dmg <= 0:
            dmg = 1
        enemy.hp -= dmg
        return enemy
        
class Healer(Knight):
    def __init__(self, hp, attack, defense, heal_power, name="Pepa"):
        super().__init__(hp, attack, defense, name)
        self.heal = heal_power

    def fight(self, enemy):
        dmg = self.attack - enemy.defense
        if dmg <= 0:
            dmg = 1
        enemy.hp -= dmg
        self.hp += self.heal
        return enemy
    
class Mage(Knight):
    def __init__(self, hp, attack, defense, staff, name="Pepa"):
        super().__init__(hp, attack, defense, name)
        self.staff = staff
        self.hp /= 2

    def fight(self, enemy):
        self.staff.callback(self,enemy)
        return enemy

class Tank(Knight):
    def __init__(self, hp, attack, defense, name="Pepa"):
        super().__init__(hp, attack, defense, name)
        self.hp *= 4
        self.defense *= 2
        self.attack += 3

    def fight(self, enemy):
        dmg = self.attack - enemy.defense
        if dmg <= 0:
            dmg = 1
        enemy.hp -= dmg
        return enemy
    

class Tournament():
    def __init__(self, knights):
        self.knights = knights

    def duel(self):
        while len(self.knights) > 1:
            pairs = self.make_pairs()
            for pair in pairs:
                loser = self.battle(pair)
                self.knights.remove(loser)
        print("What did the winner say after his victory???")
        return self.knights[0]

    def make_pairs(self):
        fighters = [knight for knight in self.knights]
        pairs = []
        odd_one_out = None
        if len(fighters) % 2 == 1:
            odd_one_out = fighters.pop(random.randint(0,len(fighters)-1))
        num_of_pairs = len(fighters)//2
        for i in range(num_of_pairs):
            knight_1 = fighters.pop(random.randint(0,len(fighters)-1))
            knight_2 = fighters.pop(random.randint(0,len(fighters)-1))
            pairs.append((knight_1,knight_2))
        return pairs

    def battle(self, pair):
        knight_1 = copy.deepcopy(pair[0])
        knight_2 = copy.deepcopy(pair[1])
        while True:
            knight_2 = knight_1.fight(knight_2)
            probability = random.randint(0, 10000)/100
            if probability <= SUICIDAL_TENDENCIES:
                knight_1.hp = 0
            if knight_2.hp <= 0:
                return pair[1] #kngiht_2
            knight_1 = knight_2.fight(knight_1)
            probability = random.randint(0, 10000)/100
            if probability <= SUICIDAL_TENDENCIES:
                knight_2.hp = 0
            if knight_1.hp <= 0:
                return pair[0] #knight_1


def make_knights(num_of_knights):
    knights = []
    index = 0
    for i in range(num_of_knights):
        if index == 0:
            knights.append(
                Swordsman(random.randint(1,101),random.randint(1,11),random.randint(1,11),
                Sword(random.randint(1,26),random.randint(1,11)),random.choice(NAMES))
            )
        elif index == 1:
            knights.append(
                Healer(random.randint(1,101),random.randint(1,11),random.randint(1,11),
                random.randint(1,16),random.choice(NAMES))
            )
        elif index == 2:
            knights.append(
                Mage(random.randint(1,101),random.randint(1,11),random.randint(1,11),
                Staff(staff_bum_bac),random.choice(NAMES))
            )
        elif index == 3:
            knights.append(
            Tank(random.randint(1,101),random.randint(1,11),random.randint(1,11),random.choice(NAMES))
            )
        index += 1
        if index >= 4:
            index = 0
    return knights

def staff_bum_bac(mage, enemy):
    mage.hp += 5
    enemy.hp -= 5
