from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import GT

channel_secret = "xxx"
channel_access_token = "xxxxx"

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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)
    
    text_th = GT.translate(text,'en','th') # en --> th
    print(text_th)
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_th))
        
if __name__ == "__main__":          
    app.run()

