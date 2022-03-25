#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

from operator import index
from sympy import false
import utils
from enlace import *
import time
import numpy as np
import math
from datetime import datetime

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta


serialName = "COM8"                  # Windows(variacao de)

def main():
    i2 = False
    i5 = False
    indexError = True
    indexErrorC = indexError
    try:
        logs = []
        com1 = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        imageR = './celeste.png'
        celeste = open(imageR,'rb').read()

        
        #Cria pacotes, inclusive o handshake(package = 0)!

        packages, nPackages = utils.createPackages('transmission',celeste)

        print('Transmissao vai comecar')
        print('{} pacotes serão enviados'.format(nPackages))

        serverOn = False
        transmission = True

        timer1 = time.time()
        timer2 = time.time()
        while transmission:
            #Bit de sacrificio
            utils.sendSacrifice(com1)
            
            #Envia o handshake
            com1.sendData(packages[0])
            time.sleep(0.2)

            sacrifice = False

            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/1/'+ str(10 + 4)+ '\n'
            logs.append(log)
            print(log)

            
            connecting = True

            while connecting:
                if time.time() - timer2 > 20:

                    #Envia mensagem tipo timeout
                    package = utils.createPackages('timeout')  
                    com1.sendData(package)
                    time.sleep(.2)

                    log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/5/'+ '14' + '\n'
                    logs.append(log)
                    print(log)

                    connecting = False
                    transmission = False

                    #Incoerencia 2
                    with open('Client3.txt','w') as f:
                        f.writelines(logs)

                    break


                elif time.time() - timer1 > 6:
                    timer1 = time.time()  

                    #Envia mensagem tipo 4
                    com1.rx.clearBuffer()
                    com1.sendData(packages[0])
                    time.sleep(0.2)

                    log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/1/'+ str(10 + 4)+ '\n'
                    logs.append(log)
                    print(log)

                #Se chegou algo no Buffer do client
                elif com1.rx.getBufferLen() > 0:

                    #Bit de sacrificio
                    if not sacrifice:
                        rxBuffer, nRx = utils.receiveSacrifice(com1)
                        sacrifice = True

                    #Le pacote resposta
                    else:
                        head, nHd = com1.getData(10)


                        if head[0] == 2:
                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/2/'+ str(10 + 4)+ '\n'
                            logs.append(log)
                            print(log)

                            eop, nE = com1.getData(4)
                            serverOn = True
                            break

                    
            #Se o server tiver respondido:
            if serverOn:
                #Enviando pacotes
                nPackage = 1

                #Enviando pacotes
                while nPackage < len(packages):

                    if indexError and nPackage == 5:
                        nPackage = 6
                        indexError = False
                        if i5 == False:
                            i2 = True


                    lenPayload = packages[nPackage][5]
                    log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/3/'+ str(10 + lenPayload + 4) + '/' + str(nPackage) + '/' + str(nPackages) + '\n'
                    logs.append(log)
                    print(log)

                    #SendPackage
                    com1.sendData(packages[nPackage])
                    time.sleep(.3)

                    timer1 = time.time()
                    timer2 = time.time()

                    waiting = True
                    #Espera resposta:
                    while waiting:

                        #Reenvia as mensagens!
                        if time.time() - timer1 > 5:
                            com1.sendData(packages[nPackage])
                            time.sleep(.3)

                            lenPayload = packages[nPackage][5]
                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/3/'+ str(10 + lenPayload + 4) + '/' + str(nPackage) + '/' + str(nPackages) + '\n'
                            logs.append(log)
                            print(log)
                            
                            #Reseta timer 1
                            timer1 = time.time()

                        elif time.time() - timer2 > 20:
                            package = utils.createPackages('timeout')
                            com1.sendData(package)

                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/5/'+ '14' + '\n'
                            logs.append(log)
                            print(log)

                            #Mata comunicação
                            nPackage = math.inf
                            waiting = False
                            transmission = False

                            #Incoerencia 4
                            with open('Client4.txt','w') as f:
                                f.writelines(logs)


                        elif com1.rx.getBufferLen() > 0:
                            waiting = False

                            head, nH = com1.getData(10)

                            #Tipo 4: Ultima mensagem foi suecsso
                            if head[0] == 4:

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/4/'+ '14' + '\n'
                                logs.append(log)
                                print(log)

                                nPackage += 1


                            elif head[0] == 5:

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/5/'+ '14' + '\n'
                                logs.append(log)
                                print(log)

                                nPackage = math.inf
                                transmission = False

                            #Ultima mensagem foi fracasso
                            elif head[0] == 6:

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/6/'+ '14' + '\n'
                                logs.append(log)
                                print(log)

                                #Erro no pacote
                                if not i2:
                                    i5 = True

                                #Ultimo pacote recebido com sucesso é este
                                nPackage = head[7] + 1
                            
                            eop, nE = com1.getData(4)
                            time.sleep(.2)

                transmission = False

        if indexErrorC == True:
            with open('Client2.txt','w') as f:
                f.writelines(logs),
        elif i2 == True or i5 == True:
            with open('Client5.txt','w') as f:
                f.writelines(logs)     
        else:
            with open('Client1.txt','w') as f:
                f.writelines(logs)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()