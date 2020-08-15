from server.Player import *


another_computer = AIPlayer()
computer = AIPlayer()
print('Поле другого коспьютера')
for line in another_computer.battlefield:
    print(line)
print('Поле компьютера')
for line in computer.battlefield:
    print(line)
while True:
    while True:
        # while True:
        #     another_computer_coord = another_computer.coord_select()
        #     if another_computer_coord not in another_computer.shoots:
        #         break
        result = another_computer.shoot(computer, another_computer_coord)
        if result[0] == 0:
            print('Мимо')
            print('Очередь компьютера')
            break
        elif result[0] == 1:
            print('Ранил')
        else:
            print('Убил')
            if not computer.check_finish():
                print('Another computer win!!!')
                exit()
        print('Поле другого компьютера')
        for line in another_computer.battlefield:
            print(line)
        print('Поле компьютера')
        for line in computer.battlefield:
            print(line)
    print('Поле другого коспьютера')
    for line in another_computer.battlefield:
        print(line)
    print('Поле компьютера')
    for line in computer.battlefield:
        print(line)
    while True:
        while True:
            computer_coord = computer.coord_select()
            if computer_coord not in computer.shoots:
                break
        result = computer.shoot(another_computer, computer_coord)
        if result[0] == 0:
            print('Мимо')
            print('Очередь другого компа')
            break
        elif result[0] == 1:
            print('Попал')
        else:
            print('Убил')
            if not another_computer.check_finish():
                print('Computer win!!!')
                exit()
        print('Поле другого коспьютера')
        for line in another_computer.battlefield:
            print(line)
        print('Поле компьютера')
        for line in computer.battlefield:
            print(line)
        computer_shoot = computer.coord_select()
    print('Поле другого компьютера')
    for line in another_computer.battlefield:
        print(line)
    print('Поле компьютера')
    for line in computer.battlefield:
        print(line)
