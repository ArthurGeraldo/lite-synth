# Importa NumPy (usado para matemática pesada e gerar ondas sonoras)
import numpy as np

# Importa pygame (usado para áudio e mixer de som)
import pygame

# Importa mido (usado para ler MIDI do teclado MPK Mini)
import mido

# Importa threading (permite rodar MIDI e áudio ao mesmo tempo)
import threading


# 44100HZ = Taxa padrão
SAMPLE_RATE = 44100

# Volume geral do synth (0.0 = mudo, 1.0 = máximo)
VOLUME = 0.3

# Tipo de forma de onda que o synth vai gerar
WAVEFORM = "square"
    # sine = som limpo
    # square = som digital
    # saw = som agressivo
    # triangle = som suave

# Inicializa o mixer de áudio do pygame
# 44100 Hz, 16-bit, 2 canais = estereo / 1 canal = mono
pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 128)
# BUFFER:
    # 512 = seguro (padrão, mais estável)
    # 256 = bom equilíbrio (leve atraso, mas ok)
    # 128 = mais rápido (boa resposta, ainda estável) = Recomendo esse.
    # 64 = muito rápido (pode dar estalos)
    # 32 = extremo (muito instável, só teste)

# Inicializa todos os módulos do pygame
pygame.init()

# Inicializa especificamente o mixer de áudio
pygame.mixer.init()


# Dicionário que guarda quais notas estão tocando atualmente
# Ex: {60: channel, 62: channel}
playing = {}

# Converte número MIDI (nota) para frequência em Hz
def midi_to_freq(note):
    # Fórmula padrão: A4 (69) = 440 Hz
    return 440 * (2 ** ((note - 69) / 12))
# Cada tecla no midi tem um número correspondente:
    # 69 = A4
    # 60 = C4
    # 72 = C5
    # 57 = A3
# A4 = 440 Hz = Padrão mundial da afinação (vai ser usado no nosso calculo base)

# Multiplicamos por 2 pois a cada vez que a escala sobe, a frequencia vai dobrar também
    # A4 = 440HZ | A5 = 880HZ | A6 = 1760HZ etc

# o "note - 69" é pra calcular a distancia da nota
    # note = 69 → 0 → mesma nota
    # note = 70 → +1 semitom
    # note = 57 → -12 semitons (1 oitava abaixo)

# resumo:
    # pega distância da nota até A4
    # converte isso em oitavas
    # aplica formula (dobrar/ dividir frequência)
    # multiplica por 440 Hz

# Gera a onda sonora baseada na frequência
def generate_wave(freq, duration=2.0):

    # Cria um vetor de tempo de 0 até "duration"
    # Ex: 2 segundos de som em 44100 samples por segundo
    t = np.linspace(
        0,
        duration,
        int(SAMPLE_RATE * duration),
        False
    )

# Seleciona o tipo de onda baseado na variável WAVEFORM

    # sine wave
    if WAVEFORM == "sine":
        wave = np.sin(2 * np.pi * freq * t)

    # square wave
    elif WAVEFORM == "square":
        wave = np.sign(np.sin(2 * np.pi * freq * t))

    # saw wave / a melhor btw s2
    elif WAVEFORM == "saw":
        wave = 2 * (freq * t - np.floor(0.5 + freq * t))

    # triangle wave
    elif WAVEFORM == "triangle":
        wave = 2 * np.abs(
            2 * (freq * t - np.floor(freq * t + 0.5))
        ) - 1

    # Caso vc tenha escrito errado etc, vai tocar a onda pura
    else:
        wave = np.sin(2 * np.pi * freq * t)


    # Converte onda (float -1 até 1) para áudio 16-bit
    audio = (wave * 32767 * VOLUME).astype(np.int16)

    # Converte áudio mono para estéreo
    # Repete o mesmo som no canal esquerdo e direito
    audio = np.column_stack((audio, audio))

    # Converte array NumPy em som tocável pelo pygame
    return pygame.sndarray.make_sound(audio)


# Função chamada quando tecla MIDI é pressionada
def note_on(note):

    # Converte nota MIDI para frequência
    freq = midi_to_freq(note)

    # Gera onda sonora da nota
    sound = generate_wave(freq)

    # Toca o som em loop infinito (-1)
    channel = sound.play(-1)

    # Guarda a nota tocando no dicionário
    playing[note] = channel


# Função chamada quando tecla MIDI é solta
def note_off(note):

    # Se a nota estiver tocando
    if note in playing:

        # Para o som
        playing[note].stop()

        # Remove do dicionário
        del playing[note]


# Thread que escuta o teclado MIDI
def midi_thread():

    # Lista todas as portas MIDI disponíveis
    ports = mido.get_input_names()

    # Se não encontrar nenhum dispositivo MIDI
    if not ports:
        print("sem midi encontrado")
        return

    # Mostra todas as portas MIDI detectadas
    print("MIDI:")
    for p in ports:
        print("-", p)

    # Escolhe a primeira porta automaticamente
    port_name = ports[0]

    # Mostra qual dispositivo foi selecionado
    print("\nLIGADO:", port_name)  # mostra o teclado conectado

    # Abre conexão com o teclado MIDI
    with mido.open_input(port_name) as port:

        # Loop infinito ouvindo eventos MIDI
        for msg in port:

            # Quando tecla é pressionada
            if msg.type == "note_on" and msg.velocity > 0:
                note_on(msg.note)

            # Quando tecla é solta (ou velocity 0)
            elif msg.type == "note_off" or (
                msg.type == "note_on" and msg.velocity == 0
            ):
                note_off(msg.note)


# Cria uma thread separada para não travar o áudio
threading.Thread(
    target=midi_thread,  # função que vai rodar
    daemon=True          # thread fecha junto com o programa
).start()


# Mensagem inicial no terminal
print("FUNCIONANDO")

# Mostra qual waveform está ativa
print("Wave:", WAVEFORM)  # ex: saw, sine, triangle etc


# Loop infinito pra manter o programa rodando
while True:
    pygame.time.wait(100)