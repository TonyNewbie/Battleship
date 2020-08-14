class Ship:
    # length = 1  # длина коробля (палубность 1 - 4)
    # ship_status = []  # статус точек коробля (0 - подбита, 1 - цела)
    # ship_coord = []  # координаты точек коробля
    # ship_around = []  # координаты точек вокруг коробля
    # alive = True  # статус коробля (жив, мертв)
    # correct_create = True  # статус создания коробля(если не удалось создать, то False)

    # конструктор с параметрами палубности, ориентации на доске и начальной точкой
    def __init__(self, length, orientation, start_point):
        self.length = length
        self.ship_status = []
        self.ship_coord = []
        self.ship_around = []
        self.alive = True
        self.correct_create = True
        row_index, column_index = [int(x) for x in start_point.split('_')]
        # заполняем массив статусов точек,
        # в зависимости от ориентации заполняем координаты коробля по вертикали или горизонтали
        # если вышли за границы, то считаем попытку создания провальной
        for i in range(length):
            self.ship_status.append(1)
            if row_index + i > 9 or column_index + i > 9:
                self.correct_create = False
            if orientation == 0:
                self.ship_coord.append(f'{row_index}_{column_index + i}')
            else:
                self.ship_coord.append(f'{row_index + i}_{column_index}')
        # проходим вокруг координат созданного корабля, заполняя массив координат вокруг коробля
        for point in self.ship_coord:
            point_row, point_column = [int(x) for x in point.split('_')]
            for i in range(point_row - 1, point_row + 2):
                for j in range(point_column - 1, point_column + 2):
                    if 0 <= i <= 9 and 0 <= j <= 9:
                        # проверяем, чтобы лишние точки не попали в массив
                        if f'{i}_{j}' not in self.ship_around and f'{i}_{j}' not in self.ship_coord:
                            self.ship_around.append(f'{i}_{j}')

    def __str__(self):
        return f'{self.length} {self.ship_coord} {self.ship_around} {self.alive} {self.correct_create}'
