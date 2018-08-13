import copy

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

def multipostorc(poss):
    rcmove = []
    for i in poss:
        rcmove.append(postorc(i[0], i[1]))
    return rcmove

def multirctopos(rcs):
    posmove = []
    for i in rcs:
        posmove.append(rctopos(i))
    return posmove

class Table:
    def __init__(self, table=None, spectre=False, scale=8):
        if table == None:
            self.table = []
        else:
            self.table = table
        self.curteam = True
        self.capturedpieces = [[],[]]
        self.isSpectre = spectre
    
    def switchTeam(self):
        if self.curteam:
            self.curteam = False
        else:
            self.curteam = True

    def resettable(self):
        self.table = []
        for i in range(8):
            self.table.append([])
            for k in range(8):
                self.table[-1].append(Space(i, k))
    
    def filltable(self):
        self.curteam = True
        for i in range(len(self.table)):
            if i == 0:
                for k in range(len(self.table[i])):
                    if k == 0 or k == 7:
                        self.table[i][k] = Rook(k, i, False, False)
                    elif k == 1 or k == 6:
                        self.table[i][k] = Horse(k, i, False, False)
                    elif k == 2 or k == 5:
                        self.table[i][k] = Bishop(k, i, False, False)
                    elif k == 3:
                        self.table[i][k] = Queen(k, i, False, False)
                    else:
                        self.table[i][k] = King(k, i, False, False)

            elif i == 1:
                for k in range(len(self.table[i])):
                    self.table[i][k] = Peon(k, i, False, False)
            
            elif i == 6:
                for k in range(len(self.table[i])):
                    self.table[i][k] = Peon(k, i, True, False)

            elif i == 7:
                for k in range(len(self.table[i])):
                    if k == 0 or k == 7:
                        self.table[i][k] = Rook(k, i, True, False)
                    elif k == 1 or k == 6:
                        self.table[i][k] = Horse(k, i, True, False)
                    elif k == 2 or k == 5:
                        self.table[i][k] = Bishop(k, i, True, False)
                    elif k == 3:
                        self.table[i][k] = Queen(k, i, True, False)
                    else:
                        self.table[i][k] = King(k, i, True, False)

    def showtable(self):
        newtable = []
        for i in self.table:
            newtable.append([])
            for k in i:
                newtable[-1].append(k.icon)
        printtable = ''
        # printtable = '+' + '-+' * 7 + '-+\n'
        for i in range(len(newtable)):
            printtable += str((i+1)*-1 + 9) + '|'
            for k in range(len(newtable[i])):
                printtable += newtable[i][k] + ' '
            printtable += '\n'
        printtable += '-+---------------\n |A B C D E F G H'
            # printtable += '|\n+' + '-+' * 7 + '-+\n'
        return printtable
    
    def check(self):
        kings = 0
        anss = [False, False]
        def checkking(checklist, kingteam):
            if kingteam:
                checklist[0] = True
            else:
                checklist[1] = True
            return checklist
        
        for k in self.table:
            if kings == 2:
                break
            for i in k:
                if kings == 2:
                    break
                if not isinstance(i, King):
                    continue
                kings += 1
                kteam = i.team
                opposide = 2
                if kteam:
                   opposide = 8

                nearPeon = i.limitSide(self, opposide+1, 1)[1] + i.limitSide(self, opposide-1, 1)[1]
                spectreHorse = Horse(i.y, i.x, i.team, False)
                nearHorse = spectreHorse.availMoves(self)[1]

                for n in nearHorse:
                    lookedat = self.table[n[0]][n[1]]
                    if isinstance(lookedat, Horse) and kteam != lookedat.team:
                        checkking(anss, kteam)

                for n in nearPeon:
                    lookedat = self.table[n[0]][n[1]]
                    if isinstance(lookedat, Peon) and kteam != lookedat.team:
                        checkking(anss, kteam)
                    
                for k in range(1, 10):
                    directionKill = i.limitSide(self, k)[1]
                    for n in directionKill:
                        lookedat = self.table[n[0]][n[1]]
                        if k % 2 != 0:
                            if (isinstance(lookedat, Bishop) or isinstance(lookedat, Queen)) and kteam != lookedat.team:
                                checkking(anss, kteam)  
                        else:
                            if (isinstance(lookedat, Rook) or isinstance(lookedat, Queen)) and kteam != lookedat.team:
                                checkking(anss, kteam)
        return anss    
    
    def checkmate(self, team):
        if team:
            teamno = 1
        else:
            teamno = 0
        simultable = []
        for y in self.table:
            simultable.append([])
            for x in y:
                if isinstance(x, Peon):
                    simultable[-1].append(Peon(x.x, x.y, x.team, False))
                elif isinstance(x, Rook):
                    simultable[-1].append(Rook(x.x, x.y, x.team, False))
                elif isinstance(x, Horse):
                    simultable[-1].append(Horse(x.x, x.y, x.team, False))
                elif isinstance(x, Bishop):
                    simultable[-1].append(Bishop(x.x, x.y, x.team, False))
                elif isinstance(x, Queen):
                    simultable[-1].append(Queen(x.x, x.y, x.team, False))
                elif isinstance(x, King):
                    simultable[-1].append(King(x.x, x.y, x.team, False))
                else:
                    simultable[-1].append(Space(x.x, x.y))
        for y in simultable:
            for x in y:
                if x.team == team or x.team == None:
                    continue
                simulBoard = Table(simultable[:], True)
                for moves in x.availMoves(simulBoard)[0]:
                    simulBoard = Table(simultable[:], True)
                    x.move(simulBoard, moves[0], moves[1])
                    if not simulBoard.check()[teamno]:
                        print(str(x.kind) + ' to ' + postorc(x.y, x.x))
                        return False
                        
                for moves in x.availMoves(simulBoard)[1]:
                    simulBoard = Table(simultable[:], True)
                    x.move(simulBoard, moves[0], moves[1])
                    if not simulBoard.check()[teamno]:
                        print(str(x.kind) + ' to ' + postorc(x.y, x.x))
                        return False
        return True
                    
        
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

    def availMoves(self, board):
        return [], []
    
    def move(self, board, xpos, ypos):
        print("You can't move an empty space!")

    def descr(self, table=None):
        attribs = vars(self)
        ans = 'This is a(n) ' + self.kind + ', and thus it is represented by ' + self.icon + '.\n'
        if 'x' in attribs and 'y' in attribs:
            ans += ' It is located at ' + postorc(self.y, self.x) + '.'
        if self.team == None:
            ans += " It doesn't belong to a team."
        else:
            team = 'Black'
            if self.team:
                team = 'White'
            ans += " It belongs to the " + team + " team."
            # if table != None:
            #     moves, kills = self.availMoves(table)
            #     rcmove = []
            #     rckills = []
            #     for i in moves:
            #         rcmove.append(postorc(i[0], i[1]))
            #     for i in kills:
            #         rckills.append(postorc(i[0], i[1]))
            #     if rcmove != []:
            #         ans += ' It can move to ' + str(rcmove)[1:-1] + '.'
            #     if rckills != []:
            #         ans += ' It can kill at ' + str(rckills)[1:-1] + '.'
        return ans

