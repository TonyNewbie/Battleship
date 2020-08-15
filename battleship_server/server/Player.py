from server.Ship import *
from random import randrange, choice


# класс описывающий игрока и его поведение
class Player:
    def __init__(self):
        self.ships = []  # флот игрока
        self.fleet_coord = []  # координаты флота игрока
        self.battlefield = [[0 for _ in range(10)] for _ in range(10)]  # игровое поле игрока(0 - пустая клетка)
        self.shoots = []  # список координат произведенных выстрелов
        self.ships_create()  # создание флота

    def __str__(self):
        return f'{self.ships} {self.battlefield} {self.fleet_coord}'

    # метод внесения изменений в игровое поле игрока
    # помечает точки из coord_list меткой
    # status(1 - целая точка, 2 - подбитая точка\потопленный корабль, точки вокруг коробля)
    def battlefield_change(self, coord_list, status):
        for coord in coord_list:
            battlefield_row, battlefield_column = coord
            self.battlefield[battlefield_row][battlefield_column] = status

    # метод, создающий флот игрока
    def ships_create(self):
        # создаем корабли, пока их не станет 10
        ships_counter = 0
        while ships_counter < 10:
            # при неудачной попытке начинаем сначала
            self.ships = []
            self.battlefield = [[0 for _ in range(10)] for _ in range(10)]
            self.fleet_coord = []
            ships_counter = 0
            # цикл по длине кораблей
            for length in range(4, 0, -1):
                # количество кораблей в зависимости от длины
                for i in range(5 - length):
                    # количество попыток создания корабля
                    try_number = 0
                    while True:
                        try_number += 1
                        # пробуем 50 раз, не получилось - начинаем сначала
                        if try_number > 50:
                            break
                        # выбираем случайную стартовую точку и ориентацию
                        start_point = (randrange(10), randrange(10))
                        orientation = randrange(2)
                        # создаем корабль и проверяем, чтобы он не пересекался с другими
                        ship = Ship(length, orientation, start_point)
                        ships_crossing = list(set(self.fleet_coord) & set(ship.ship_coord + ship.ship_around))
                        # если все успешно, добавляем корабль и его координаты во флот, изменяем разметку поля
                        if ship.correct_create and not ships_crossing:
                            self.fleet_coord += ship.ship_coord + ship.ship_around
                            self.ships.append(ship)
                            ships_counter += 1
                            self.battlefield_change(ship.ship_coord, 1)
                            break

    # выстрел по врагу, передаем объект Player, по которому стреляем, и координаты выстрела
    # метод возвращает статус выстрела и список измененных точек
    def shoot(self, enemy, coord):
        # статус выстрела (0- мимо, 1 - попал, 2 - убил)
        shoot_status = 0
        self.shoots.append(coord)
        # проверяем наличие координаты выстрела в координатах короблей противника
        for ship in enemy.ships:
            # если попали, меняем статус точки корабля на "подбито"
            if coord in ship.ship_coord:
                ship_peace_index = ship.ship_coord.index(coord)
                ship.ship_status[ship_peace_index] = 0
                # если остались целые точки, то "попал"
                if 1 in ship.ship_status:
                    shoot_status = 1
                    enemy.battlefield[coord[0]][coord[1]] = 3
                    return shoot_status, [coord]
                # если нет, то "убил", добавляем окуржение корабля в спсиок вытсрелов, чтобы не стрелять туда
                else:
                    shoot_status = 2
                    ship.alive = False
                    self.shoots += ship.ship_around
                    enemy.battlefield[coord[0]][coord[1]] = 3
                    enemy.battlefield_change(ship.ship_around, 2)
                    return shoot_status, ship.ship_coord + ship.ship_around
        enemy.battlefield[coord[0]][coord[1]] = 2
        return shoot_status, []

    # метод проверки проигрыша, возвращает True если остались живые корабли, иначе False
    def check_finish(self):
        alive_counter = 0
        for ship in self.ships:
            if ship.alive:
                alive_counter += 1
        if alive_counter:
            return True
        return False


# класс ИИ компьютера, наследуется от Player
# доаолняет логику игрока выбором точки выстрела
class AIPlayer(Player):
    def __init__(self):
        super().__init__()
        self.hits = []  # список удачных выстрелов

    # метод выбора точки выстрела, возвращает координаты выстрела
    def coord_select(self):
        # если успешных выстрелов нет, то выбираем рандомную точку, в которую еще не стреляли
        if not self.hits:
            while True:
                random_point = (randrange(10), randrange(10))
                if random_point not in self.shoots:
                    break
        # если был один успешный выстрел, то случайно выбираем одну из соседних 4 точек
        elif len(self.hits) == 1:
            neighbor_points = []
            previous_point_row, previous_point_column = self.hits[0]
            for i in range(previous_point_row - 1, previous_point_row + 2):
                for j in range(previous_point_column - 1, previous_point_column + 2):
                    if (0 <= i <= 9 and 0 <= j <= 9 and i != j
                            and (i == previous_point_row or j == previous_point_column)
                            and not (i == previous_point_row and j == previous_point_column)
                            and not ((i, j) in self.shoots)):
                        neighbor_points.append((i, j))
            random_point = choice(neighbor_points)
        else:
            # если было больше одного удачного выстрела, то случайно выбираем из 2 крайних точек
            neighbor_points = []
            # если у точек общая строка, выбираем минимальный номер столбца и рассматриваем точки левее и правее
            if self.hits[0][0] == self.hits[1][0]:
                min_column = min(list(zip(*self.hits))[1])
                if min_column - 1 >= 0:
                    neighbor_points.append((self.hits[0][0], min_column - 1))
                if min_column + len(self.hits) <= 9:
                    neighbor_points.append((self.hits[0][0], min_column + len(self.hits)))
            # если общий столбец, выьираем минимальный номер строки и рассматриваем точки выше и ниже
            else:
                min_row = min(list(zip(*self.hits))[0])
                if min_row - 1 >= 0:
                    neighbor_points.append((min_row - 1, self.hits[0][1]))
                if min_row + len(self.hits) <= 9:
                    neighbor_points.append((min_row + len(self.hits), self.hits[0][1]))
            random_point = choice(neighbor_points)
        return random_point
