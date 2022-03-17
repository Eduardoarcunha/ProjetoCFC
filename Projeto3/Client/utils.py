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

def createPackages(message, falseIndex = False, falsePayload = False, falseEOP = False):

    packages = []

    #Numero de pacotes
    numberOfPackages = len(message) // 114
    if len(message) % 114 > 0:
        numberOfPackages += 1

    #numero de pacotes em bytes
    numberOfPackagesB = numberOfPackages.to_bytes(1,byteorder='big')
    
    #Pacote atual
    nPackage = 0

    if falseIndex or falsePayload or falseEOP:
        errorIndex = np.random.randint(1,numberOfPackages - 1)
        print('O erro acontecerá no pacote {}\n'.format(errorIndex + 1))
    else:
        errorIndex = 0

    #Creating packages
    while len(message) > 0:
        nPackageB = nPackage.to_bytes(1, byteorder='big')
        
        payload = message[0:114]
        message = message[114:]

        #Força um erro no tamanho do Payload se pedido
        if falsePayload and nPackage == errorIndex:
            payloadSize = (len(payload) - 3).to_bytes(1,byteorder='big')
        else:
            payloadSize = (len(payload)).to_bytes(1,byteorder='big')


        #Força um erro no Index do pacote se necessário
        if falseIndex and nPackage == errorIndex:
            head = numberOfPackagesB +  (1).to_bytes(1, byteorder='big') + payloadSize + b'\x00\x00\x00\x00\x00\x00\x00'
        else:
            head = numberOfPackagesB + nPackageB + payloadSize + b'\x00\x00\x00\x00\x00\x00\x00'

        #Forca um erro no EOP se necessário
        if falseEOP and nPackage == errorIndex:
            eop = b'\x10\x30\x04\x20'
        else:
            eop = b'\x00\x00\x00\x00'
        
        package = head + payload + eop

        packages.append(package)
        nPackage += 1

    return packages, numberOfPackages


print(40/3)