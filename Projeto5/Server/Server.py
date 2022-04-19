from enlace import *
import time
import numpy as np
from utils import *
import math
from Package import *
from datetime import datetime


class Server:

    def __init__(self,serialName,id,destiny):

        self.com = enlace(serialName)
        self.id = id
        self.destiny = destiny

        self.status = 'OFF'
        self.ready = False
        self.waiting = None
        self.sacrifice = False
        self.next = False

        self.logs = []

        self.nPackage = None
        self.nPackages = None

        self.timer1 = time.time()
        self.timer2 = time.time()

        self.message = b''

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

        time.sleep(.3)
        self.com.sendData(b'00')
        time.sleep(.3)

    def receiveSacrifice(self):

        rxBuffer, nRx = self.com.getData(1)
        self.com.rx.clearBuffer()
        time.sleep(.1)
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
            self.status = 'ON'

            while self.status == 'ON':
                self.handShake()
                if self.next:
                    self.receivingPackages()
                    if self.next:
                        self.write()

                self.status = "OFF"

            self.end()

        except Exception as erro:
            print("ops! :-\\")
            print(erro)
            self.com.disable()



    def handShake(self):

        while not self.ready:
            if self.com.rx.getBufferLen()>0:
                if not self.sacrifice:
                    self.receiveSacrifice()
                else:
                    head, nH = self.com.getData(10)
                    self.printLog('receb',str(head[0]))


                    if head[0] == 1 and head[2] == self.id:

                        eop, nE = self.com.getData(4)

                        self.nPackages = int(head[3])

                        self.sendSacrifice()

                        package = createPackage(2,self.id, self.destiny)
                        self.com.sendData(package)
                        self.printLog('envio','2')

                        self.ready = True
                        self.nPackage = 1
                        self.next = True
                        
    def receivingPackages(self):

        self.next = False

        while self.nPackage < self.nPackages:
            payloadError = False
            eopError = False
            indexError = False
            crcError = False

            self.resetTimers()

            self.waiting = True

            while self.waiting:

                if time.time() - self.timer2 > 20:
                    waiting = False

                    package = createPackage(5,self.id,self.destiny)
                    self.com.sendData(package)
                    self.printLog('envio','5')

                    return

                elif time.time() - self.timer1 > 2:
                    self.resetTimers(1)
                    self.com.rx.clearBuffer()
                    
                    package = createPackage(6,self.id,self.destiny, nPackage = self.nPackage)
                    self.com.sendData(package)
                    self.printLog('envio','6')

                elif self.com.rx.getBufferLen() > 0:
                    self.waiting = False

                    head, nH = self.com.getData(10)
                    


                    if head[0] == 3:

                        nP = head[4]
                        payloadSize = head[5]

                        self.printLog('receb','3',payloadSize)

                        if self.nPackage != nP:
                            indexError = True

                        if self.com.rx.getBufferLen() != payloadSize + 4:
                            payloadError = True

                        if payloadError == False:
                            payload, nPl = self.com.getData(payloadSize)
                        else:
                            payloadTrash, nPt = self.com.getData(self.com.rx.getBufferLen())

                        eop, nE = self.com.getData(4)
                        if eop != b'\xaa\xbb\xcc\xdd':
                            eopError = True

                        if payload is not None:
                            #VERIFICA CRC
                            crc8 = head[8].to_bytes(1, byteorder='big')
                            crc9 = head[9].to_bytes(1, byteorder='big')
                            
                            crc8novo, crc9novo = createCRC(payload)

                            if (crc8 != crc8novo) or (crc9 != crc9novo):
                                print(crc8,(crc8novo))
                                print(crc9,(crc9novo))
                                crcError = True


                        if not eopError and not payloadError and not indexError and not crcError:
                            
                            #Atualiza mensagem
                            self.message = self.message + payload

                            package = createPackage(4,self.id, self.destiny, nPackage = self.nPackage)
                            self.com.sendData(package)

                            self.printLog('envio','4')

                            self.nPackage += 1

                            if self.nPackage == self.nPackages:
                                self.next = True
                        
                        else:
                            package = createPackage(6,self.id, self.destiny, nPackage = self.nPackage)
                            self.com.sendData(package)
                            self.printLog('envio','6')
                            self.com.rx.clearBuffer()

    
    def write(self):

        f = open('./celeste.png','wb')
        f.write(self.message)
        f.close()
    
    def end(self):

        with open('Server.txt','w') as f:
            f.writelines(self.logs)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.com.disable()