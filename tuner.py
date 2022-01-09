import pyaudio
import wave
import numpy as np
pa = pyaudio.PyAudio()

RATE = 48000
CHANNELS=1
FORMAT=pyaudio.paInt16
FRAMES=1024

filename = "sick-tune-bro.wav"

stream = pa.open(
    rate=RATE,
    channels=CHANNELS,
    format=FORMAT,
    frames_per_buffer=FRAMES,
    input=True
)


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