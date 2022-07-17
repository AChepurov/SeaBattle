from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел вне игрового поля"

class BoardAgainException(BoardException):
    def __str__(self):
        return "В это поле уже был выстрел"

class BoardPlaceException(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, length, start, goriz):
        self.length = length
        self.start = start
        self.goriz = goriz
        self.lives = length

    # все точки корабля списком
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            dot_x = self.start.x
            dot_y = self.start.y

            if self.goriz:
                dot_y += i
            else:
                dot_x += i

            ship_dots.append(Dot(dot_x,dot_y))
        return ship_dots

    # проверка попадания в корабль
    def shooten(self,shot):
        return shot in self.dots

class Board:
    def __init__(self, hid = False, size=6):
        self.size = size
        self.hid = hid
        self.field = [['0']*size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.count = 0

    def __str__(self):
        Board_To_Show = '  |'
        for i in range(self.size):
            Board_To_Show += f' {i+1} |'
        for i, row in enumerate(self.field):
            Board_To_Show += f'\n{i+1} | ' + ' | '.join(row) + ' |'
        if self.hid:
            Board_To_Show = Board_To_Show.replace("■","0")
        return(Board_To_Show)

    def in_board(self,dot):
        return (0 <= dot.x < self.size) and (0 <= dot.y < self.size)

    def mark_busy(self,ship):
        for d in ship.dots:
            for i in range(d.x-1,d.x+2):
                for j in range(d.y-1,d.y+2):
                    if (0 <= i < self.size) and (0 <= j < self.size):
                        curd = Dot(i,j)
                        if curd not in self.busy:
                            self.busy.append(curd)

    def add_ship(self, ship):
        for d in ship.dots:
            if not self.in_board(d) or d in self.busy:
                raise BoardPlaceException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)
        self.ships.append(ship)
        self.mark_busy(ship)

    def shot(self, d):
        if not self.in_board(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardAgainException()
        self.busy.append(d)
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль пострадал!")
                    return True
        self.field[d.x][d.y] = "T"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, pl):
        self.board = board
        self.pl = pl

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                next_move = self.ask()
                repeat = self.pl.shot(next_move)
                return repeat
            except BoardException as e:
                print(e)

class User(Player):
    def ask(self):
        while True:
            turn = input("Ваш ход: ").split()
            if len(turn) != 2:
                print("Введите 2 координаты! \n")
                continue
            x, y = turn
            if not(x.isdigit()) or not(y.isdigit()):
                print("Введите числа! \n")
                continue
            x,y = int(x),int(y)
            return Dot(x-1,y-1)

class AI(Player):
    def ask(self):
        d = Dot(randint(0,5),randint(0,5))
        print(f'Ход компьютера: {d.x+1} {d.y+1}')
        return d

class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        ship_lens = [3, 2, 2, 1, 1, 1, 1]
        b = Board(size = self.size)
        attempts = 0
        for l in ship_lens:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                s = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), randint(0,1))
                try:
                    b.add_ship(s)
                    break
                except BoardPlaceException:
                    pass
        b.begin()
        return b

    def random_board(self):
        b = None
        while b is None:
            b = self.try_board()
        return b

    def greet(self):
        print('  Добро пожаловать в игру')
        print('        МОРСКОЙ БОЙ')
        print('---------------------------')
        print('Формат хода: строка столбец')

    def loop(self):
        num = 0
        while True:
            print('-'*20)
            print('Доска игрока')
            print(self.us.board)
            print('-'*20)
            print('Доска компьютера')
            print(self.ai.board)
            if num % 2 == 0:
                print('-'*20)
                print('Ход игрока')
                repeat = self.us.move()
            else:
                print('-'*20)
                print('Ход компьютера')
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print('-'*20)
                print('Игрок победил!!!')
                break
            if self.us.board.count == 7:
                print('-'*20)
                print('Компьютер победил!!!')
                break
            num += 1


    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()
