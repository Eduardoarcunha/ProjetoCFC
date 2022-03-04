import random
import time
import numpy as np

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
        #print(ComandsDic['COMAND' + str(i)])

    ComandsArray = bytearray(b'')

    for n in range(nComands):
        ComandsArray.append(Comands[n][1])
        ComandsArray.extend(Comands[n][0])

    ComandsArray.extend(b'\xff')

    return ComandsArray, n + 1

def sendSacrifice(com1):
    time.sleep(.3)
    com1.sendData(b'00')
    time.sleep(.3)
    return

def receiveSacrifice(com1):
    rxBuffer, nRx = com1.getData(1)
    com1.rx.clearBuffer()
    time.sleep(.1)

    return rxBuffer, nRx

def createPackages(message):

    packages = []

    #Numero de pacotes
    numberOfPackages = len(message) // 114
    if len(message) % 114 > 0:
        numberOfPackages += 1

    numberOfPackagesB = numberOfPackages.to_bytes(1,byteorder='big')
    nPackage = 0

    #Creating packages
    while len(message) > 0:

        nPackageB = nPackage.to_bytes(1, byteorder='big')

        payload = message[0:114]
        message = message[114:]

        payloadSize = (len(payload)).to_bytes(1,byteorder='big')

        head = numberOfPackagesB + nPackageB + payloadSize + b'\x00\x00\x00\x00\x00\x00\x00'
        eop = b'\x00\x00\x00\x00'
        

        package = head + payload + eop

        packages.append(package)
        nPackage += 1

    return packages, numberOfPackages


#packages, nPackage = createPackages(cr7)