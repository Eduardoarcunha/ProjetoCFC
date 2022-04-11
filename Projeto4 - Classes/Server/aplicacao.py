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
from Server import *

#   python -m serial.tools.list_ports

serialName = "COM8"

id = 80
clientId = 81

def main():
    
    server = Server(serialName,id,clientId)
    server.run()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()