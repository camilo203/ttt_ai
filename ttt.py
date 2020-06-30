import random


mapx = {1: 0, 2: 1, 3: 2}
mapy = {1: 2, 2: 1, 3: 0}
convert = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0),
           4: (1, 1), 5: (1, 2), 6: (2, 0), 7: (2, 1), 8: (2, 2)}


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

    def evaluateboard(self, board, maximizer):
        board = [board[i-3:i] for i in range(3, 10, 3)]
        minimizer = "X" if maximizer == "O" else "O"
        for row in board:
            if row[0] == row[1] and row[1] == row[2]:
                if row[0] == maximizer:
                    return 10
                elif row[0] == minimizer:
                    return -10
        for column in range(3):
            if board[0][column] == board[1][column] and board[1][column] == board[2][column]:
                if board[0][column] == maximizer:
                    return 10
                elif row[0] == minimizer:
                    return -10

        if board[0][0] == board[1][1] and board[2][2]:
            if board[0][0] == maximizer:
                return 10
            elif row[0] == minimizer:
                return -10
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            if board[0][2] == maximizer:
                return 10
            elif row[0] == minimizer:
                return -10

        return 0

    def makeMove(self, board, pos, typ):
        new = board[:]
        new[pos] = typ
        return new

    def getMoves(self, board):
        moves = []
        for i in board:
            if i != "X" and i != "O":
                moves.append(i)
        return moves

    def state(self, board):
        results1 = board[:]
        for vert in zip(*board):
            results1.append(list(vert))
        results1.append([board[i][i] for i in range(len(board))])
        results1.append([board[i][2-i] for i in range(len(board))])
        results2 = results1[:]
        for i in range(len(results1)):
            results1[i] = list(
                map(lambda x: True if x == "X" else False, results1[i]))
            results2[i] = list(
                map(lambda x: True if x == "O" else False, results1[i]))
        return True if any(all(i) for i in results1) or any(all(i) for i in results2) else False

    def minimax(self, board, player, maximizer, other):
        nboard = [board[i-3:i] for i in range(3, 10, 3)]
        if self.state(nboard):
            return self.evaluateboard(board, player)
        elif self.getMoves(board) == 0:
            return self.evaluateboard(board, player)
        scores = []
        if maximizer:
            for move in self.getMoves(board):
                pos = board[move]
                board[move] = player
                scores.append(self.minimax(
                    board, player, not maximizer, other))
                board[move] = pos
        else:
            for move in self.getMoves(board):
                pos = board[move]
                board[move] = other
                scores.append(self.minimax(
                    board, player, not maximizer, other))
                board[move] = pos
        return max(scores) if maximizer else min(scores)

    def HardAi(self, typ):
        flatboard = [pos if val == " " else val for pos, val in enumerate(
            [elem for row in self.board for elem in row])]
        ai = typ
        other = "X" if ai == "O" else "O"
        best_score = -1111111
        bestmove = None
        for move in self.getMoves(flatboard):
            pos = flatboard[move]
            flatboard[move] = ai
            score = self.minimax(flatboard, ai, False, other)
            flatboard[move] = pos
            if score > best_score:
                best_score = score
                bestmove = move
        x, y = convert[bestmove]
        self.board[x][y] = typ

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
                    self.HardAi("X")
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
                    self.HardAi("O")
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
