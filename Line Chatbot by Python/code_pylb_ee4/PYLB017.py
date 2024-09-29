from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

channel_secret = "d198b2eae368c5363c5f21ab40e68a23"
channel_access_token = "JTiN9V2qMgnRrmEz6Qk8GsTJev9zN2JDRWo0pNf/7jPPhTIgmDzqSM4SOkoBl1PJOMJ9/TcjtYjx78lFoneeWqMtMNiJYN/7Z2ii2Xk9IoFyinABZLrVEDiRnoGBdZMJ9DUdOaKLzXcSTGNskT94SwdB04t89/1O/w1cDnyilFU="

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
                
    if (text.startswith("คำนวณ")): # "คำนวณ 4+6" 
        text_math = text.strip("คำนวณ").replace(" ", "") #--> " 4+6" --> "4+6"
        print(text_math)
        try:
            result = eval(text_math) # 10 --> "10"
            text_out = "เท่ากับ " + str(result)
            print(text_out)
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=text_out))
        except:
            pass
        
if __name__ == "__main__":          
    app.run()

