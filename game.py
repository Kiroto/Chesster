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
        except:
            print('Something went wrong. Sorry bro!')
    elif usrin == 'fillTable':
        try:
            teibol.filltable()
            print()
            print('Table Filled!')
        except:
            print('Something went wrong. Sorry bro!')
    elif usrin == 'showTable':
        try:
            print()
            print(teibol.showtable())
            print()
            print('Table Shown!')
        except:
            print('Something went wrong. Sorry bro!')
    elif usrin == 'changeTeam':
        try:
            if teibol.curteam:
                teibol.curteam = False
            else:
                teibol.curteam = True
            print('Team Changed!')
        except:
            print('Something went wrong. Sorry bro!')
    elif usrin[:5] == 'moves': # Ex input: moves A2
        try:
            print()
            frompos = chesster.rctopos(usrin[6:8])
            movements, assasinations = teibol.table[frompos[0]][frompos[1]].availMoves(teibol.table)
            print('You can move to: ' + movements)
            print('You can kill at: ' + assasinations)
        except:
            print('Something went wrong. Sorry bro!')
    elif usrin[:4] == 'move':

        pass   

while True: # Main loop
    usrin = str(input())
    if usrin == 'exit':
        break
    options(usrin)