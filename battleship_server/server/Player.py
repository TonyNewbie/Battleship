from server.Ship import *
from random import randrange


class Player:
    def __init__(self):
        self.ships = []
        self.fleet_coord = []
        self.battlefield = [[0 for _ in range(10)] for _ in range(10)]
        self.shoots = []
        self.ships_create()

    def __str__(self):
        return f'{self.ships} {self.battlefield} {self.fleet_coord}'

    def battlefield_change(self, coord_list, status):
        for coord in coord_list:
            battlefield_row, battlefield_column = [int(x) for x in coord.split('_')]
            self.battlefield[battlefield_row][battlefield_column] = status

    def ships_create(self):
        ships_counter = 0
        while ships_counter < 10:
            self.ships = []
            self.battlefield = [[0 for _ in range(10)] for _ in range(10)]
            self.fleet_coord = []
            ships_counter = 0
            for length in range(4, 0, -1):
                for i in range(5 - length):
                    try_number = 0
                    while True:
                        try_number += 1
                        if try_number > 50:
                            break
                        start_point = f'{randrange(10)}_{randrange(10)}'
                        orientation = randrange(2)
                        ship = Ship(length, orientation, start_point)
                        ships_crossing = set(self.fleet_coord) & set(ship.ship_coord + ship.ship_around)
                        if ship.correct_create and not ships_crossing:
                            self.fleet_coord += ship.ship_coord + ship.ship_around
                            self.ships.append(ship)
                            ships_counter += 1
                            self.battlefield_change(ship.ship_coord, 1)
                            break

    def shoot(self, enemy, coord):
        shoot_status = 0
        for ship in enemy.ships:
            if coord in ship.ship_coord:
                self.shoots.append(coord)
                ship_peace_index = ship.ship_coord.index(coord)
                ship.ship_status[ship_peace_index] = 0
                if 1 in ship.ship_status:
                    shoot_status = 1
                    return shoot_status, [coord]
                else:
                    shoot_status = 2
                    ship.alive = False
                    self.shoots += ship.ship_around
                    return shoot_status, ship.ship_coord + ship.ship_around
        return shoot_status, []


class AIPlayer(Player):
    def __init__(self):
        super().__init__()
        self.attempt = 0

    def make_move(self):
        if self.attempt == 0:
            while True:
                row_index = randrange(10)
                column_index = randrange(10)
                if f'{row_index}_{column_index}' not in self.shoots:
                    break
        elif self.attempt == 1:
            neighbor_points = []
            previous_point_row, previous_point_column = [int(x) for x in self.shoots[-1].split('_')]
            for i in range(previous_point_row - 1, previous_point_row + 2):
                for j in range(previous_point_column - 1, previous_point_column + 2):
                    if (0 <= i <= 9 and 0 <= j <= 9 and i != j
                            and (i == previous_point_row or j == previous_point_column)
                            and not (i == previous_point_row and j == previous_point_column)
                            and not (f'{i}_{j}' in self.shoots)):
                        neighbor_points.append([i, j])
            random_point = randrange(len(neighbor_points))
            row_index = neighbor_points[random_point][0]
            column_index = neighbor_points[random_point][0]
        elif self.attempt == 2:
            attempt_one_point_row, attempt_one_point_column = self.shoots[-1].split('_')
            attempt_two_point_row, attempt_two_point_column = self.shoots[-2].split('_')
            if attempt_one_point_row == attempt_two_point_row:
                min_column = min(int(attempt_one_point_column), int(attempt_two_point_column))
                neighbor_points = [[attempt_one_point_row, min_column],[]]
            else:
                common = attempt_one_point_column
        # return f'{row_index}_{column_index}'





# player = Player()
# player_two = Player()
# for line in player_two.battlefield:
#     print(line)
# while True:
#     coord = input()
#     result = player.shoot(player_two, coord)
#     print(result)
#     if result[0]:
#         player_two.battlefield_change(result[1], 2)
#     for line in player_two.battlefield:
#         print(line)
