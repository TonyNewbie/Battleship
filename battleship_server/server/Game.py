from server.Player import *


class Game:
    def __init__(self):
        self.player = Player()
        self.ai_player = Player()
        self.status = 'in game'

    @staticmethod
    def check_finish(player):
        alive_counter = 0
        for ship in player.ships:
            if ship.alive:
                alive_counter += 1
        if not alive_counter:
            return 'win'
