import math
import random


class ticTacBoard:
    def __init__(self):
        self.board = [" " for i in range(9)]
        self.stack = []
        self.turnX = True
        self.turnO = False

    def get_possible_moves(self):
        return [pos for pos, val in enumerate(self.board) if val != "X" and val != "O"]

    def undo(self):
        if len(self.stack) > 0:
            self.board[self.stack.pop()] = " "
            self.turnO, self.turnX = self.turnX, self.turnO

    def make_move(self, pos):
        if self.turnX:
            self.board[pos] = "X"
            self.stack.append(pos)
            self.turnX = False
            self.turnO = True
        else:
            self.board[pos] = "O"
            self.stack.append(pos)
            self.turnO = False
            self.turnX = True

    def __str__(self):
        prettyboard = "---------\n"
        separated = [self.board[x-3:x] for x in range(3, 10, 3)]
        for row in separated:
            prettyboard += ("| "+" ".join(row)+" |\n")
        prettyboard += "---------\n"
        return prettyboard

    def get_state(self):
        horizontal = [self.board[i-3:i] for i in range(3, 10, 3)]
        resultsX = []
        resultsX.extend(horizontal)
        for vert in zip(*horizontal):
            resultsX.append(list(vert))
        resultsX.append([horizontal[i][i] for i in range(len(horizontal))])
        resultsX.append([horizontal[i][2-i] for i in range(len(horizontal))])
        resultsO = resultsX[:]
        for i in range(len(resultsX)):
            resultsX[i] = list(
                map(lambda x: True if x == "X" else False, resultsX[i]))
        for i in range(len(resultsO)):
            resultsO[i] = list(
                map(lambda x: True if x == "O" else False, resultsO[i]))
        if sum(map(lambda x: 1 if x == "X" or x == "O" else 0, self.board)) == 9:
            return "OVER" if any((any(all(i) for i in resultsX), any(all(i) for i in resultsO))) else "DRAW"
        else:
            return "OVER" if any((any(all(i) for i in resultsX), any(all(i) for i in resultsO))) else "None"

    def get_winner(self):
        horizontal = [self.board[i-3:i] for i in range(3, 10, 3)]
        resultsX = []
        resultsX.extend(horizontal)
        for vert in zip(*horizontal):
            resultsX.append(list(vert))
        resultsX.append([horizontal[i][i] for i in range(len(horizontal))])
        resultsX.append([horizontal[i][2-i] for i in range(len(horizontal))])
        resultsO = resultsX[:]
        for i in range(len(resultsX)):
            resultsX[i] = list(
                map(lambda x: True if x == "X" else False, resultsX[i]))
        for i in range(len(resultsO)):
            resultsO[i] = list(
                map(lambda x: True if x == "O" else False, resultsO[i]))
        return "X" if any(all(i) for i in resultsX) else "O" if any(all(i) for i in resultsO) else ""


class user:
    convert = {"1 3": 0, "2 3": 1, "3 3": 2, "1 2": 3,
               "2 2": 4, "3 2": 5, "1 1": 6, "2 1": 7, "3 1": 8}

    def __init__(self, board):
        self.board = board

    def move(self):
        while True:
            val = input("Enter the coordinates: ")
            coords = val.split()
            if len(coords) < 2:
                print("You should enter numbers!")
            else:
                try:
                    r = list(filter(lambda num: 1 <= num <= 3, map(int, coords)))
                    if len(r) == 2:
                        pos = self.convert[val.strip()]
                        if pos in self.board.get_possible_moves():
                            self.board.make_move(pos)
                            print(self.board)
                            break
                        else:
                            print("This cell is occupied! Choose another one!")
                    else:
                        print("Coordinates should be from 1 to 3!")
                except:
                    print("You should enter numbers!")


class EasyAi:
    def __init__(self, board):
        self.board = board

    def move(self):
        self.board.make_move(random.choice(self.board.get_possible_moves()))
        print(self.board)


class MediumAi:
    def __init__(self, board, typ):
        self.board = board
        self.typ = typ

    def towin(self):
        for move in self.board.get_possible_moves():
            self.board.make_move(move)
            if self.board.get_winner == self.typ:
                print(self.board)
                break
            self.board.undo()
        else:
            return 1

    def tostop(self):
        invert = {"X": "O", "O": "X"}
        other = invert[self.typ]
        move = None

        rows = [self.board.board[i-3:i] for i in range(3, 10, 3)]
        horizontal = []
        for j, i in enumerate(rows):
            step = []
            for x, y in enumerate(i):
                step.append((x+(j*3), y))
            horizontal.append(step)

        resultsX = []
        resultsX.extend(horizontal)

        for vert in zip(*horizontal):
            resultsX.append(list(vert))
        resultsX.append([horizontal[i][i] for i in range(len(horizontal))])
        resultsX.append([horizontal[i][2-i] for i in range(len(horizontal))])

        for row in resultsX:
            count = 0
            blank = 0
            pos = 0
            for elem in row:
                if elem[1] == other:
                    count += 1
                elif elem[1] == " ":
                    blank += 1
                    pos = elem[0]
            if count == 2 and blank == 1:
                move = pos
                break
        if move is not None:
            self.board.make_move(move)
            print(self.board)
        else:
            return 1

    def rand(self):
        self.board.make_move(random.choice(self.board.get_possible_moves()))
        print(self.board)

    def move(self):
        win = self.towin()
        if win == 1:
            stop = self.tostop()
            if stop == 1:
                self.rand()


class HardAi:
    def __init__(self, board):
        self.board = board

    def move(self):
        bestScore = -math.inf
        bestMove = None
        for move in self.board.get_possible_moves():
            self.board.make_move(move)
            score = self.minimax(False, "O", self.board)
            self.board.undo()
            if (score > bestScore):
                bestScore = score
                bestMove = move
        self.board.make_move(bestMove)
        print(self.board)

    def minimax(self, isMaxTurn, maximizerMark, board):
        state = board.get_state()
        if (state == "DRAW"):
            return 0
        elif (state == "OVER"):
            return 1 if board.get_winner() == maximizerMark else -1

        scores = []
        for move in board.get_possible_moves():
            board.make_move(move)
            scores.append(self.minimax(not isMaxTurn, maximizerMark, board))
            board.undo()
        return max(scores) if isMaxTurn else min(scores)


ttb = ticTacBoard()
print(ttb)
X = ""
O = ""
inicommands = ["start", "exit"]
playercommands = ["user", "easy", "medium", "hard"]
while True:
    command = input("Input command ").split()
    if len(command) == 3:
        if command[0] in inicommands:
            if command[0] == "start":
                if command[1] in playercommands and command[2] in playercommands:
                    X = command[1]
                    O = command[2]
                    break
                else:
                    print("Bad parameters!")
            else:
                exit()
        else:
            print("Bad parameters!")
    else:
        print("Bad parameters!")

if X == "user":
    X = user(ttb)
elif X == "easy":
    X = EasyAi(ttb)
elif X == "medium":
    X = MediumAi(ttb, "X")
else:
    X = HardAi(ttb)

if O == "user":
    O = user(ttb)
elif O == "easy":
    O = EasyAi(ttb)
elif O == "medium":
    O = MediumAi(ttb, "O")
else:
    O = HardAi(ttb)

while True:
    if ttb.get_winner() == "X" or ttb.get_winner() == "O":
        print(f"{ttb.get_winner()} wins")
        break
    if ttb.get_state() == "DRAW":
        print("Draw")
        break
    if ttb.turnX:
        X.move()
    else:
        O.move()
