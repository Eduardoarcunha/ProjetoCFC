from sympy import E
from enlace import *
import time
import numpy as np
from utils import *
import math
from Package import Package
from datetime import datetime

class Client:

    def __init__(self, serialName, id, destiny,file):
        self.com = enlace(serialName)
        self.id = id
        self.destiny = destiny

        self.sacrifice = False
        self.status = "OFF"
        self.serverReady = False

        self.file = file
        self.logs = []

        self.packages = None
        self.nPackage = 0
        self.nPackages = None

        self.timer1 = time.time()
        self.timer2 = time.time()

    def printLog(self,type,typeN,lenPayload = None):
        
        base = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/' + type + '/' + typeN + '/'

        if typeN == '1' or typeN == '2' or typeN == '4' or typeN == '5' or typeN == '6':
            final = '14' + '\n'
        elif typeN == '3':

            final = str(lenPayload + 14) + '/' + str(self.nPackage) + '/' + str(self.nPackages - 1) + '\n'
        log = base + final
        self.logs.append(log)
        
        print(log)

    def sendSacrifice(self):
        self.com.sendData(b'00')

    def receiveSacrifice(self):

        rxBuffer, nRx = self.com.getData(1)
        self.com.rx.clearBuffer()
        self.sacrifice = True

    def resetTimers(self, which = 0):

        if which == 0:
            self.timer1 = time.time()
            self.timer2 = time.time()
        elif which == 1:
            self.timer1 = time.time()
        elif which == 2:
            self.timer2 = time.time()

    def run(self):
        try:
            self.com.enable()
            self.status = "ON"

            fileB = open(self.file,'rb').read()
            self.packages, self.nPackages = createPackagesToSend(fileB, self.id,self.destiny)

            self.sendSacrifice()

            while self.status == "ON":
                self.handShake()
                if self.status == "ON":
                    self.sendingPackages()
                    self.status = "OFF"
                
            self.end()


        except Exception as erro:
            print("ops! :-\\")
            print(erro)
            self.com.disable()       
        
    def handShake(self):

        self.resetTimers()

        self.com.sendData(self.packages[0])
        self.printLog('envio','1')


        while not self.serverReady:
            if time.time() - self.timer1 > 5:

                self.resetTimers(1)

                self.com.sendData(self.packages[0])
                self.printLog('envio','1')

            elif self.com.rx.getBufferLen() > 0:

                if not self.sacrifice:
                    self.receiveSacrifice()
                    self.sacrifice = True

                else:
                    head, nH = self.com.getData(10)
                    if head[0] == 2:
                        eop, nE = self.com.getData(4)
                        self.nPackage += 1

                        return

    
    def sendingPackages(self):

        while self.nPackage < self.nPackages:
            self.com.sendData(self.packages[self.nPackage])

            lenPayload = self.packages[self.nPackage][5]
            self.printLog('envio','3', lenPayload)
            self.resetTimers()

            waiting = True

            while waiting:

                if time.time() - self.timer1 > 5:
                    self.com.sendData(self.packages[self.nPackage])
                    lenPayload = self.packages[self.nPackage][5]
                    self.printLog('envio','3', lenPayload)

                    self.resetTimers(1)

                elif time.time() - self.timer2 > 20:
                    package = createPackage(5,self.id,self.destiny)
                    self.com.sendData(package)
                    self.printLog('envio','5')

                    return

                elif self.com.rx.getBufferLen() > 0:

                    waiting = False

                    head, nH = self.com.getData(10)

                    if head[0] == 4:
                        self.nPackage += 1
                        self.printLog('receb','4')


                    elif head[0] == 5:
                        self.printLog('receb','5')
                        return

                    elif head[0] == 6:
                        self.printLog('receb','5')
                        self.nPackage = head[6]

                    
                    eop, nE = self.com.getData(4)

    def end(self):

        with open('Client.txt','w') as f:
                f.writelines(self.logs)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.com.disable()

