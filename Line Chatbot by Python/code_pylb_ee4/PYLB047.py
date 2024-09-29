from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import google.generativeai as genai
genai.configure(api_key="***************************************")
model = genai.GenerativeModel("gemini-pro")

channel_secret = "***************************************"
channel_access_token = "***************************************"

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
    prompt = text
                
    try:
        response = model.generate_content(prompt)
        text_out = response.text
        #print(text_out)        
    except:
        text_out = "no response"
        #print(text_out)

    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

