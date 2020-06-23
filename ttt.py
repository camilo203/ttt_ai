import random


mapx = {1: 0, 2: 1, 3: 2}
mapy = {1: 2, 2: 1, 3: 0}


class TicTacToe:
    def __init__(self):
        self.turnX = True
        self.turnO = False
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.round = 0
        self.typeX = None
        self.typeO = None

    def __str__(self):
        prettyboard = "---------\n"
        for row in self.board:
            prettyboard += ("| "+" ".join(row)+" |\n")
        prettyboard += ("---------")
        return prettyboard

    def coordanalisis(self):
        while True:
            val = input("Enter the coordinates: ")
            coords = val.split()
            if len(coords) < 2:
                print("You should enter numbers!")
            else:
                try:
                    r = list(filter(lambda num: 1 <= num <= 3, map(int, coords)))
                    if len(r) == 2:
                        return r
                    else:
                        print("Coordinates should be from 1 to 3!")
                except:
                    print("You should enter numbers!")

    def checkspace(self, x, y, ai=False):
        if ai:
            if self.turnX:
                self.board[x][y] = "X"
                self.turnX = False
                self.turnO = True
                self.round += 1
                return True
            else:
                self.board[x][y] = "O"
                self.turnX = False
                self.turnX = True
                self.round += 1
                return True
        else:
            posy, posx = mapx[x], mapy[y]
            if self.board[posx][posy] != " ":
                return "This cell is occupied! Choose another one!"
            else:
                if self.turnX:
                    self.board[posx][posy] = "X"
                    self.turnX = False
                    self.turnO = True
                    self.round += 1
                    return True
                else:
                    self.board[posx][posy] = "O"
                    self.turnX = False
                    self.turnX = True
                    self.round += 1
                    return True

    def EasyAi(self):
        while True:
            x, y = random.randint(1, 3), random.randint(1, 3)
            val = self.checkspace(x, y)
            if val:
                break

    def MediumAi(self):
        if self.round >= 4:
            mapvert = {3: 0, 4: 1, 5: 2}
            typ = "X" if self.turnX else "O"
            other = "O" if self.turnX else "X"
            state = self.board[:]

            for vert in zip(*self.board):
                state.append(list(vert))
            state.append([self.board[i][i] for i in range(len(self.board))])
            state.append([self.board[i][2-i] for i in range(len(self.board))])

            towin = []
            tostop = []
            for tp, lis in enumerate(state):
                countwin = 0
                countstop = 0
                for elem in lis:
                    if elem == typ:
                        countwin += 1
                    elif elem == other:
                        countstop += 1
                empty = [x for x, y in enumerate(lis) if y == " "]
                if countwin == 2 and any([True if y == " " else False for x, y in enumerate(lis)]):
                    if tp <= 2:
                        towin.append([tp, empty[0]])
                    elif tp <= 5:
                        towin.append([empty[0], mapvert[tp]])
                    elif tp == 6:
                        towin.append([empty[0], empty[0]])
                    else:
                        towin.append([empty[0], 2-empty[0]])
                if countstop == 2 and any([True if y == " " else False for x, y in enumerate(lis)]):
                    if tp <= 2:
                        tostop.append([tp, empty[0]])
                    elif tp <= 5:
                        tostop.append([empty[0], mapvert[tp]])
                    elif tp == 6:
                        tostop.append([empty[0], empty[0]])
                    else:
                        tostop.append([empty[0], 2-empty[0]])
            if towin:
                x, y = random.choice(towin)
                self.checkspace(x, y, True)
            elif tostop:
                x, y = random.choice(tostop)
                self.checkspace(x, y, True)
            else:
                self.EasyAi()

        else:
            self.EasyAi()

    def HardAi(self):

    def analizegame(self, typ):
        results = self.board[:]
        for vert in zip(*self.board):
            results.append(list(vert))
        results.append([self.board[i][i] for i in range(len(self.board))])
        results.append([self.board[i][2-i] for i in range(len(self.board))])
        for i in range(len(results)):
            results[i] = list(
                map(lambda x: True if x == typ else False, results[i]))
        return any(all(i) for i in results)

    def play(self):
        players = ["user", "easy", "medium", "hard"]
        ini = ["start", "exit"]
        while True:
            params = [x.strip() for x in input("Input command ").split()]
            if params[0] in ini:
                if params[0] == "start":
                    if len(params) == 3:
                        if params[1] == "user":
                            self.typeX = "user"
                        elif params[1] == "easy":
                            self.typeX = "easy"
                        elif params[1] == "medium":
                            self.typeX = "medium"
                        elif params[1] == "hard":
                            self.typeX = "hard"
                        if params[2] == "user":
                            self.typeO = "user"
                        elif params[2] == "easy":
                            self.typeO = "easy"
                        elif params[2] == "medium":
                            self.typeO = "medium"
                        elif params[2] == "hard":
                            self.typeO = "hard"
                        if params[1] not in players or params[2] not in players:
                            print("Bad parameters!")
                        elif params[1] in players and params[2] in players:
                            break
                    else:
                        print("Bad parameters!")
                else:
                    exit()
            else:
                print("Bad parameters!")
        print(self)
        while True:
            if self.round >= 5:
                typ = "O" if self.turnX else "X"
                if self.analizegame(typ):
                    print(f"{typ} wins")
                    break
                if self.round == 9:
                    print("Draw")
                    break
            if self.turnX:
                if self.typeX == "easy":
                    self.EasyAi()
                    print('Making move level "easy"')
                    print(self)
                elif self.typeX == "medium":
                    self.MediumAi()
                    print('Making move level "medium"')
                    print(self)
                elif self.typeX == "hard":
                    self.HardAi()
                    print('Making move level "hard"')
                    print(self)
                else:
                    print(self.typeX)
                    x, y = self.coordanalisis()
                    val = self.checkspace(x, y)
                    if val != True:
                        print(val)
                    else:
                        print(self)
            else:
                if self.typeO == "easy":
                    self.EasyAi()
                    print('Making move level "easy"')
                    print(self)
                elif self.typeO == "medium":
                    self.MediumAi()
                    print('Makin move level "medium"')
                    print(self)
                elif self.typeO == "hard":
                    self.HardAi()
                    print('Making move level "hard"')
                    print(self)
                else:
                    x, y = self.coordanalisis()
                    val = self.checkspace(x, y)
                    if val != True:
                        print(val)
                    else:
                        print(self)


e = TicTacToe()
e.play()
