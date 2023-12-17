import mido
import time
import rtmidi
import pygame
import pickle
mid = mido.MidiFile('./MIDI/RFiY.mid') #, clip = True)
print(len(mid.tracks))
 
pygame.mixer.init(frequency = 44100, size = -16, channels = 2)
# pygame.mixer.music.load('./MIDI/RFiY.mid')
# pygame.mixer.music.play()

# while True:
#     pass
# for i in mid.tracks[0][:200]:
#     print(i)
time_series = []
with open("frame_series.pickle", "rb") as f:
    time_series = pickle.load(f)

print(time_series)