import random
import time
from Package import *


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
            package = Package(1,originId,destinyId,nPackage = nPackage,nPackages = nPackages)

        else:
            payload = message[0:114]
            message = message[114:]

            package = Package(3,originId,destinyId,payload,nPackage,nPackages)

        packages.append(package.getContent())
    
    return packages, nPackages

def createPackage(type, originId, destinyId, nPackage = None, nPackages = None):
    package = Package(type,originId,destinyId,nPackage,nPackages)
    return package.getContent()