import copy

def rctopos(rc): # Transforms Row Column (rc) notation to Pos (y, x) notation.
    columnID = {'a': 0, 'b': 1, 'c': 2, 'd':3, 'e':4, 'f': 5, 'g': 6, 'h': 7,\
        'A': 0, 'B': 1, 'C': 2, 'D':3, 'E':4, 'F': 5, 'G': 6, 'H': 7}
    rowID = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    xpos = columnID[rc[0]]
    ypos = rowID[rc[1]]
    return ypos, xpos

def postorc(posy, posx): # Transforms Position (posy, posx) notation to RC (X#) notation.
    posyID = {7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8'}
    posxID = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    return posxID[posx] + posyID[posy]

def multipostorc(poss): # Transforms many Position [(y, x), ...] notation to many RC [(X#), ...] notation.
    rcmove = []
    for i in poss:
        rcmove.append(postorc(i[0], i[1]))
    return rcmove

def multirctopos(rcs): # Transforms many Row Column ['X#', ...] notation to many Pos [(posy, posx), ...] notation.
    posmove = []
    for i in rcs:
        posmove.append(rctopos(i))
    return posmove

class Table:
    """Represents a chess Table.
    Has a chess board (referred to as table)
    Keeps track of the current team (referred to as curteam)
    > When curteam is True, it's the whites' turn.
    > This is true for all pieces.
    > The white team is the one on the bottom side.
    Keeps track of captured pieces"""
    def __init__(self, table=None):
        """Creates the Table object.
        Can have preset tables inputed."""
        if table == None:
            self.table = []
        else:
            self.table = table
        self.curteam = True # Current team. If True, it's white team's turn.
        self.capturedpieces = [[],[]]
    
    def switchTeam(self):
        """Switches the current playing side."""
        if self.curteam:
            self.curteam = False
        else:
            self.curteam = True

    def resettable(self):
        """Clears the board and fills it with empty spaces."""
        self.table = []
        for i in range(8):
            self.table.append([])
            for k in range(8):
                self.table[-1].append(Space(i, k))
    
    def filltable(self):
        """Fills the current board with the default layout of pieces.
        Starts with the white team."""
        self.curteam = True
        for i in range(len(self.table)):
            if i == 0: # If it's the first row
                for k in range(len(self.table[i])): # Add pieces to the row
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

            elif i == 1: # Second row
                for k in range(len(self.table[i])):
                    self.table[i][k] = Peon(i, k, False, False)
            
            elif i == 6: # Seventh row
                for k in range(len(self.table[i])):
                    self.table[i][k] = Peon(i, k, True, False)

            elif i == 7: # Eigth row
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
        """Shows the table in it's current state.
        Uses piece icons.
        Represents positions and colored spaces."""
        newtable = []
        for i in self.table:
            newtable.append([])
            for k in i:
                newtable[-1].append(k.icon) # Gets all the icons and store them.
        printtable = '' # Represents the table to be printed
        for i in range(len(newtable)):
            printtable += str((i+1)*-1 + 9) + '|' # Add the current row's number and a dividing line
            for k in range(len(newtable[i])):
                printtable += newtable[i][k] + ' ' # Add the icon of that position and an empty space
            printtable += '\n'
        printtable += '-+---------------\n |A B C D E F G H' # Add the column letters

        return printtable
    
    def check(self):
        """Checks wether or not the king is in check"""
        kings = 0 # Count the kings you've found
        anss = [False, False] # [White king in check?, Black king in check?]
        def checkking(checklist, kingteam): # Quickly update a king's in-check status.
            if kingteam:
                checklist[1] = True
            else:
                checklist[0] = True
            return checklist
        
        for k in self.table:
            if kings == 2: # Stop if you've found both kings
                break
            for i in k:
                if kings == 2: # Stop if you've found both kings
                    break
                if not isinstance(i, King): # If you didn't find a king, do nothing.
                    continue
                kings += 1
                kteam = i.team # The king's team is the team of the piece we're checking.
                opposide = 2 # Opposite side. Check your numpad.
                if kteam:
                   opposide = 8

                nearPeon = i.limitSide(self, opposide+1, 1)[1] + i.limitSide(self, opposide-1, 1)[1] # Checks if there is a peon nearby
                spectreHorse = Horse(i.y, i.x, i.team, False) # Makes a false horse to test for it's moves
                nearHorse = spectreHorse.availMoves(self)[1]

                # lookedat refers to the piece being examined

                for n in nearHorse: # Check if there is a horse nearby
                    lookedat = self.table[n[0]][n[1]]
                    if isinstance(lookedat, Horse) and kteam != lookedat.team:
                        checkking(anss, kteam)

                for n in nearPeon: # Check if there is a peon nearby
                    lookedat = self.table[n[0]][n[1]]
                    if isinstance(lookedat, Peon) and kteam != lookedat.team:
                        checkking(anss, kteam)
                    
                for k in range(1, 10): # Check for the rest of the pieces
                    directionKill = i.limitSide(self, k)[1]
                    for n in directionKill:
                        lookedat = self.table[n[0]][n[1]]
                        if k % 2 != 0: # If it's a diagonal moving piece, make sure it's a queen or a bishop and that it's of the opposite team
                            if (isinstance(lookedat, Bishop) or isinstance(lookedat, Queen)) and kteam != lookedat.team:
                                checkking(anss, kteam)  
                        else: # Else make sure it's a queen or a rook and that it's of the opposite team
                            if (isinstance(lookedat, Rook) or isinstance(lookedat, Queen)) and kteam != lookedat.team:
                                checkking(anss, kteam)
        return anss     

class Space:
    """Defines an empty space.
    Keeps track of it's position y and x.
    Keeps track of it's own team (team).
    Has an icon (icon).
    Has a string representation."""
    def __init__(self, y, x):
        self.x = x
        self.y = y
        if (x+1) % 2 == (y+1) % 2:
            self.icon = '.'
        else:
            self.icon = '#'
        self.team = None
        self.kind = 'Empty'

    def availMoves(self, board):
        """Available moves of an empty space"""
        return [], []
    
    def move(self, board, xpos, ypos):
        print("You can't move an empty space!")

    def descr(self, table=None):
        """Gives a piece description, for all pieces."""
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
        return ans

class Piece(Space):
    """Represents a piece of either team.
    + Has a team.
    + Can be captured."""
    def __init__(self, x, y, team, captured):
        Space.__init__(self, x, y)
        self.team = team
        self.captured = captured

    def die(self, board):
        """The piece becomes captured"""
        self.captured = True
        if self.team:
            board.capturedpieces[0].append(self)
        else:
            board.capturedpieces[1].append(self)

    def move(self, board, ypos, xpos):
        """Moves the piece.
        If movement to-try is on the available moves, it can move.
        If the move is a kill, it captures the piece that is in the position to move.
        Switches teams after a sucessful move.
        If a peon reaches the final line, transform into a queen.
        Checks if a team is in check."""
        table = board.table
        moves, kills = self.availMoves(board)
        
        if self.team == board.curteam: # Check if the piece's team is the current team's
            if (ypos, xpos) in moves: # Check if the move is a move, not a kill
                if isinstance(self, Peon) and (ypos in [0, 7]):
                    table[ypos][xpos] = Queen(ypos, xpos, self.team, self.captured)
                else:
                    table[ypos][xpos] = self
                table[self.y][self.x] = Space(self.y, self.x)
                self.x = xpos
                self.y = ypos
                board.switchTeam()
                
            elif (ypos, xpos) in kills: # Check if the move is a kill
                table[ypos][xpos].die(board)
                if isinstance(self, Peon) and (ypos in [0, 7]):
                    table[ypos][xpos] = Queen(ypos, xpos, self.team, self.captured)
                else:
                    table[ypos][xpos] = self
                table[self.y][self.x] = Space(self.y, self.x)
                self.x = xpos
                self.y = ypos
                board.switchTeam()

            if board.check()[1]:
                print('Black in Check')
            elif board.check()[0] == True:
                print('White in Check')
        
        else:
            if self.team:
                print("Not whites' turn.")
            else:
                print("Not blacks' turn.")
   

    def limitSide(self, board, side, speed=8):
        """Lists all the moves towards a side, determined by the numpad position.
        Speed is how far a piece can go in the direction.
        (2 is south, 6 is east)"""
        checkingpos = [self.y, self.x] # Currently checked position.
        spaces = [] # Available empty spaces you can move to.
        kills = [] # Available spaces you can kill at.
        table = board.table

        def checkSpace(checkingpos, speed): # Check the selected space and reduce the speed. Append to the method variable if can move or kill. Stop on a wall or ally.
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
        # Check all sides
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
    """Represents a peon of a team.
    + Has available moves with peon rules."""
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.kind = 'Peon'
        self.icon = 'p' # Lowercase pieces are black
        if self.team:
            self.icon = 'P' # Uppercase pieces are white
    
    def availMoves(self, board):
        kills = []
        moves = []
        if self.team: # If on the white team, it moves to the north, 8.
            side = 8
        else: # Else it moves to the south, 2
            side = 2
        if self.y == 1 and not self.team: # If black's first move, can move twice
            limitside = self.limitSide(board, side, 2)
            for k in limitside:
                moves.extend(k)
        elif self.y == 6 and self.team: # If whites' first move, can move twice
            limitside = self.limitSide(board, side, 2)
            for k in limitside:
                moves.extend(k)
        else:
            moves.extend(self.limitSide(board, side, 1)[0])
        kills.extend(self.limitSide(board, side+1, 1)[1]) # Check both sides
        kills.extend(self.limitSide(board, side-1, 1)[1]) # And look for a kill

        # moves = multipostorc(moves)
        # kills = multipostorc(kills)

        return moves, kills

class Rook(Piece):
    """Represents a rook of a team.
    + Has available moves with rook rules."""
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
            if i % 2 == 0: # If not a diagonal
                sidelimit = self.limitSide(board, i) 
                moves.extend(sidelimit[0]) # Add the moves found in a straight line
                kills.extend(sidelimit[1]) # Add the kills found in a straight line

        return moves, kills         

class Horse(Piece):
    """Represents a horse (knight) of a team.
    + Has available moves with horse (knight) rules."""
    def __init__(self, x, y, team, captured):
        Piece.__init__(self, x, y, team, captured)
        self.icon = 'h'
        if self.team:
            self.icon = 'H'
        self.kind = 'Horse'        

    def availMoves(self, board):
        spaces = []
        kills = []

        def checkSpace(checkingpos): # Check the space selected
            checkedspace = board.table[checkingpos[0]][checkingpos[1]]
            if checkedspace.team == None:
                spaces.append((checkedspace.y, checkedspace.x))
            elif checkedspace.team != self.team:
                kills.append((checkedspace.y, checkedspace.x))
        # Horse's moving rules.
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
    """Represents a bishop of a team.
    + Has available moves with bishop rules."""
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
            if i % 2 != 0: # If the move would be diagonal
                sidelimit = self.limitSide(board, i)
                moves.extend(sidelimit[0]) # Add the moves found in the diagonal
                kills.extend(sidelimit[1]) # Add the kills found in the diagonal

        return moves, kills

class King(Piece):
    """Represents a king of a team.
    + Has available moves with king rules."""
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
            sidelimit = self.limitSide(board, i, 1) # Check all sides and add them to the move/kills
            moves.extend(sidelimit[0])
            kills.extend(sidelimit[1])

        return moves, kills

class Queen(Piece):
    """Represents a queen of a team.
    + Has available moves with queen rules."""
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
            sidelimit = self.limitSide(board, i) # Check all sides and add them to the move/kills
            moves.extend(sidelimit[0])
            kills.extend(sidelimit[1])

        return moves, kills         
