
#importe as bibliotecas
from re import A
from signal import signal
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    print("Aguardando usuário")

    while True:
        tecla = input('Digite uma tecla numérica!')
        if tecla.isdigit() and len(tecla) == 1:
            break

        elif tecla in ['A','B','C','D','X','#']:
            break

        else:
            print("Valor invalido tente novamente")

    dicionario_ondas = {
        '1': [697, 1206], '2': [697, 1339], '3': [697, 1477], 'A': [697, 1633],
        '4': [770, 1206], '5': [770, 1339], '6': [770, 1477], 'B': [770, 1633],
        '7': [852, 1206], '8': [852, 1339], '9': [852, 1477], 'C': [852, 1633],
        'X': [941, 1206], '0': [941, 1339], '#': [941, 1477], 'D': [941, 1633]
    }

    fs = 44100

    frequencia_ondas = dicionario_ondas[tecla]
    
    t = 5

    signal_objeto = signalMeu()
    time1, signal1 = signal_objeto.generateSin(frequencia_ondas[0], 1, t, fs)

    signal2 = signalMeu()
    time2, signal2 = signal_objeto.generateSin(frequencia_ondas[1], 1, t, fs)

    signal_final = signal1 + signal2


    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(tecla))

    sd.play(signal_final, fs)
    # Exibe gráficos
    sd.wait()

    signal_objeto.plotFFT(signal_final, fs)

    plt.figure()
    plt.plot(time1[:500], signal_final[:500])
    plt.show()
    # aguarda fim do audio

    

if __name__ == "__main__":
    main()
