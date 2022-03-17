#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from struct import pack
from enlace import *
import time
import numpy as np
import utils
import math

#   python -m serial.tools.list_ports

serialName = "COM8"

id = 128

def main():
    try:
        com1 = enlace(serialName)      
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #Resposta final do cliente
        message = b''


        protocol = True
        while protocol:
            print('Iniciando protocolo')

            #Esperando contato:
            hold = True
            sacrifice = False

            #Servidor pronto para responder?
            ready = False

            while not ready:
                if com1.rx.getBufferLen() > 0:
                    if not sacrifice:
                        rxBuffer, nRx = utils.receiveSacrifice(com1)
                        sacrifice = True

                    else:
                        head, nRx = com1.getData(10)
                        eop = com1.getData(4)


                        if head[0] == 1 and head[1] == id:
                            print('O recebimento é para ca')

                            utils.sendSacrifice(com1)

                            #Montar pacote
                            package = utils.createPackages('ready')

                            print('Enviando pacote do tipo 2!')
                            com1.sendData(package)
                            time.sleep(.5)

                            ready = True


            n = 1
            nPackages = math.inf

            print('------------------')
            print('Recebendo pacotes')
            while n < nPackages:

                payloadError = False
                eopError = False

                #Esperando recebimento
                waiting = True
                while waiting:
                    if com1.rx.getBufferLen() > 0:
                        print('Lendo pacote {}'.format(n))

                        #Pega head
                        head, nH = com1.getData(10)
                        nPackages = int(head[3])
                        nPackage = int(head[4])
                        
                        if nPackage != n:
                            print('Número do pacote incorreto!')
                            
                        if nPackage == nPackages:
                            protocol = False

                        #Tamanho do payload!
                        payloadSize = int(head[5])

                        #Verifica tamanho payload
                        if com1.rx.getBufferLen() != payloadSize + 4:
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
                            print("ERRO EOP")

                        #erro = utils.tipoErro(eopError,indexError,payloadError)

                        #Sem erro de eop ou payload
                        if not eopError and not payloadError:
                            message = message + payload

                            package = utils.createPackages('correct')

                            com1.sendData(package)
                            print('Pacote {} recebido com sucesso \n'.format(n))
                            n +=1
                            time.sleep(1)
                            
                        else:
                            #Codigo de erro
                            package = utils.createPackages('error', h7 = n-1)
                            com1.rx.clearBuffer()

                            com1.sendData(package)
                            time.sleep(.5)
                            print(package)

                            print('---------------------ALERTA-----------------------')
                            print('Pacote {} não foi recebido com sucesso (ERRO: {})'.format(n,erro))
                            print('--------------------------------------------------\n')
                            protocol = True
                            time.sleep(1)
                        
                        waiting = False
                    
            protocol = False
            print('Fim do recebimento')

        f = open('./celeste.png','wb')
        f.write(message)
        f.close()
                    


        
    
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