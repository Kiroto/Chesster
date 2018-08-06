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
    elif usrin[:4] == 'move':
        pass   

while True: # Main loop
    usrin = str(input())
    if usrin == 'exit':
        break
    options(usrin)