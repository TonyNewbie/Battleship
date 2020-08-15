from rest_framework.response import Response
from rest_framework.views import APIView
from server.Player import *

player = Player()
computer = AIPlayer()


class StartGameView(APIView):
    def get(self, request):
        global player, computer
        player = Player()
        computer = AIPlayer()
        fields = {
            'player_field': player.battlefield,
            'computer_field': computer.battlefield
        }
        return Response({'fields': fields})


class GameProcessView(APIView):
    def get(self, request, coord):
        global player, computer
        game_status = 'continue'
        player_coord = tuple([int(x) for x in coord])
        player_changes = {}
        computer_changes = {}
        while True:
            shoot_result = player.shoot(computer, player_coord)
            if shoot_result[0] == 0:
                computer_changes[coord] = 0
                break
            else:
                if shoot_result[0] == 1:
                    computer_changes[coord] = 1
                if shoot_result[0] == 2:
                    computer_changes[coord] = 1
                    for death_ship_coord in shoot_result[1]:
                        computer_changes[''.join(map(str, death_ship_coord))] = 0
                    if not computer.check_finish():
                        game_status = 'player win'
                return Response({'fields': {
                    'player_changes': player_changes,
                    'computer_changes': computer_changes,
                    'game_status': game_status
                }})
        while True:
            computer_coord = computer.coord_select()
            shoot_result = computer.shoot(player, computer_coord)
            if shoot_result[0] == 0:
                player_changes[''.join(map(str, computer_coord))] = 0
                break
            else:
                if shoot_result[0] == 1:
                    player_changes[''.join(map(str, computer_coord))] = 1
                if shoot_result[0] == 2:
                    player_changes[''.join(map(str, computer_coord))] = 1
                    for death_ship_coord in shoot_result[1]:
                        player_changes[''.join(map(str, death_ship_coord))] = 0
                    if not player.check_finish():
                        game_status = 'computer win'
                        return Response({'fields': {
                            'player_changes': player_changes,
                            'computer_changes': computer_changes,
                            'game_status': game_status
                        }})
        return Response({'fields': {
            'player_changes': player_changes,
            'computer_changes': computer_changes,
            'game_status': game_status
        }})
