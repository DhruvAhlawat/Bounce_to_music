import mido
mid = mido.MidiFile('./MIDI/impmarch.mid', clip = True)
print(len(mid.tracks[0]))