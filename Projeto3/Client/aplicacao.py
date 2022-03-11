#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

from utils import createPackages, receiveSacrifice, sendSacrifice
import utils
from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM9"                  # Windows(variacao de)

def main():
    try:
        com1 = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        imageR = './celeste.png'
        celeste = open(imageR,'rb').read()

        
        packages, nPackages = createPackages(celeste,falseIndex=False,falsePayload=True,falseEOP = False)

        print('Transmissao vai comecar')
        print('{} pacotes serão enviados'.format(nPackages))

        serverOn = False
        transmission = True

        start_time = time.time()
        while transmission:
            #Bit de sacrificio
            utils.sendSacrifice(com1)
            
            #Verificando status servidor:
            com1.sendData(b'\x22')
            time.sleep(0.5)

            sacrifice = False
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
                            com1.sendData(b'\x22')
                            time.sleep(.5)

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
                    if not sacrifice:
                        rxBuffer, nRx = receiveSacrifice(com1)
                        sacrifice = True

                    else:
                        rxBuffer, nRx = com1.getData(1)
                        serverOn = True
                        break

                    
            #Se o server tiver respondido:
            if serverOn:
                print('Server respondeu\n')
                #Enviando pacotes
                nPackage = 0

                while nPackage < len(packages):
                    print('Enviando pacote {}'.format(nPackage + 1))
                    
                    #SendPackage
                    com1.sendData(packages[nPackage])
                    time.sleep(0.5)

                    waiting = True
                    #Espera resposta:
                    while waiting:
                        if com1.rx.getBufferLen() > 0:
                            #Aguarda para poder enviar proxima resposta
                            rxBuffer, nRx = com1.getData(1)
                            waiting = False

                            if rxBuffer == b'\x55':
                                print('---------------------ALERTA---------------------')
                                print('{} pacote foi fracasso'.format(nPackage + 1))
                                print('Recriando pacote para envio')
                                print('------------------------------------------------\n')
                                packages, i = createPackages(celeste,falseIndex=False,falsePayload=False,falseEOP = False)

                            else:
                                print('{} pacote foi sucesso\n'.format(nPackage + 1))
                                nPackage +=1

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