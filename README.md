# Synth MIDI

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-100%25%20Concluído-success)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-0d1117?style=flat&logo=python&logoColor=white)
![MIDI](https://img.shields.io/badge/MIDI-Supported-orange)

Sintetizador simples controlado por teclado MIDI, desenvolvido em Python. O projeto recebe eventos MIDI, converte as notas para frequências e gera ondas sonoras digitalmente utilizando NumPy e Pygame.

## Sobre o Projeto

O projeto funciona como um sintetizador básico controlado por dispositivos MIDI. 

Ao pressionar uma tecla no controlador MIDI, o programa:

1. Recebe o evento MIDI da nota.
2. Converte o número da nota MIDI para sua frequência correspondente.
3. Gera digitalmente uma onda sonora.
4. Reproduz a nota através do mixer de áudio do Pygame.

Quando a tecla é solta, a reprodução correspondente é interrompida.

A geração das ondas é realizada através de cálculos matemáticos com NumPy, enquanto o Pygame é responsável pela reprodução do áudio.

## Funcionalidades

- Leitura de dispositivos MIDI disponíveis no sistema.
- Detecção automática da primeira porta MIDI encontrada.
- Suporte a eventos `note_on` e `note_off`.
- Conversão de notas MIDI para frequência em Hertz.
- Geração de diferentes formas de onda.
- Reprodução de notas em loop enquanto a tecla MIDI permanece pressionada.
- Suporte a múltiplas notas simultaneamente.
- Processamento da entrada MIDI em uma thread separada.

## Formas de Onda

O sintetizador possui suporte às seguintes formas de onda:

- `sine` — onda senoidal.
- `square` — onda quadrada.
- `saw` — onda dente de serra.
- `triangle` — onda triangular.

A forma de onda utilizada é definida pela constante:

```
WAVEFORM = "square"
```

Caso seja informado um valor diferente dos tipos suportados, o sistema utiliza uma onda senoidal como padrão.

# Tecnologias Utilizadas
### Python

- Linguagem utilizada para desenvolver toda a aplicação.

### NumPy

- Utilizado para realizar os cálculos matemáticos necessários para a geração das ondas sonoras e manipulação dos dados de áudio.

### Pygame

- Utilizado para inicialização do sistema de áudio e reprodução dos sons gerados.

### Mido

- Utilizado para detectar portas MIDI, abrir a conexão com o dispositivo e receber mensagens MIDI.

### Threading

- Utilizado para executar a leitura do dispositivo MIDI em uma thread separada do fluxo principal da aplicação.

# Como Executar

O código depende de Python e das bibliotecas utilizadas diretamente no projeto.

- As dependências são:
```
numpy
pygame
mido
```
Após instalar o Python e as dependências, execute o arquivo principal do projeto pelo interpretador Python. O programa deverá detectar as portas MIDI disponíveis e selecionar automaticamente a primeira encontrada.

# Configuração

As principais configurações estão definidas no início do código:
```
SAMPLE_RATE = 44100
VOLUME = 0.3
WAVEFORM = "square"
```


**SAMPLE_RATE** Define a taxa de amostragem utilizada para a geração do áudio.

**VOLUME** Define o volume geral aplicado ao sinal gerado.

**WAVEFORM** Define o tipo de onda utilizado pelo sintetizador.

- Valores suportados:
```
sine
square
saw
triangle
```

# Funcionamento

O fluxo principal da aplicação pode ser representado da seguinte forma:

```
Teclado MIDI
     |
     v
Mido
     |
     v
Evento MIDI
     |
     v
midi_thread()
     |
     +------ note_on ------> midi_to_freq()
     |                              |
     |                              v
     |                       generate_wave()
     |                              |
     |                              v
     |                        Pygame Mixer
     |
     +------ note_off -----> Interrupção da nota
```
## Conversão MIDI

Cada tecla MIDI possui um número de nota. Esse número é convertido para uma frequência utilizando A4 como referência em 440 Hz.

A função responsável por essa conversão é:
```
midi_to_freq(note)
```
## Geração do áudio

A função:
```
generate_wave(freq)
```
Cria um vetor de tempo utilizando NumPy e calcula a forma de onda selecionada. O sinal resultante é convertido para áudio PCM de 16 bits e posteriormente duplicado para os canais esquerdo e direito.

## Reprodução

O Pygame transforma o array NumPy em um objeto de áudio utilizando:
```
pygame.sndarray.make_sound(audio)
```
A nota é reproduzida em loop enquanto estiver ativa.

## MIDI

A biblioteca Mido é utilizada para:

- Listar portas MIDI disponíveis;
- Abrir a porta selecionada;
- Receber eventos do dispositivo;
- Identificar notas pressionadas;
- Identificar notas liberadas.

A aplicação seleciona automaticamente a primeira porta encontrada por:
```
ports = mido.get_input_names()
port_name = ports[0]
```
Portanto, o projeto atualmente não possui uma interface para seleção manual do dispositivo MIDI.

# Como utilizar

Com um dispositivo MIDI conectado ao computador:

1. Execute a aplicação.
2. O programa listará as portas MIDI detectadas.
3. A primeira porta disponível será selecionada automaticamente.
4. Pressione uma tecla no controlador.
5. A nota correspondente será convertida e reproduzida.
6. Solte a tecla para interromper a reprodução.
