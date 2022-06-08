#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import sounddevice as sd
import numpy as np
import time
import matplotlib.pyplot as plt
from sqlalchemy import true
from suaBibSignal import *
import peakutils
from peakutils.plot import plot as pplot


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    fs = 44100
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa

    n = 1
    print(f"A captação começará em {n} segundos")
    time.sleep(n)
    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
   
   #faca um print informando que a gravacao foi inicializada
    print("Gravação inicializada")
   
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)

    duracao = 2
    numAmostras =   fs * duracao

    audio = sd.rec(int(numAmostras),    fs, channels=1)
    print(audio[0])
    y = audio[:,0]
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    inicio = 0
    fim = 1
    numPontos = fs * 2
    t = np.linspace(inicio,fim,numPontos)

    # plot do gravico  áudio vs tempo!
    plt.figure()
    plt.plot(t,audio[:,0])

    signal_objeto = signalMeu()
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    # signal_objeto.plotFFT(audio[:5000]    fs)

    xf, yf = signal_objeto.calcFFT(y,  fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(yf, thres=0.2, min_dist=50)
    print("PICOS:")
    print(xf[index], yf[index])
    pplot(xf, yf, index)
    plt.show()

    dicionario_ondas = {
        '1': (697, 1206), '2': (697, 1339), '3': (697, 1477), 'A': (697, 1633),
        '4': (770, 1206), '5': (770, 1339), '6': (770, 1477), 'B': (770, 1633),
        '7': (852, 1206), '8': (852, 1339), '9': (852, 1477), 'C': (852, 1633),
        'X': (941, 1206), '0': (941, 1339), '#': (941, 1477), 'D': (941, 1633)
    }

    lista_ondas = [697, 770, 852, 941, 1206, 1339, 1477, 1633]
    

    frequenciasPossiveis = []
            
    for xPico in xf[index]:
        for onda in lista_ondas:
            if abs(xPico - onda) < 2:
                frequenciasPossiveis.append(onda)
                break

    print(f'As frequencias possíveis são as seguintes: {frequenciasPossiveis}')

    if len(frequenciasPossiveis) > 1:
        res = [(a, b) for idx, a in enumerate(frequenciasPossiveis) for b in frequenciasPossiveis[idx + 1:]]

        for pair in res:
            if pair in dicionario_ondas.values():
                for key in dicionario_ondas:
                    if dicionario_ondas[key] == pair:
                        print(f'A tecla digitada foi {key}')
                break
    else:
        print("Nao encontramos nada")

        


    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    # plt.show()

if __name__ == "__main__":
    main()
