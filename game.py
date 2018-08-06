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
            print('You can move to: ' + str(movements))
            print('You can kill at: ' + str(assasinations))
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin[:4] == 'move':

        pass   

while True: # Main loop
    usrin = str(input())
    if usrin == 'exit':
        break
    options(usrin)