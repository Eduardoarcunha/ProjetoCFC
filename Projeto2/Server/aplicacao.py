#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import utils

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM8"                  # Windows(variacao de)


def main():
    try:
        #Registra tempo inicial
        start_time = time.time()

        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)      
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        state = 0
        nBytes = 0
        nComands = 0

        while True:
            if state == 0 and com1.rx.getBufferLen() > 0:
                #Recebendo byte de sacrificio
                rxBuffer, nRx = utils.receiveSacrifice(com1)
                state = 1


            elif state == 1:
                print("Recebendo n Bytes do próximo comando")
                print("Rx antes de ler {}".format(rxBuffer))
                
                rxBuffer, nRx = com1.getData(1)
                time.sleep(.2)

                #Finaliza recepção
                if rxBuffer == b'\xff':
                    com1.rx.clearBuffer()
                    break

                nBytes = int.from_bytes(rxBuffer,'big')
                state = 2

                print("Byte que chegou: {0} ({1}) \n".format(rxBuffer,nBytes))

            elif state == 2 and com1.rx.getBufferLen() > 0:
                #Recebendo byte de sacrificio
                rxBuffer, nRx = utils.receiveSacrifice(com1)
                state = 3
                
            elif state == 3:
                rxBuffer, nRx = com1.getData(nBytes)
                time.sleep(.2)
                nComands += 1
                state = 0
                
                print('Comando que chegou: {0} ({1})\n'.format(rxBuffer,len(rxBuffer)))

        #Enviando número de comandos
        #Bit de sacrificio
        utils.sendSacrifice(com1)
        

        #Envia nComands
        nComands = nComands.to_bytes(1, byteorder='big')
        com1.sendData(nComands)
    
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