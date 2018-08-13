import chesster
teibol = chesster.Table()
teibol.resettable()
teibol.filltable()
commands = [['Reset Table', 'resetTable', 'reset table', 'rt'],\
            ['Fill Table', 'fill table', 'fillTable', 'ft'],\
            ['startup', 'su'],\
            ['showTable', 'Show Table', 'show table', 'st'],\
            ['changeTeam', 'change team', 'Change Team', 'ct'],\
            ['what is', 'describ', 'What is'],\
            ['moves', 'moovs', 'Moves', 'ms'],\
            ['move', 'moov', 'Move', 'm'],\
            ['help', 'Help', 'h'],\
            ['quickeat'],\
            ['quickcheck']]
def options(usrin):
    if usrin in commands[0]:
        try:
            teibol.resettable()
            print()
            print('Table Reset!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin in commands[8]:
        print()
        print('You may issue the commands:')
        print(commands)
        print()
    elif usrin in commands[1]:
        try:
            teibol.filltable()
            print()
            print('Table Filled!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin in commands[2]:
        try:
            teibol.resettable()
            teibol.filltable()
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin in commands[3]:
        try:
            print()
            print(teibol.showtable())
            print()
            print('Table Shown!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin in commands[4]:
        try:
            teibol.switchTeam()
            print('Team Changed!')
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin[:7] in commands[5] or usrin[:usrin.find(' ')] in commands[5]:
        try:
            print()
            place = usrin[8:]
            froy, frox = chesster.rctopos(place)
            print(teibol.table[froy][frox].descr(teibol))
        except Exception as e:
            print('Something went wrong. Sorry bro!')
            print(str(e))
    elif usrin[:usrin.find(' ')] in commands[6]: # Ex input: moves A2
        # try:
        print()
        place = usrin[6:]
        froy, frox = chesster.rctopos(place)
        movements, assasinations = teibol.table[froy][frox].availMoves(teibol)
        print('It can move to: ' + str(chesster.multipostorc(movements))[1:-1])
        print('It can kill at: ' + str(chesster.multipostorc(assasinations))[1:-1])
        # except Exception as e:
        #     pass
            # print('Something went wrong. Sorry bro!')
            # print(str(e))
    elif usrin[:usrin.find(' ')] in commands[7]: # move A2 A4
        try:
            spacePos = usrin.find(' ')
            piece = chesster.rctopos(usrin[spacePos+1:spacePos+3])
            spot = chesster.rctopos(usrin[spacePos+4:spacePos+6])
            teibol.table[piece[0]][piece[1]].move(teibol, spot[0], spot[1])
        except KeyError as e:
            print('Correct usage: move L# L#, where L is a letter between A and H and # is a number between 1 and 8.\n' + str(e) + ' is not recognized.')
        except IndexError as e:
            print('Did you write the position you want to move to?')
    elif usrin in commands[9]:
        options('move c2 c3')
        options('move e7 e6')
        options('move d1 a4')
        options('move a7 a6')
        options('move a4 a6')
    elif usrin in commands[10]:
        options('move c2 c3')
        options('move d7 d6')
        options('move d1 a4')
    print(teibol.showtable())
    if teibol.curteam:
        print("White pieces' turn")
    else:
        print("Black pieces' turn")

options('help')
while True: # Main loop
    print('You may now insert your next command (or help).')
    usrin = str(input())
    if usrin == 'exit':
        break
    options(usrin)