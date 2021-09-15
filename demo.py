#!/usr/bin/env python3

import soundfile as sf
from sys import argv
from pedalboard import (
    Pedalboard,
    Compressor,
    Convolution,
    Chorus,
    Gain,
    Reverb,
    Limiter,
    LadderFilter,
    Phaser,
)
import time, webbrowser

fileName = argv[0] if argv[0] != 'demo.py' else 'short-demo-song.wav'

print('reading soundfile %s...' % (fileName))

audio, sample_rate = sf.read(fileName)

newFileName = 'short-demo-song-processed' + str(int(time.time())) + '.wav'

print('setting up board...')

# Make a Pedalboard object, containing multiple plugins:
board = Pedalboard([
    Compressor(threshold_db=-24, ratio=25),
    Gain(gain_db=0.3),
    Chorus(rate_hz=0.2, mix=0.2, depth=0.1),
    Convolution('crash.wav', 0.6),
    LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=300),
    # Phaser(),
    Reverb(room_size=0.3),
], sample_rate=sample_rate)

print('board set up!')

# Pedalboard objects behave like lists, so you can add plugins:
board.append(Compressor(threshold_db=-25, ratio=10))
# board.append(Gain(gain_db=1))
board.append(Limiter())

print('running audio through pedalboard...')

# Run the audio through this pedalboard!
effected = board(audio)

print('writing back as wav file...')

# Write the audio back as a wav file:
with sf.SoundFile(newFileName, 'w', samplerate=sample_rate, channels=len(effected.shape)) as f:
    f.write(effected)

print('done!')

chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

webbrowser.get(chrome_path).open(newFileName)