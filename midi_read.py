import mido
mid = mido.MidiFile('./MIDI/impmarch.mid', clip = True)

for i in mid.tracks[1][:20]:
    print(i)