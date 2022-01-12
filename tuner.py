#wip
import pyaudio
import wave
import numpy as np
pa = pyaudio.PyAudio()

RATE = 48000
CHANNELS=1
FORMAT=pyaudio.paInt16
FRAMES=1024
CONCERT_PITCH = 440

filename = "sick-tune-bro.wav"

stream = pa.open(
    rate=RATE,
    channels=CHANNELS,
    format=FORMAT,
    frames_per_buffer=FRAMES,
    input=True
)



# 12 * log2(fi/f0)=i ;; formula to find how many half steps between fi and f0

notes = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
def find_closest_note(pitch):
    if pitch == 0:
        return 0, 0
    else:
        i = int(np.round(12 * np.log2(pitch/CONCERT_PITCH)))
        closest_pitch = CONCERT_PITCH*2**(i/12)
        closest_note = notes[i%12] + str(4 + (i + 9) // 12)
        return closest_note, closest_pitch



# continuous recording until program exits
try:
    frames = []
    while True:
        data = stream.read(FRAMES)
        frames.append(data)

        #perform FFT on the data
        fft = np.fft.fft(np.fromstring(data, dtype=np.int16))
        freqs = np.fft.fftfreq(len(fft))

        # find peak
        idx = np.argmax(np.abs(fft))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * RATE)

        print(f"hertz: {freq_in_hertz}")

        note, pitch = find_closest_note(freq_in_hertz)
        print(f"note: {note}")
        print(f"pitch: {pitch}")




  
except KeyboardInterrupt:

    # stop recording
    stream.stop_stream()
    stream.close()
    pa.terminate()

    #save audio
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()