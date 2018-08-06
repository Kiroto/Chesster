import chesster
teibol = chesster.Table()
teibol.resettable()
teibol.filltable()

def options(usrin):
    if usrin == 'resetTable':
        teibol.resettable()
    elif usrin == 'fillTable':
        teibol.filltable()
    elif usrin == 'showTable':
        try:
            print()
            print(teibol.showtable())
            print()
            print('Table Shown')
        except:
            print('Something went wrong. Sorry bro!')
    elif usrin == 'changeTeam':
        if teibol.curteam:
            teibol.curteam = False
        else:
            teibol.curteam = True
    elif usrin[:4] == 'move':
        pass
        
    

while True: # Main loop
    usrin = str(input())
    if usrin == 'exit':
        break
    options(usrin)