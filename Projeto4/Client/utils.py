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

def createPackages(type, message = None):

    #Lista com os pacotes que serão retornados
    packages = []

    #Constantes
    #Id server
    h1 = b'\x80'
    h2 = b'\x00'
    h6 = b'\x00'
    h7 = b'\x00'
    h8 = b'\x00'
    h9 = b'\x00'

    eop = b'\xAA\xBB\xCC\xDD'


    if type == 'transmission':
        #Numero de pacotes caso tenha mensagem
        numberOfPackages = len(message) // 114

        if len(message) % 114 > 0:
            numberOfPackages += 1

    else:
        numberOfPackages = 1

    #Numero de pacotes em bytes, quantidade de pacotes do arquivo + 1 do handshake
    numberOfPackagesB = ((numberOfPackages + 1).to_bytes(1,byteorder='big') )
    
    #Pacote atual
    nPackage = 0


    if type == 'transmission':
    #Creating packages
        while len(message) > 0:   
            nPackageB = nPackage.to_bytes(1, byteorder='big')

            if nPackage == 0:
                h0 = b'\x01'
                h5 = b'\x00'
            else:
                h0 = b'\x03'

                #A mensagem terá payload
                payload = message[0:114]
                message = message[114:]
                payloadSize = (len(payload)).to_bytes(1,byteorder='big')

                h5 = payloadSize


            h3 = numberOfPackagesB
            h4 = nPackageB

            head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        
            if nPackage == 0:
                package = head + eop
            else:
                package = head + payload + eop

            packages.append(package)
            nPackage += 1

    elif type == 'timeout':

        h0 = b'\x05'
        h1 = b'\x80'
        h2 = b'\x00'
        h3 = b'\x00'
        h4 = b'\x00'
        h5 = b'\x00'
        h6 = b'\x00'
        h7 = h7
        h8 = b'\x00'
        h9 = b'\x00'

        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        package = head + eop

        return package

    return packages, numberOfPackages