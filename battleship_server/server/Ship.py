class Ship:
    # конструктор с параметрами палубности, ориентации на доске и начальной точкой
    def __init__(self, length, orientation, start_point):
        self.length = length  # длина коробля (палубность 1 - 4)
        self.ship_status = []  # статус точек коробля (0 - подбита, 1 - цела)
        self.ship_coord = []  # координаты точек коробля
        self.ship_around = []  # координаты точек вокруг коробля
        self.alive = True  # статус коробля(жив, мертв)
        self.correct_create = True  # статус создания коробля(если не удалось создать, то False)
        row_index, column_index = start_point
        # заполняем массив статусов точек,
        # в зависимости от ориентации заполняем координаты коробля по вертикали или горизонтали
        # если вышли за границы, то считаем попытку создания провальной
        for i in range(length):
            self.ship_status.append(1)
            if row_index + i > 9 or column_index + i > 9:
                self.correct_create = False
            if orientation == 0:
                self.ship_coord.append((row_index, column_index + i))
            else:
                self.ship_coord.append((row_index + i, column_index))
        # проходим вокруг координат созданного корабля, заполняя массив координат вокруг коробля
        for point in self.ship_coord:
            point_row, point_column = point
            for i in range(point_row - 1, point_row + 2):
                for j in range(point_column - 1, point_column + 2):
                    if 0 <= i <= 9 and 0 <= j <= 9:
                        # проверяем, чтобы лишние точки не попали в массив
                        if (i, j) not in self.ship_around and (i, j) not in self.ship_coord:
                            self.ship_around.append((i, j))

    def __str__(self):
        return f'{self.length} {self.ship_coord} {self.ship_around} {self.alive} {self.correct_create}'
