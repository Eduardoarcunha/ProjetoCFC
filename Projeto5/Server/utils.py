import random
import time
from Package import Package
import binascii
import crcmod


def tipoErro(eopError,indexError,payloadError):
    if eopError and indexError and payloadError:
        erro = 'EOP, INDEX DO PACOTE, PAYLOAD'
    elif eopError and indexError:
        erro = 'EOP, INDEX DO PACOTE'
    elif eopError and payloadError:
        erro = "EOP, PAYLOAD"
    elif indexError and payloadError:
        erro = "INDEX DO PACOTE, PAYLOAD"
    elif eopError:
        erro = "EOP"
    elif indexError:
        erro = "INDEX DO PACOTE"
    elif payloadError:
        erro = "PAYLOAD"
    else:
        erro = None
    
    return erro

def createPackagesToSend(message, originId, destinyId):
    packages = []

    nPackages = len(message) // 114

    if len(message) % 144 > 0:
        nPackages += 1

    #Um pacote extra devido o handshake
    nPackages += 1

    for nPackage in range(nPackages):

        if nPackage == 0:
            package = Package(1,originId,destinyId,nPackage,nPackages)
        else:

            payload = message[0:114]
            message = message[114:]

            package = Package(3,originId,destinyId,payload,nPackage,nPackages)

        packages.append(package.getContent())
    
    return packages, nPackages

def createPackage(type, originId, destinyId, nPackage = None, nPackages = None):
    package = Package(type,originId,destinyId,nPackage = nPackage,nPackages = nPackages)
    return package.getContent()

def createCRC(payload):

        if payload is None:
            return b'\x00', b'\x00'

        else:

            payloadHex = binascii.hexlify(payload)
            payloadBits = binascii.unhexlify(payloadHex)


            crc16 = crcmod.predefined.Crc('crc-16')
            crc16.update(payloadBits)
            hexString = crc16.hexdigest()



            h8 = bytes.fromhex(hexString[0:2])
            h9 = bytes.fromhex(hexString[2:])


            return h8, h9