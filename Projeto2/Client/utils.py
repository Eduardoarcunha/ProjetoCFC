import random

def randomCommands():
    Comands = []
    ComandsDic = {
            "COMAND1": [b'\x00\xFF\x00\xFF',4],
            "COMAND2": [b'\x00\xFF\xFF\x00',4],
            "COMAND3": [b'\xFF',1],
            "COMAND4": [b'\x00',1],
            "COMAND5": [b'\xFF\x00',2],
            "COMAND6": [b'\x00\xFF',2],
    }

    nComands = random.randint(10,30)

    for n in range(nComands):
        i = random.randint(1,6)
        Comands.append(ComandsDic['COMAND' + str(i)])

    return Comands, n

