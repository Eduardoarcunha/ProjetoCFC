#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from multiprocessing.connection import wait
from struct import pack
from enlace import *
import time
import numpy as np
import utils
import math
from datetime import datetime

#   python -m serial.tools.list_ports

serialName = "COM8"
id = 128

timeoutError1 = False
timeoutError2 = False

def main():
    i2 = False
    logs = []
    try:
        com1 = enlace(serialName)      
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #Resposta final do cliente
        message = b''

        protocol = True
        while protocol:
            print('Iniciando protocolo')

            #Bit de sacrificio
            sacrifice = False

            #Servidor pronto para responder?
            ready = False

            while not ready:
                if com1.rx.getBufferLen() > 0:
                    if not sacrifice:
                        rxBuffer, nRx = utils.receiveSacrifice(com1)
                        sacrifice = True

                    else:
                        while timeoutError1:
                            continue
                        head, nRx = com1.getData(10)
                        eop = com1.getData(4)

                        log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/1/'+ '14' + '\n'
                        logs.append(log)
                        print(log)        

                        if head[0] == 1 and head[1] == id:

                            nPackages = int(head[3])

                            print('O request realmente é para este servidor!')

                            #Bit de sacrificio
                            utils.sendSacrifice(com1)

                            #Montar pacote tipo 2
                            package = utils.createPackages('ready')
                            com1.sendData(package)
                            time.sleep(.2)

                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/2/'+ '14' + '\n'
                            logs.append(log)
                            print(log)  

                            ready = True

            n = 1

            print('------------------')
            print('Recebendo pacotes')
            while n < nPackages:

                payloadError = False
                eopError = False
                indexError = False

                timer1 = time.time()
                timer2 = time.time()

                #Esperando recebimento
                waiting = True
                while waiting:

                    if time.time() - timer2 > 20:
                        waiting = False
                        n = math.inf
                        ready = False

                        #Envia mensagem tipo 5
                        package = utils.createPackages('timeout')  
                        com1.sendData(package)
                        time.sleep(.2) 

                        log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/5/'+ str(10 + 4) + '\n'
                        logs.append(log)
                        print(log)

                        with open('Server6.txt','w') as f:
                            f.writelines(logs)

                    elif time.time() - timer1 > 2:
                        timer1 = time.time()  

                        #Envia mensagem tipo 6
                        com1.rx.clearBuffer()
                        package = utils.createPackages('error', h7 = n - 1)

                        log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/6/'+ str(10 + 4) + '\n'
                        logs.append(log)
                        print(log)

                        com1.sendData(package)
                        time.sleep(.2)
          
                    
                    #Chegou algum tipo de resposta
                    elif com1.rx.getBufferLen() > 0:

                        while timeoutError2:
                            continue

                        waiting = False
                        

                        #Pega head
                        head, nH = com1.getData(10)
                        time.sleep(.2)
                        


                        if head[0] == 3:

                            nPackage = int(head[4])

                            #Tamanho do payload!
                            payloadSize = int(head[5])

                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/3/'+ str(10 + (payloadSize - 1) + 4) + '/' + str(nPackage) + '/' + str(nPackages) + '\n'
                            logs.append(log)
                            print(log)
                            
                            if nPackage != n:
                                print('Número do pacote incorreto!')
                                indexError = True
                                i2 = True
                                
                            if nPackage == nPackages:
                                protocol = False
                            

                            #Verifica tamanho payload
                            if com1.rx.getBufferLen() != payloadSize + 4:
                                payloadError = True
                                print('-------------')
                                print('Tamanho do payload incorreto!\nInformado: {0}\nReal: {1}'.format(payloadSize,int(com1.rx.getBufferLen()) - 4))

                            #Pega payload caso seu tamanho esteja certo!
                            if payloadError == False:
                                payload, nPl = com1.getData(payloadSize)
                            else:
                                payloadTrash, nPT = com1.getData(com1.rx.getBufferLen() - 4)

                            #Pega EOP
                            eop, nEOP = com1.getData(4)

                            if eop != b'\xaa\xbb\xcc\xdd':
                                eopError = True
                                print("EOP incorreto!")

                            erro = utils.tipoErro(eopError,indexError,payloadError)

                            #Sem nenhum tipo de erro
                            if not eopError and not payloadError and not indexError:
                                #Atualiza mensagem
                                message = message + payload

                                package = utils.createPackages('correct',h7 = n)
                                com1.sendData(package)

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/4/'+ str(10 + 4) + '\n'
                                logs.append(log)
                                print(log)


                                n += 1
                                time.sleep(.2)
                                
                            else:
                                #Codigo de erro
                                package = utils.createPackages('error', h7 = n-1)
                                com1.sendData(package)

                                log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/envio/6/'+ str(10 + 4) + '\n'
                                logs.append(log)
                                print(log)

                                com1.rx.clearBuffer()
                                time.sleep(.2)

                                print('---------------------ALERTA-----------------------')
                                print('Pacote {0} não foi recebido com sucesso (ERRO:{1})'.format(n,erro))
                                print('--------------------------------------------------\n')
                                protocol = True
                        
                        elif head[0] == 5:
                            waiting = False
                            n = math.inf
                            print("TIMEOUT CHEGOU")

                            
                            log = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '/receb/5/'+ str(10 + 4) + '\n'
                            logs.append(log)
                            print(log)


                    
            protocol = False
            print('Fim do recebimento')

            

        f = open('./celeste.png','wb')
        f.write(message)
        f.close()

        if i2 == True:
            with open('Server2.txt','w') as f:
                f.writelines(logs)
        else:
            with open('Server1.txt','w') as f:
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