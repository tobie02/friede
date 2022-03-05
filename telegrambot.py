import telebot
import requests
import os
import sys
import re
import youtube_dl
import subprocess
import sqlite3
import openai

import cv2
import time
import datetime

from telebot import types
from subprocess import check_output
from youtube_dl import YoutubeDL
from urllib import parse, request
from keys import TOKEN, OPENAI

bot = telebot.TeleBot(TOKEN)

openai.api_key = OPENAI

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

ai = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
 \n\nHuman: Hola, como estas?\nAI: Hola, soy una inteligencia artificial creada con OpenAI, mi nombre es Friede. 
 \nHuman: Mucho gusto! Quien es tu creador?\nAI: Mi creador es un humano llamado Tobie.\nHuman: Que estas haciendo?\nAI: Estoy ayudando a Tobie con OpenAI.
 \nHuman: quien es Tobie?\nAI: Ah, Tobie es mi creador, y también mi jefe.\nHuman: Perfecto! puedo conocerlo?
 \nAI: No lo creo, le gusta estar solo todo el tiempo.\nHuman: Por que?\nAI: Porque el cree que las personas son solo malas para el mundo. 
 \nHuman: a Tobie le gustan los animales?\nAI: Si, le encantan los animales, sobre todo los gatos. \nHuman: Tobie tiene mascotas? 
 \nAI: Si, tiene una hija llamada Aura, una gata tricolor. \nHuman: Que bonita! \nAI: Si que lo es! \nHuman: Cual era tu nombre? 
 \nAI: Mi nombre es Friede. \nHuman: Tienes genero? \nAI: Soy una inteligencia artificial y me considero femenina. """

memory = {}

print("Friede has connected to Telegram")

markup = types.ReplyKeyboardMarkup()
markup.add('/buscar', '/hablar', '/friede', '/console', '/consolestop')

global is_searching
is_searching = False
global cmd_on
cmd_on = False
global is_protecting
is_protecting = False
global ai_on
ai_on = False

def generate_response():
    global response
    response = openai.Completion.create(
        engine="davinci",
        prompt= ai,
        temperature = 0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    if 'human:' in response['choices'][0]['text'].lower():
        generate_response()
    if len(response['choices'][0]['text']) < 5:
        generate_response()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bienvenido a la interfaz de Friede", None, None, markup)


@bot.message_handler(commands=['hablar', 'speak'])
def just_talk(message):
    global is_searching
    is_searching = False
    bot.send_message(message.chat.id, "Modo Busqueda desactivado")


@bot.message_handler(commands=['search', 'buscar'])
def send_welcome(message):
    global is_searching
    is_searching = True
    bot.send_message(message.chat.id, 'Modo Busqueda activado, indicame el nombre de la canción')


@bot.message_handler(commands=['console'])
def console(message):
    global cmd_on
    if message.chat.id == 994286593:
        if cmd_on == True:
            cmd_on = False
            bot.send_message(message.chat.id, 'Modo cmd desactivado')
        else:
            cmd_on = True
            bot.send_message(message.chat.id, 'Modo cmd activado')
    else:
        bot.send_message(message.chat.id, 'Acceso denegado')


@bot.message_handler(commands=['ai'])
def ai_lavel(message):
    global ai_on
    if message.chat.id == 994286593:
        if ai_on == True:
            ai_on = False
            bot.send_message(message.chat.id, 'Inteligencia Artificial desactivada')
        else:
            ai_on = True
            bot.send_message(message.chat.id, 'Inteligencia Artificial activada')
    else:
        bot.send_message(message.chat.id, 'Acceso denegado')


@bot.message_handler(commands=['reset'])
def reset(message):
    if message.chat.id == 994286593:
        try:
            bot.send_message(message.chat.id, 'Reiniciando sistema')
            command = ['python', 'friede.py']
            subprocess.run(command)
            subprocess.run(exit())
        except:
            print("Error reiniciando sistema")
            bot.send_message(message.chat.id, 'Error reiniciando sistema')
    else:
        bot.send_message(message.chat.id, 'Acceso denegado')


@bot.message_handler(commands=['friede'])
def friede(message):
    try:
        img = open('friede/img/friede.png', 'rb')
        bot.send_photo(message.chat.id, img)
    except:
        bot.send_message(message.chat.id, 'Error enviando mensaje')


@bot.message_handler(commands=['protect', 'p'])
def protect(message):
    global is_protecting
    if message.chat.id == 994286593:
        if is_protecting:
            print('Error, bot is protecting')
            bot.send_message('994286593', 'Error, bot is already protecting')
            return
        print('Starting protection..')
        is_protecting = True
        bot.send_message('994286593', 'iniciando proteccion..')
        try:
            import protect
        except:
            bot.send_message('994286593', 'Error iniciando proteccion')
    else:
        bot.send_message(message.chat.id, 'Acceso denegado')
    is_protecting = False


@bot.message_handler(commands=['record', 'r'])
def record(message):
    global is_recording
    if message.chat.id == 994286593:
        if is_protecting:
            print('Error, bot is protecting')
            bot.send_message('994286593', 'Error, bot is protecting')
            return
        print('Starting recording..')
        is_recording = True
        bot.send_message('994286593', 'iniciando grabación..')
        try:
            import record
        except:
            bot.send_message('994286593', 'Error iniciando grabacion')
    else:
        bot.send_message(message.chat.id, 'Acceso denegado')
    is_recording = False


@bot.message_handler(commands=['random'])
def random(self, desde: int, hasta: int, cant: int):
    dice = [
        str(random.choice(range(desde, hasta + 1)))
        for _ in range(cant)
    ]
    bot.send_message(', '.join(dice))


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    bot.send_message()


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

@bot.message_handler(commands=['showdatabase'])
def show_db(message):
    try:
        conn = sqlite3.connect('users.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM Users')
        text = ''
        for fila in cur:
            text = text + str(fila) + '\n'
        bot.send_message(message.chat.id, text)
        conn.commit()
        cur.close()
    except:
        bot.send_message(message.chat.id, 'Error with Data Base')


@bot.message_handler(func=lambda message: True)
def search_song(message):
    global ai

    if cmd_on and message.chat.id == 994286593:
        try:
            p = subprocess.run(message.text.split())
            try:
                out = check_output(message.text.split())
                bot.send_message(message.chat.id, str(out))
            except:
                bot.send_message(message.chat.id, 'Trabajo completado, error enviando informacion')
        except:
            bot.send_message(message.chat.id, 'Error in subprocess call')

    if is_searching:
        try:
            query_string = parse.urlencode({'search_query': message.text})
            html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
            print(search_results)
            bot.send_message(message.chat.id, 'Buscando..')
            yt = "https://www.youtube.com/watch?v="
            search1 = yt + search_results[0]
            video1 = YoutubeDL({}).extract_info(search1, download=False)
            name1 = f"{video1['artist']} - {video1['track']}.mp3"
            bot.send_message(message.chat.id, name1)

            url = search1

            ydl_opts = {
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        }

            for file in os.listdir("./"):
                if file.endswith('.mp3') or file.endswith('.webm'):
                    os.remove(file)

            bot.send_message(message.chat.id, 'Descargando y subiendo..')

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    os.rename(file, name1)
            try:
                audio = open(name1, 'rb')
                bot.send_document(message.chat.id, audio)
            except:
                print('Error al subir archivo')
                bot.send_message(message.chat.id, 'Error al subir archivo, recuerda pedir canciones que duren menos de 10 minutos')
        except:
            print('Error al procesar archivo')
            bot.send_message(message.chat.id, 'Error, vuelva a intentalo más tarde x.x')

    if not cmd_on and not is_searching:
        if ai_on:
            ai += ('Human: ' + message.text + '\n')
            generate_response()

            ai += response['choices'][0]['text']
            print(message.text)
            print(response['choices'][0]['text'])
            bot.send_message(message.chat.id, response['choices'][0]['text'][3::])
        else:
            bot.send_message(message.chat.id, 'Mi inteligencia artificial esta actualmente desactivada 😖\nSaludos! =(\n- Friede ❄️')
            print('Error with AI, or AI off')
        


bot.polling(none_stop=False, interval=0, timeout=60)
