#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

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


serialName = "COM9"                  # Windows(variacao de)

def main():
    try:
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

        start_time = time.time()
        while transmission:
            #Bit de sacrificio
            utils.sendSacrifice(com1)
            
            #Envia o handshake
            com1.sendData(packages[0])
            time.sleep(0.5)
            sacrifice = False


            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/1/'+ str(10 + 4)+ '\n'
            print(log)

            
            connecting = True

            while connecting:

                if time.time() - start_time > 5:
                    invalid = True

                    while invalid:
                        resposta = input('Servidor inativo. Tentar novamente? S/N')

                        #Se a resposta for sim
                        if resposta == 'S':
                            print('Requisitando servidor novamente')
                            start_time = time.time()
                            invalid = False
                            com1.sendData(packages[0])
                            time.sleep(0.5)

                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/1/'+ str(10 + 4)+ '\n'
                            print(log)

                        #Se a resposta for não
                        elif resposta == 'N':
                            connecting = False
                            invalid = False
                            transmission = False

                        #Se a respostas for invalida
                        else:
                            print('Resposta invalida')

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
                            print(log)

                            eop, nE = com1.getData(4)
                            serverOn = True
                            break

                    
            #Se o server tiver respondido:
            if serverOn:
                #Enviando pacotes
                nPackage = 1

                while nPackage < len(packages):

                    lenPayload = packages[nPackage][5]
                    log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/3/'+ str(10 + lenPayload + 4) + '/' + str(nPackage) + '/' + str(nPackages) + '\n'
                    print(log)

                    #SendPackage
                    com1.sendData(packages[nPackage])
                    time.sleep(.7)

                    timer1 = time.time()
                    timer2 = time.time()

                    waiting = True
                    #Espera resposta:
                    while waiting:

                        #Reenvia as mensagens!
                        if time.time() - timer1 > 5:
                            com1.sendData(packages[nPackage])
                            time.sleep(.7)

                            lenPayload = packages[nPackage][5]
                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/3/'+ str(10 + lenPayload + 4) + '/' + str(nPackage) + '/' + str(nPackages) + '\n'
                            print(log)
                            
                            #Reseta timer 1
                            timer1 = time.time()

                        elif time.time() - timer2 > 20:
                            package = utils.createPackages('timeout')
                            com1.sendData(package)

                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/5/'+ '14' + '\n'
                            print(log)

                            #Mata comunicação
                            nPackage = math.inf
                            waiting = False
                            transmission = False


                        elif com1.rx.getBufferLen() > 0:
                            waiting = False

                            head, nH = com1.getData(10)

                            #Tipo 4: Ultima mensagem foi suecsso
                            if head[0] == 4:

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/4/'+ '14' + '\n'
                                print(log)

                                nPackage += 1


                            elif head[0] == 5:

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/5/'+ '14' + '\n'
                                print(log)

                                nPackage = math.inf
                                transmission = False

                            #Ultima mensagem foi fracasso
                            elif head[0] == 6:

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/6/'+ '14' + '\n'
                                print(log)


                                # print('---------------------ALERTA---------------------')
                                # print('{} pacote foi fracasso'.format(nPackage))
                                # print('Recriando pacote para envio')
                                # print('------------------------------------------------\n')

                                #Ultimo pacote recebido com sucesso é este
                                nPackage = head[7] + 1
                                print(head)
                            
                            eop, nE = com1.getData(4)
                            time.sleep(.4)

                transmission = False

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