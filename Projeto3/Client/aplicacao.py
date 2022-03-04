#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

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
        #Registra tempo inicial
        start_time = time.time()
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.


        com1 = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        comands, nComands = utils.randomCommands()

        #Envia as informações numero de bytes depois comandos
        print('Transmissao vai comecar')
        print('Enviou-se {0} comandos'.format(nComands))

        #Bit de sacrificio
        utils.sendSacrifice(com1)


        #Envia arrays
        
        com1.sendData(comands)
        start_time = time.time()

        while True:
            if time.time() - start_time >= 10:

                print('Timeout!')

                break

            if com1.rx.getBufferLen() > 0:
                #Recebendo byte de sacrificio
                rxBuffer, nRx = utils.receiveSacrifice(com1)

                #Recebendo verdadeiro valor
                rxBuffer, nRx = com1.getData(1)
                response = int.from_bytes(rxBuffer,'big')
                print('O servidor enviou de volta {} comandos'.format(response))
                break
            
        if nComands != response:
            print('Ocorreu um erro de interpretação!')

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