from pprint import pprint

def rctopos(rc): # Row Column
    columnID = {'a': 0, 'b': 1, 'c': 2, 'd':3, 'e':4, 'f': 5, 'g': 6, 'h': 7,\
        'A': 0, 'B': 1, 'C': 2, 'D':3, 'E':4, 'F': 5, 'G': 6, 'H': 7}
    rowID = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    xpos = columnID[rc[0]]
    ypos = rowID[rc[1]]
    return ypos, xpos

def postorc(posy, posx):
    posyID = {7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8'}
    posxID = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    return posxID[posx] + posyID[posy]

class Table:
    def __init__(self, scale=8):
        self.table = []
        self.curteam = True
    
    def resettable(self):
        self.table = []
        for i in range(8):
            self.table.append([])
            for k in range(8):
                self.table[-1].append(Space(k, i))
    
    def filltable(self):
        for i in range(len(self.table)):
            if i == 0:
                for k in range(len(self.table[i])):
                    if k == 0 or k == 7:
                        self.table[i][k] = Rook(i, k, False, False)
                    elif k == 1 or k == 6:
                        self.table[i][k] = Horse(i, k, False, False)
                    elif k == 2 or k == 5:
                        self.table[i][k] = Bishop(i, k, False, False)
                    elif k == 3:
                        self.table[i][k] = Queen(i, k, False, False)
                    else:
                        self.table[i][k] = King(i, k, False, False)

            elif i == 1:
                for k in range(len(self.table[i])):
                    self.table[i][k] = Peon(i, k, False, False)
            
            elif i == 6:
                for k in range(len(self.table[i])):
                    self.table[i][k] = Peon(i, k, True, False)

            elif i == 7:
                for k in range(len(self.table[i])):
                    if k == 0 or k == 7:
                        self.table[i][k] = Rook(i, k, True, False)
                    elif k == 1 or k == 6:
                        self.table[i][k] = Horse(i, k, True, False)
                    elif k == 2 or k == 5:
                        self.table[i][k] = Bishop(i, k, True, False)
                    elif k == 3:
                        self.table[i][k] = Queen(i, k, True, False)
                    else:
                        self.table[i][k] = King(i, k, True, False)

    def showtable(self):
        newtable = []
        for i in self.table:
            newtable.append([])
            for k in i:
                newtable[-1].append(k.icon)
        printtable = ''
        # printtable = '+' + '-+' * 7 + '-+\n'
        for i in range(len(newtable)):
            for k in range(len(newtable[i])):
                # printtable += '|'
                printtable += newtable[i][k]
            printtable += '\n'
            # printtable += '|\n+' + '-+' * 7 + '-+\n'
        return printtable
        
class Space:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if (x+1) % 2 == (y+1) % 2:
            self.icon = '.'
        else:
            self.icon = '#'
        self.team = None
        self.kind = 'Empty'

    def descr(self):
        attribs = vars(self)
        ans = 'This is a(n) ' + self.kind + ', and thus it is represented by ' + self.icon + '.\n'
        if 'x' in attribs and 'y' in attribs:
            ans += ' It is located at ' + postorc(self.y, self.x) + '.'
        if self.team != None:
            ans += " It doesn't belong to a team."
        else:
            team = 'Black'
            if self.team:
                team = 'White'
            ans += " It belongs to the " + team + " team."

class Piece(Space):
    """Represents a piece of either team"""
    def __init__(self, x, y, team, captured):
        Space.__init__(self, x, y)
        self.team = team
        self.captured = captured

    def die(self):
        self.captured = True
        self.team = None
        if (self.x+1) % 2 == (self.y+1) % 2:
            self.icon = '#'
        else:
            self.icon = '.'

    def limitSide(self, board, side, speed=8):
        checkingpos = [self.y, self.x]
        spaces = []
        kills = []

        def checkSpace(checkingpos, speed):
            speed += -1
            cont = True
            checkedspace = board[checkingpos[0]][checkingpos[1]]
            if checkedspace.team == None:
                spaces.append((checkedspace.y, checkedspace.x))
            elif checkedspace.team != self.team:
                kills.append((checkedspace.y, checkedspace.x))
                cont = False
            else:
                cont = False
            return cont, spaces, kills, speed
            
        if side == 8:
            while checkingpos[0] > 0 and speed > 0:
                checkingpos[0] += -1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 9:
            while checkingpos[0] > 0 and checkingpos[1] < 7 and speed > 0:
                checkingpos[0] += -1
                checkingpos[1] += 1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 1:
            while checkingpos[0] < 7 and checkingpos[1] > 0 and speed > 0:
                checkingpos[0] += 1
                checkingpos[1] += -1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 2:
            while checkingpos[0] < 7 and speed > 0:
                checkingpos[0] += 1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 3:
            while checkingpos[0] < 7 and checkingpos[1] < 7 and speed > 0:
                checkingpos[0] += 1
                checkingpos[1] += 1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 4:
            while checkingpos[1] > 0 and speed > 0:
                checkingpos[1] += -1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 6:
            while checkingpos[1] < 7 and speed > 0:
                checkingpos[1] += 1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 7:
            while checkingpos[0] > 0 and checkingpos[1] > 0 and speed > 0:
                checkingpos[0] += -1
                checkingpos[1] += -1
                cont, spaces, kills, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        return spaces, kills

class Peon(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.kind = 'Peon'
        self.icon = 'p'
        if self.team:
            self.icon = 'P'
    
    def availMoves(self, board):
        kills = []
        moves = []
        if self.team:
            side = 8
        else: 
            side = 2
        if self.y == 1 and not self.team:
            moves.append((self.y+2, self.x))
        elif self.y == 6 and self.team:
            moves.append((self.y-2, self.x))
        moves.extend(self.limitSide(board, side, 1)[0])
        kills.extend(self.limitSide(board, side+1, 1)[1])
        kills.extend(self.limitSide(board, side-1, 1)[1])

        return moves, kills
    
    def move(self, board, ypos, xpos):
        moves, kills = self.availMoves(board)
        if (ypos, xpos) in moves or (xpos, ypos) in kills:
            board[ypos][xpos] = self
            board[self.y][self.x] = Space(self.x, self.y)
            self.x = xpos
            self.y = ypos
            
        elif (ypos, xpos) in kills:
            board[ypos][xpos].die()
            self.x = xpos
            self.y = ypos

class Rook(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'r'
        if self.team:
            self.icon = 'R'
        self.kind = 'Rook'

class Horse(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'h'
        if self.team:
            self.icon = 'H'
        self.kind = 'Horse'

class Bishop(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'b'
        if self.team:
            self.icon = 'B'
        self.kind = 'Bishop'

class King(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'k'
        if self.team:
            self.icon = 'K'
        self.kind = 'King'

class Queen(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'q'
        if self.team:
            self.icon = 'Q'
            self.kind = 'Queen'

    def availMoves(self, board):
        kills = []
        moves = []

        for i in range(1, 10):
            sidelimit = self.limitSide(board, i)
            moves.extend(sidelimit[0])
            kills.extend(sidelimit[1])

        return moves, kills

    def move(self, board, ypos, xpos):
        moves, kills = self.availMoves(board)
        if (ypos, xpos) in moves or (xpos, ypos) in kills:
            board[ypos][xpos] = self
            board[self.y][self.x] = Space(self.x, self.y)
            self.x = xpos
            self.y = ypos
            
        elif (ypos, xpos) in kills:
            board[ypos][xpos].die()
            self.x = xpos
            self.y = ypos           

# teibol.resettable()
# teibol.filltable()
# print(teibol.showtable())
# teibol.table[1][1].move(teibol.table, 2, 1)
# print(teibol.showtable())
# teibol.table[3][1].descr()