class Piece(Space):
    """Represents a piece of either team"""
    def __init__(self, x, y, team, captured):
        Space.__init__(self, x, y)
        self.team = team
        self.captured = captured

    def die(self, board):
        self.captured = True
        if self.team:
            board.capturedpieces[0].append(self)
        else:
            board.capturedpieces[1].append(self)

    def availMoves(self, board):
        return [], []

    def move(self, board, ypos, xpos):
        table = board.table
        moves, kills = self.availMoves(board)
        
        if self.team == board.curteam:
            if (ypos, xpos) in moves:
                if isinstance(self, Peon) and (ypos in [0, 7]):
                    table[ypos][xpos] = Queen(ypos, xpos, self.team, self.captured)
                else:
                    table[ypos][xpos] = self
                table[self.y][self.x] = Space(self.y, self.x)
                self.x = xpos
                self.y = ypos
                board.switchTeam()
                
            elif (ypos, xpos) in kills:
                table[ypos][xpos].die(board)
                if isinstance(self, Peon) and (ypos in [0, 7]):
                    table[ypos][xpos] = Queen(ypos, xpos, self.team, self.captured)
                else:
                    table[ypos][xpos] = self
                table[self.y][self.x] = Space(self.y, self.x)
                self.x = xpos
                self.y = ypos
                board.switchTeam()

            if not board.isSpectre and board.check()[1]:
                print('Black in Check')
                if board.checkmate(False):
                    print('Checkmate')
            if not board.isSpectre and board.check()[0] == True:
                print('White in Check')
                if board.checkmate(False):
                    print('Checkmate')
        
        elif not board.isSpectre:
            if self.team:
                print("Not whites' turn.")
            else:
                print("Not blacks' turn.")
   

    def limitSide(self, board, side, speed=8):
        checkingpos = [self.y, self.x]
        spaces = []
        kills = []
        if isinstance(board, list):
            pass
        table = board.table

        def checkSpace(checkingpos, speed):
            speed += -1
            cont = True
            checkedspace = table[checkingpos[0]][checkingpos[1]]
            if checkedspace.team == None:
                spaces.append((checkedspace.y, checkedspace.x))
            elif checkedspace.team != self.team:
                kills.append((checkedspace.y, checkedspace.x))
                cont = False
            else:
                cont = False
            return cont, speed

        if side == 1:
            while checkingpos[0] < 7 and checkingpos[1] > 0 and speed > 0:
                checkingpos[0] += 1
                checkingpos[1] += -1
                cont, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 2:
            while checkingpos[0] < 7 and speed > 0:
                checkingpos[0] += 1
                cont, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 3:
            while checkingpos[0] < 7 and checkingpos[1] < 7 and speed > 0:
                checkingpos[0] += 1
                checkingpos[1] += 1
                cont, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 4:
            while checkingpos[1] > 0 and speed > 0:
                checkingpos[1] += -1
                cont, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 6:
            while checkingpos[1] < 7 and speed > 0:
                checkingpos[1] += 1
                cont, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 7:
            while checkingpos[0] > 0 and checkingpos[1] > 0 and speed > 0:
                checkingpos[0] += -1
                checkingpos[1] += -1
                cont, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break  

        elif side == 8:
            while checkingpos[0] > 0 and speed > 0:
                checkingpos[0] += -1
                cont, speed = checkSpace(checkingpos, speed)
                if not cont:
                    break

        elif side == 9:
            while checkingpos[0] > 0 and checkingpos[1] < 7 and speed > 0:
                checkingpos[0] += -1
                checkingpos[1] += 1
                cont, speed = checkSpace(checkingpos, speed)
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
            limitside = self.limitSide(board, side, 2)
            for k in limitside:
                moves.extend(k)
        elif self.y == 6 and self.team:
            limitside = self.limitSide(board, side, 2)
            for k in limitside:
                moves.extend(k)
        else:
            moves.extend(self.limitSide(board, side, 1)[0])
        kills.extend(self.limitSide(board, side+1, 1)[1])
        kills.extend(self.limitSide(board, side-1, 1)[1])

        # moves = multipostorc(moves)
        # kills = multipostorc(kills)

        return moves, kills

