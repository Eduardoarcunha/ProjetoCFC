import random

def randomCommands():
    Comands = []
    ComandsDic = {
            "COMAND1": b'\x00\xFF\x00\xFF',
            "COMAND2": b'\x00\xFF\xFF\x00',
            "COMAND3": b'\xFF',
            "COMAND4": b'\x00',
            "COMAND5": b'\xFF\x00',
            "COMAND6": b'\x00\xFF',
    }

    nComands = random.randint(10,30)

    for n in range(nComands):
        i = random.randint(1,6)
        Comands.append(ComandsDic['COMAND' + str(i)])

    return Comands, n

#print(randomCommands())