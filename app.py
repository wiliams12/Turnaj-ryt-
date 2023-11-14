from classes import *

knights = make_knights(10)
#knights.append(Healer(100,10,10,10,"Mistr Kampanus"))

print(Tournament(knights).duel())