class Rook(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'r'
        if self.team:
            self.icon = 'R'
        self.kind = 'Rook'
    
    def availMoves(self, board):
        kills = []
        moves = []

        for i in range(1, 10):
            if i % 2 == 0:
                sidelimit = self.limitSide(board, i)
                moves.extend(sidelimit[0])
                kills.extend(sidelimit[1])

        return moves, kills         

class Horse(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'h'
        if self.team:
            self.icon = 'H'
        self.kind = 'Horse'        

    def availMoves(self, board):
        spaces = []
        kills = []

        def checkSpace(checkingpos):
            checkedspace = board.table[checkingpos[0]][checkingpos[1]]
            if checkedspace.team == None:
                spaces.append((checkedspace.y, checkedspace.x))
            elif checkedspace.team != self.team:
                kills.append((checkedspace.y, checkedspace.x))
        
        if self.y <= 5:
            if self.x >= 1:
                checkSpace([self.y +2, self.x-1])
            if self.x <= 6:
                checkSpace([self.y +2, self.x+1])
        
        if self.y >= 2:    
            if self.x >= 1:
                checkSpace([self.y -2, self.x-1])
            if self.x <= 6:
                checkSpace([self.y -2, self.x+1])
        
        if self.x <= 5:
            if self.y >= 1:
                checkSpace([self.y - 1, self.x + 2])
            if self.y <= 6:
                checkSpace([self.y + 1, self.x + 2])
        
        if self.x >= 2:    
            if self.y >= 1:
                checkSpace([self.y - 1, self.x-2])
            if self.y <= 6:
                checkSpace([self.y + 1, self.x-2])

        return spaces, kills         

class Bishop(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'b'
        if self.team:
            self.icon = 'B'
        self.kind = 'Bishop'

    def availMoves(self, board):
        kills = []
        moves = []

        for i in range(1, 10):
            if i % 2 != 0:
                sidelimit = self.limitSide(board, i)
                moves.extend(sidelimit[0])
                kills.extend(sidelimit[1])

        return moves, kills

class King(Piece):
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'k'
        if self.team:
            self.icon = 'K'
        self.kind = 'King'

    def availMoves(self, board):
        kills = []
        moves = []

        for i in range(1, 10):
            sidelimit = self.limitSide(board, i, 1)
            moves.extend(sidelimit[0])
            kills.extend(sidelimit[1])

        return moves, kills

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
            if sidelimit[0] not in moves or sidelimit[1] not in kills:
                moves.extend(sidelimit[0])
                kills.extend(sidelimit[1])

        return moves, kills         
