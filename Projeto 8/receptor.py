import sounddevice as sd
from funcoes_LPF import LPF
from scipy.io import wavfile
from math import *
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt

signal_objeto = signalMeu()
fs = 44100
fbanda = 13e3

freq_amostragem, data_modulada = wavfile.read('./output.wav')

#Desmodulando
t, seno_modulado = signal_objeto.generateSin(fbanda,1,5,fs)
data_desmodulada = data_modulada * seno_modulado
sd.play(data_desmodulada/max(data_desmodulada))
sd.wait()

data_filtrada = LPF(data_desmodulada,2500,fs)


plt.figure()
signal_objeto.plotFFT(data_modulada, fs)
plt.grid()
plt.title('Onda modulada')

plt.figure()
signal_objeto.plotFFT(data_filtrada, fs)
plt.grid()
plt.title('Onda desmodulada e filtrada na frequencia')

plt.show()