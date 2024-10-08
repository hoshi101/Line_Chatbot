from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            StickerSendMessage)

import random

channel_secret = "xxxxxxxxxxxxxxxxxxxxxxxx"
channel_access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

play_status = False
letter = ''

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global play_status,letter
    text = event.message.text
    print(text)

    if not play_status:
        if text == "let's play game":
            letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') #A-Z
            print(letter)
            text_out = "Guess the letter from A to Z! Let's have some fun!"
            print(text_out)
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=text_out))
            play_status = True


    elif play_status:
        guess = text.upper()
        if guess == letter:
            text_out = "That's correct! You're amazing!"
            print(text_out)
            p_id = 11537 
            s_id = 52002734 
            line_bot_api.reply_message(event.reply_token,
                                       [TextSendMessage(text=text_out),
                                        StickerSendMessage(package_id=p_id,
                                                           sticker_id=s_id)])
            play_status = False
    #if (play_status == True): 
        #num = int(text) # "50" --> 50
        #if (num == number): #num ผู้เล่นพิมพ์เข้ามา , number เลขโจทย์
          #  50 == 18
            #text_out = "ถูกต้องนะครับ เก่งจริงๆ"
            #print(text_out)
            #p_id = 11537 
            #s_id = 52002734 
            #line_bot_api.reply_message(event.reply_token,
                                       #[TextSendMessage(text=text_out),
                                        #StickerSendMessage(package_id=p_id,
                                                           #sticker_id=s_id)])
            
        else: #ตอบผิด
            if guess > letter:
                text_out = "Too high! Try a smaller letter."
                print(text_out)
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text=text_out))
            else:              
                text_out = "Too low! Try a bigger letter."
                print(text_out)
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()
