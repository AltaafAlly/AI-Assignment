from reconchess import play_local_game
from RandomSensing import BaselineBot
from TroutBot import TroutBot as Trout
from ImprovedAgent import ImprovedBot as ImprovedAgent

if __name__ == '__main__':
    #MATCH 1: Trout vs BaselineBot
    play_local_game(Trout(), BaselineBot())
    #MATCH 2: ImprovedAgent vs BaselineBot
    play_local_game(ImprovedAgent(), BaselineBot())
    #MATCH 3: Trout vs ImprovedAgent
    play_local_game(Trout(), ImprovedAgent())
