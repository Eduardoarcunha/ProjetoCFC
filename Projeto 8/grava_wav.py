import numpy 
import sounddevice as sd
import soundfile as sf
import sys

#Frequencia de amostragem
fs = 44100

#Duracao e numero de amostrar
duracao = 5
numAmostras =   fs * duracao

filename = 'output.wav'
audio = sd.rec(int(numAmostras), fs, channels=1)
sd.wait()

sf.write(filename, audio, fs)