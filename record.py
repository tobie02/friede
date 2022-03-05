import telebot
import requests
import os
import cv2
import time
import datetime
from friede import TOKEN

bot = telebot.TeleBot(TOKEN)

cap = cv2.VideoCapture(0)

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v") #('m', 'p', '4', 'v')

timer_started = False
current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
bot.send_message('994286593', 'Started recording')
print("Started recording")

while True:
    _, frame = cap.read()

    if timer_started:
        if time.time() - detection_stopped_time > SECONDS_TO_RECORD_AFTER_DETECTION:
            detection = False
            timer_started = False
            out.release()
            bot.send_message('994286593', 'Stoped recording')
            print("Stoped Recording")
            try:
                video = open(current_time + '.mp4', 'rb')
                bot.send_document('994286593', video)
            except:
                bot.send_message('994286593', 'Error sending video.')
            break
    else:
        timer_started = True
        detection_stopped_time = time.time()

    out.write(frame)

    cv2.imshow("Camera", frame)

out.release()
cap.release()
cv2.destroyAllWindows()