import random

def randomCommands():
    Comands = []
    ComandsDic = {
            "COMAND1": "00 FF 00 FF",
            "COMAND2": "00 FF FF 00",
            "COMAND3": "FF",
            "COMAND4": "00",
            "COMAND5": "FF 00",
            "COMAND6": "00 FF",
    }

    nComands = random.randint(10,30)

    for n in range(nComands):
        i = random.randint(1,6)
        Comands.append(ComandsDic['COMAND' + i])

    return Comands