import chesster
teibol = chesster.Table()
teibol.resettable()
teibol.filltable()
commands = [['Reset Table', 'resetTable', 'reset table', 'rt'],\
            ['what is', 'describ', 'What is'],\
            ['moves', 'moovs', 'Moves', 'ms'],\
            ['move', 'moov', 'Move', 'm'],\
            ['help', 'Help', 'h']]
def options(usrin):
    """Lists all the interactions from the user with the game"""
    if usrin in commands[0]: # Resets the table
        try:
            teibol.resettable()
            teibol.filltable()
            print('Table Reset!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin in commands[4]: # Lists the help
        print('\nYou may issue the commands (or exit):\n > reset table | sets the table back to the beggining of the game.\
                                            \n > what is X#  | shows information about a tile.\
                                            \n > moves X#    | shows available moves for a piece.\
                                            \n > move X# X#  | moves a piece, if it can move to that tile.\
                                            \n > help        | shows this information.\
                                            ')
    elif usrin[:7] in commands[1] or usrin[:usrin.find(' ')] in commands[1]: # Describes a piece
        try:
            print()
            place = usrin[8:]
            froy, frox = chesster.rctopos(place)
            print(teibol.table[froy][frox].descr(teibol))
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin[:usrin.find(' ')] in commands[2]: # Shows a piece's mossible moves
        print()
        place = usrin[6:]
        froy, frox = chesster.rctopos(place)
        movements, assasinations = teibol.table[froy][frox].availMoves(teibol)
        print('It can move to: ' + str(chesster.multipostorc(movements))[1:-1])
        print('It can kill at: ' + str(chesster.multipostorc(assasinations))[1:-1])
    elif usrin[:usrin.find(' ')] in commands[3]: # moves a piece
        try:
            spacePos = usrin.find(' ')
            piece = chesster.rctopos(usrin[spacePos+1:spacePos+3])
            spot = chesster.rctopos(usrin[spacePos+4:spacePos+6])
            teibol.table[piece[0]][piece[1]].move(teibol, spot[0], spot[1])
        except KeyError as e:
            print('Correct usage: move L# L#, where L is a letter between A and H and # is a number between 1 and 8.\n' + str(e) + ' is not recognized.')
        except IndexError as e:
            print('Did you write the position you want to move to?')
    print(teibol.showtable())
    if teibol.curteam:
        print("White pieces' turn")
    else:
        print("Black pieces' turn")

options('help')
while True: # Main loop, the program takes place here.
    print('You may now insert your next command (or help).')
    usrin = str(input())
    if usrin == 'exit':
        break
    options(usrin)