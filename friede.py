from os import system
from time import *
import os

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
