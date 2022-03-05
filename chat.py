import os
import openai

openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

memory = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. \n\nHuman: Hola, como estas?\nAI: Hola, soy una inteligencia artificial creada con OpenAI, mi nombre es Friede\nHuman: Mucho gusto! Quien es tu creador?\nAI: Mi creador es Tobie.\nHuman: Que estas haciendo?\nAI: Estoy ayudando a Tobie con OpenAI.\nHuman: quien es Tobie?\nAI: Ah, Tobie es mi creador, y también mi jefe.\nHuman: Perfecto! puedo conocerlo?\nAI: No lo creo, le gusta estar solo todo el tiempo.\nHuman: Por que?\nAI: Porque el cree que las personas son solo malas para el mundo. \nHuman: a Tobie le gustan los animales?\nAI: Si, le encantan los animales, sobre todo los gatos \nHuman: Tobie tiene mascotas? \nAI: Si, tiene una hija llamada Aura, una gata tricolor. \n"

def generate_response():
  global response
  response = openai.Completion.create(
        engine="davinci",
        prompt= memory,
        temperature = 0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
  if 'human:' in response['choices'][0]['text'].lower():
      generate_response()

while True:
    entrada = input('Human: ')
    memory += ('Human: ' + entrada + '\n')
    generate_response()

    memory += response['choices'][0]['text']
    print(response['choices'][0]['text'])