from rest_framework.response import Response
from rest_framework.views import APIView
from server.Player import *
from django.shortcuts import render

# глобальные объекты игрока и ИИ
player = Player()
computer = AIPlayer()


def index(request):
    return render(request, "index.html")


class StartGameView(APIView):
    # обработчик запроса начала игры
    # создает игрока и ИИ
    # возвращает поле игрока для открисовки на стороне клиента
    def get(self, request):
        global player, computer
        player = Player()
        computer = AIPlayer()
        return Response({'player_field': player.battlefield})


class GameProcessView(APIView):
    # обработчик выстрела игрока
    # принимает координаты выстрела игрока
    # возвращает изменения в полях игрока и ИИ и текущий статус игры
    def get(self, request, coord):
        global player, computer
        game_status = 'continue'
        # преобразование координат из строки в кортеж
        player_coord = tuple([int(x) for x in coord])
        player_changes = {}
        computer_changes = {}
        while True:
            # выстрел игрока и обработка изменений игровой ситуации
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
                    # проверка на победу
                    if not computer.check_finish():
                        game_status = 'player win'
                return Response({'fields': {
                    'player_changes': player_changes,
                    'computer_changes': computer_changes,
                    'game_status': game_status
                }})
        while True:
            # очередь ИИ, делает выстрел, далее обработка как у игрока
            computer_coord = computer.coord_select()
            shoot_result = computer.shoot(player, computer_coord)
            if shoot_result[0] == 0:
                player_changes[''.join(map(str, computer_coord))] = 0
                break
            else:
                if shoot_result[0] == 1:
                    player_changes[''.join(map(str, computer_coord))] = 1
                    # при попадании записываем координаты в массив попаданий ИИ
                    computer.hits.append(computer_coord)
                if shoot_result[0] == 2:
                    # после потопления вражеского корабля, очищаем список попаданий
                    computer.hits.clear()
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
