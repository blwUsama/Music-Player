import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sounddevice as sd
import time

class Song:
    def __init__(self, duration, bpm, time_signature_numerator, time_signature_denominator):
        self.duration = duration
        self.bpm = bpm
        self.time_signature_denominator = time_signature_denominator
        self.time_signature_nominator = time_signature_numerator

        self.duration2seconds = {
        "full note" :    (self.time_signature_denominator / 4) * (60 / bpm) * 4,
        "half note" :    (self.time_signature_denominator / 4) * (60 / bpm) * 2,
        "quarter note" : (self.time_signature_denominator / 4) * (60 / bpm),
        "eight note" :   (self.time_signature_denominator / 4) * (60 / bpm) * 1/2,
        "full note dot" :    (self.time_signature_denominator / 4) * (60 / bpm) * 4 * 3/2,
        "half note dot" :    (self.time_signature_denominator / 4) * (60 / bpm) * 2 * 3/2,
        "quarter note dot" : (self.time_signature_denominator / 4) * (60 / bpm) * 3/2,
        "eight note dot" :   (self.time_signature_denominator / 4) * (60 / bpm) * 1/2 * 3/2,
         }    
        
        self.note2frequency = {
            "rest" : 0,
            "Do3": 130,
            "Re3" : 146,
            "Re#3": 155,
            "Mi3" : 164,
            "Fa3" : 174,
            "Sol3" : 196,
            "La3" : 220,
            "Si3" : 246,

            "Do4": 261,
            "Re4" : 293,
            "Re#4": 311,
            "Mi4" : 329,
            "Fa4" : 349,
            "Fa#4" : 370,
            "Sol4" : 392,
            "La4" : 440,
            "Si4" : 493,

            "Do5" :392,
            "Re5" :587,
            "Re#5": 622,
            "Mi5" : 659,
            "Fa5" : 698,
            "Sol5" : 784,
            "La5" : 880,
            "Si5" : 987,
        }

        self.music_sheet = [
        #bar 1
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("La4", "eight note"),
        ("Si4", "eight note"),
        ("La4", "eight note"),
        ("Si4", "eight note"),
        #bar 2
        ("Re5", "eight note"),
        ("Si4", "eight note"),
        ("La4", "quarter note"),
        ("Si4", "quarter note"),
        ("rest", "eight note"),
        ("Si4", "eight note"),
        #bar 3
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("La4", "eight note"),
        ("Sol4", "eight note"),
        #bar 4
        ("La4", "eight note"),
        ("Sol4", "eight note"),
        ("Si4", "quarter note"),
        ("rest", "quarter note dot"),
        ("Si4", "eight note"),
        #bar 5
        ("La4", "eight note"),
        ("Sol4", "eight note"),
        ("Mi4", "eight note"),
        ("Re4", "eight note"),
        ("Mi4", "quarter note"),
        ("Mi4", "eight note"),
        ("Mi4", "eight note"),
        #bar 6
        ("Fa#4", "eight note"),
        ("Mi4", "eight note"),
        ("Re4", "eight note"),
        ("Do4", "eight note"),
        ("Re4", "quarter note"),
        ("Mi4", "quarter note"),
        #bar 7
        ("Sol4", "eight note"),
        ("Mi4", "eight note"),
        ("rest", "half note"),
        ("Mi4", "quarter note"),
        #bar 8
        ("Fa#4", "eight note"),
        ("Re4", "eight note"),
        ("rest", "quarter note"),
        ("rest", "half note"),
        #bar 9
        ("rest", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("La4", "eight note"),
        ("Si4", "eight note"),
        # bar 10
        ("Re5", "eight note"),
        ("Si4", "eight note"),
        ("La4", "quarter note"),
        ("Si4", "quarter note"),
        ("rest", "eight note"),
        ("Si4", "eight note"),
        # bar 11
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        ("La4", "eight note"),
        ("Si4", "eight note"),
        ("La4", "eight note"),
        ("Sol4", "eight note"),
        #bar 12
        ("La4", "eight note"),
        ("Sol4", "eight note"),
        ("Si4", "quarter note"),
        ("rest", "quarter note dot"),
        ("Si4", "eight note"),
        #bar 13
        ("La4", "eight note"),
        ("Sol4", "eight note"),
        ("Mi4", "quarter note"),
        ("Mi4", "quarter note"),
        ("Mi4", "eight note"),
        ("Mi4", "eight note"),
        #bar 14
        ("Fa#4", "eight note"),
        ("Mi4", "eight note"),
        ("Re4", "quarter note"),
        ("Re4", "quarter note"),
        ("Mi4", "quarter note"),
        # bar 15
        ("Sol4", "eight note"),
        ("Mi4", "eight note"),
        ("rest", "half note"),
        ("Si4", "eight note"),
        ("Si4", "eight note"),
        #bar 16
        ("Re5", "eight note"),
        ("Si4", "eight note"),
        ("La4", "quarter note"),
        ("Si4", "quarter note"),
        ("La4", "quarter note"),
        #bar 17
        ("Si4","eight note"),
        ("Si4", "quarter note dot"),
        ]

    def play_note(self, note, note_duration):
        print(f'note : {note}, duration : {note_duration}')
        
        frequency = self.note2frequency[note]
        note_duration = self.duration2seconds[note_duration]

        print(f'note frequency : {frequency}, duration in seconds: {note_duration}')

        sampling_rate = 44100 #Hz
        sampling_period = 1. / sampling_rate
        samples = int(note_duration / sampling_period)

        time_axis = np.linspace(0, note_duration, samples)
        # wave_values = np.sin(2 * np.pi * frequency * time_axis)
        # wave_values = signal.sawtooth(2 * np.pi * frequency * time_axis)
        wave_values = signal.square(2 * np.pi * frequency * time_axis)

        sd.play(wave_values, sampling_rate)
        sd.wait()

    def metronome(self):
        for i in range(self.duration):
            print(f'secunda {i + 1}')
            for j in range(int(self.bpm / 60)):
                self.play_note(440, 0.1)
                time.sleep(60 / self.bpm)    

    def play_song(self):
        for note in self.music_sheet:
            frequency, note_duration = note 
            self.play_note(frequency , note_duration)


mysong = Song (10, 150, 4, 4)

mysong.play_song()