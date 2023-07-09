import telebot
import requests
import numpy as np
import cv2
import io

# Create bot
bot = telebot.TeleBot(<BOT_TOKEN>)

# Alowed users
allowed_user = []

# Admins
admin_users = []

# Chat to send errors and usages
TARGET_CHAT_ID = ''

#queue
queue = []

# Request to stable diffusion
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1" 
headers = {"Authorization": "Bearer <HUGGINGFACE_TOKEN>"} 
def diffusion(payload): 
    response = requests.post(API_URL, headers=headers, json=payload) 
    return response.content 

###############################################################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I'm a bot for generating images with stable diffusion, write /help to output details")
###############################################################
@bot.message_handler(commands=['help'])
def send_Help(message):
    bot.reply_to(message, "Enter /stablediffusion for generation image with your prompt\nContacts - @<YOUR_USE>")
#################################################################
@bot.message_handler(commands=["report"])
def report(message):
    global message_text
    If message.chat.id in allowed_group or (message.from_user.id in allowed_user and message.chat.type == "private"):
        sobaka = message.from_user.username
        check = message.text
        check = check.replace("/report", "")
        check = check.replace("@<BOT_USE>", "")
        if check != "":
            bot.reply_to(message, "Message sent successfully")
            bot.send_message(chat_id=TARGET_CHAT_ID, text="Report:\n@" + sobaka + " : " + check)
        else:
            bot.reply_to(message, "The request cannot be blank.")
    else:
        bot.reply_to(message, "You have no access.")
#################################################################
@bot.message_handler(commands=['ad'])
def ad(message):
    global message_text
    if (message.from_user.id in admin_users):
        message_text = message.text
        message_text = message_text.replace("/ad", "")
        message_text = message_text.replace("@<BOT_USE>", "")
        users = 0
        bot.reply_to(message, 'ads are being sent...')
        for user in allowed_user:
            time.sleep(5)
            bot.send_message(user, message_text)
        bot.reply_to(message, 'Ads sent successfully, number of recipients:' + users)
    else:
        bot.reply_to(message, 'You are not an administrator.')
#################################################################
@bot.message_handler(commands=['stablediffusion'])
def stablediffusion(message):
    global message_text
    if message.chat.id in allowed_group or (message.from_user.id in allowed_user and message.chat.type == 'private'):
        use = message.from_user.username
        if use is not in queue:
            check = message.text.replace("/stablediffusion", "").replace("@<BOT_USE>", "").strip()
            if check != "":
                queue.append(use)
                bot.reply_to(message, 'Wait... \n{your position in the queue: {}'.format(len(queue))
                try:
                    image_bytes = query4({'inputs': check,})
                    img_bytes = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                    success, png_image = cv2.imencode('.png', img_bytes)
                    photo = io.BytesIO(png_image)
                    photo.seek(0)
                    bot.send_message(message.chat.id, text=f "Request: {check}\nStable Diffusion:")
                    bot.send_photo(message.chat.id, photo)
                    image_bytes = query4({"inputs": check,})
                    img_bytes = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                    success, png_image = cv2.imencode('.png', img_bytes)
                    photo = io.BytesIO(png_image)
                    photo.seek(0)
                    bot.send_message(chat_id=TARGET_CHAT_ID, text=f "AI Model: Stable Diffusion \n@{use} {check}\nStable Diffusion:")
                    bot.send_photo(TARGET_CHAT_ID, photo)
                except Exception as e:
                    bot.reply_to(message, "Error: Admin is already working on fixing it")
                    bot.send_message(chat_id=TARGET_CHAT_ID, text="AI Model: Stability AI Stable Diffusion\ error: " + str(e))
                queue.remove(use)
            else:
                bot.reply_to(message, 'Request cannot be empty.')
        else:
            bot.reply_to(message, "You are already generating a query for this model, wait for completion.")
    else:
        bot.reply_to(message, 'You do not have access.')
################################################################
