import numpy as np
import pygame
import mido
import threading

SAMPLE_RATE = 44100 # samplerate(tem q ser 44100khz pq mais que isso, minha interface da problema
VOLUME = 0.3 # volume
WAVEFORM = "triangle"  # sine, square, saw, triangle / pra tocar só mudar o nome aqui e executar dnv

#stereo
pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
pygame.init()
pygame.mixer.init()

playing = {}

def midi_to_freq(note):
    return 440 * (2 ** ((note - 69) / 12))


def generate_wave(freq, duration=2.0):

    t = np.linspace(
        0,
        duration,
        int(SAMPLE_RATE * duration),
        False
    )

    if WAVEFORM == "sine":
        wave = np.sin(2 * np.pi * freq * t)

    elif WAVEFORM == "square":
        wave = np.sign(np.sin(2 * np.pi * freq * t))

    elif WAVEFORM == "saw":
        wave = 2 * (freq * t - np.floor(0.5 + freq * t))

    elif WAVEFORM == "triangle":
        wave = 2 * np.abs(
            2 * (freq * t - np.floor(freq * t + 0.5))
        ) - 1

    else:
        wave = np.sin(2 * np.pi * freq * t)

    audio = (wave * 32767 * VOLUME).astype(np.int16)

    # 🔥 converte pra estéreo (OBRIGATÓRIO)
    audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(audio)


def note_on(note):
    freq = midi_to_freq(note)
    sound = generate_wave(freq)
    channel = sound.play(-1)
    playing[note] = channel


def note_off(note):
    if note in playing:
        playing[note].stop()
        del playing[note]


def midi_thread():
    ports = mido.get_input_names()

    if not ports:
        print("sem midi encontrado")
        return

    print("MIDI:")
    for p in ports:
        print("-", p)

    port_name = ports[0]
    print("\nLIGADO:", port_name) # port_name retorna qual midi ta conectado no pc

    with mido.open_input(port_name) as port:
        for msg in port:

            if msg.type == "note_on" and msg.velocity > 0:
                note_on(msg.note)

            elif msg.type == "note_off" or (
                msg.type == "note_on" and msg.velocity == 0
            ):
                note_off(msg.note)


threading.Thread(
    target=midi_thread,
    daemon=True
).start()

print("FUNCIONANDO")
print("Wave:", WAVEFORM) # retorna qual waveform ta ligada no programa

while True:
    pygame.time.wait(100)