from os import system
from time import *
import os

TOKEN = '2006904933:AAEMcjtXkNfQsmZW6IrLzc2rCvSWHsVj_NU'

if __name__ == '__main__':
    print("""
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░█▀▀▀░█▀▀█░░█░░█▀▀▀░█▀▀█░█▀▀▀░
    ░█▀▀▀░█▀▀░░░█░░█▀▀░░█░░█░█▀▀░░
    ░▀░░░░▀░░▀░░▀░░▀▀▀▀░▀▀▀░░▀▀▀▀░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    """)

    try:
        import telegrambot
    except:
        print('Execute the installer first.')
        sleep(15) 

#well shit
