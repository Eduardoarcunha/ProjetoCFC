from email.mime import audio
import sounddevice as sd
from funcoes_LPF import LPF
from scipy.io import wavfile
from math import *
import numpy as np
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import soundfile as sf

signal_objeto = signalMeu()
fs = 44100
fbanda = 13e3

#Lendo audio
freq_amostragem, data = wavfile.read('./input.wav')
sd.play(data, fs)
sd.wait()

#Apenas filtrado
data_filtrada = LPF(data,2500,fs)

#Apenas normalizado
data_normalizada = data / max(abs(data))

#Normalizando data
data_filtrada_normalizada = data_filtrada / max(abs(data_filtrada))
# sd.play(data_filtrada_normalizada, fs)
# sd.wait()


t, seno_modulado = signal_objeto.generateSin(fbanda,1,5,fs)

data_modulada = data_filtrada_normalizada * seno_modulado

sd.play(data_modulada, fs)
sd.wait()

filename = 'output.wav'
sf.write(filename, data_modulada, fs)

t = np.linspace(0, len(data)/fs, len(data))
#a - onda no tempo
plt.figure()
plt.plot(t,data_normalizada)
plt.grid()
plt.title('Onda normalizada no tempo')

#b - filtraa no tempo
plt.figure()
plt.plot(t,data_filtrada)
plt.grid()
plt.title('Onda filtrada no tempo')

#c - filtrada na frequencia
plt.figure()
signal_objeto.plotFFT(data_filtrada, fs)
plt.grid()
plt.title('Onda filtrada na frequencia')

#d - modulado no tempo
plt.figure()
plt.plot(t,data_modulada)
plt.grid()
plt.title('Onda filtrada no tempo')

#e - modulado na frequencia
plt.figure()
signal_objeto.plotFFT(data_modulada, fs)
plt.grid()
plt.title('Onda modulada na frequencia')


plt.show()