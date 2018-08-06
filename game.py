import chesster
teibol = chesster.Table()
teibol.resettable()
teibol.filltable()

def options(usrin):
    if usrin == 'resetTable':
        try:
            teibol.resettable()
            print()
            print('Table Reset!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin == 'help':
        print()
        print('You may issue the commands:')
        print('resetTable, fillTable, startup, showTable, changeTeam')
        print('what is (piece), moves (piece), move (piece) (place)')
        print()
    elif usrin == 'fillTable':
        try:
            teibol.filltable()
            print()
            print('Table Filled!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin == 'startup':
        try:
            teibol.resettable()
            teibol.filltable()
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin == 'showTable':
        try:
            print()
            print(teibol.showtable())
            print()
            print('Table Shown!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin == 'changeTeam':
        try:
            if teibol.curteam:
                teibol.curteam = False
            else:
                teibol.curteam = True
            print('Team Changed!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin[:7] == 'what is':
        try:
            print()
            place = usrin[8:]
            froy, frox = chesster.rctopos(place)
            print(teibol.table[froy][frox].descr(teibol))
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin[:5] == 'moves': # Ex input: moves A2
        try:
            print()
            place = usrin[6:]
            froy, frox = chesster.rctopos(place)
            movements, assasinations = teibol.table[froy][frox].availMoves(teibol.table)
            print('It can move to: ' + str(chesster.multipostorc(movements)[1:-1]))
            print('It can kill at: ' + str(chesster.multipostorc(assasinations)[1:-1]))
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin[:4] == 'move': # move A2 A4
        piece = chesster.rctopos(usrin[5:7])
        spot = chesster.rctopos(usrin[8:])
        teibol.table[piece[0]][piece[1]].move(teibol.table, spot[0], spot[1])
        print(teibol.showtable())

options('help')
while True: # Main loop
    print('You may now insert your next command (or help).')
    usrin = str(input())
    if usrin == 'exit':
        break
    options(usrin)