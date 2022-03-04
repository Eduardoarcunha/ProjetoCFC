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

        message = b''


        protocol = True
        while protocol:
            print('Iniciando protocolo')

            #Esperando contato:
            hold = True
            sacrifice = False
            while hold:
                if com1.rx.getBufferLen() > 0:
                    #Verifica se ja foi recebido um bit de sacrificio
                    if not sacrifice:
                        rxBuffer, nRx = utils.receiveSacrifice(com1)
                        sacrifice = True
                    else:
                        print('Recebendo pedido client')
                        rxBuffer, nRx = com1.getData(1)
                        hold = False

            print('Enviando resposta')
            #Bit de sacrificio
            utils.sendSacrifice(com1)

            #Envia resposta
            com1.sendData(b'\x44')

            n = 0
            nPackages = 100

            print('Recebendo pacotes')
            while n < nPackages:
                hold = True
                sacrifice = False

                while hold:
                    if com1.rx.getBufferLen() > 0:
                        #Verifica se ja foi recebido um bit de sacrificio
                        if not sacrifice:
                            rxBuffer, nRx = utils.receiveSacrifice(com1)
                            sacrifice = True
                        else:
                            

                            print('Lendo pacote {}'.format(n + 1))

                            #Pega head
                            head, nHd = com1.getData(10)
                            nPackages = int(head[0])
                            nPackage = int(head[1])
                            
                            if nPackage != n:
                                print('deu ruim')

                            if nPackage == nPackages:
                                protocol = False

                            payloadSize = int(head[2])

                            #Pega payload
                            payload, nPl = com1.getData(payloadSize)

                            message = message + payload

                            #Pega EOP
                            eop, nEOP = com1.getData(4)

                            #Bit de sacrificio
                            utils.sendSacrifice(com1)

                            time.sleep(.2)
                            #Envia resposta
                            com1.sendData(b'\x44')

                            print('Pacote {} recebido com sucesso \n'.format(n + 1))

                            n +=1

                            hold = False
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