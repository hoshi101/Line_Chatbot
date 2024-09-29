from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import random
from wit import Wit

channel_secret = "d198b2eae368c5363c5f21ab40e68a23"
channel_access_token = "JTiN9V2qMgnRrmEz6Qk8GsTJev9zN2JDRWo0pNf/7jPPhTIgmDzqSM4SOkoBl1PJOMJ9/TcjtYjx78lFoneeWqMtMNiJYN/7Z2ii2Xk9IoFyinABZLrVEDiRnoGBdZMJ9DUdOaKLzXcSTGNskT94SwdB04t89/1O/w1cDnyilFU="

wit_access_token = "NWR4IC3SVPNFUKPOUA65TRQ4RFT3WAVD"
client = Wit(wit_access_token)

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

answer_caption = ["ความโสดอาจทำให้เหงา 😔 แต่ถ้า MARS เป็นแฟนเรา ไม่มีเหงาแน่นอน! 🚀💫","อยากเกิดเป็นดวงจันทร์จัง 🌕 ที่ยังมีดวงดาวอยู่เคียงข้างทุกค่ำคืน ✨🌠","ดูดาวคนเดียวอาจจะทำให้เหงา ลองมานั่งดูกับเราอาจจะหายเหงาก็ได้นะ อิอิ^^"]
answer_against = ["มีอะไรให้ช่วยไหม?","นี่คือข้อความอัตโนมัติ ถ้าคุณสงสัยตรงไหนรบกวนพิมพ์ข้อความที่สอดคล้องกับเรื่องนั้นๆ","อยากรู้จักดาวอะไรพิมพ์มาเลยย~","พิมพ์ชื่อดาวของคุณ"]

first_greeting = True
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global first_greeting
    text = event.message.text
    print(text)
    
    if (text != ""):
        ret = client.message(text)
        if len(ret["intents"]) > 0:
            confidence = ret["intents"][0]['confidence']
            
            if (confidence > 0.8):
                intents_name = ret["intents"][0]['name']        
                print("intent = ",intents_name)

                if (intents_name=="greeting"):
                    if first_greeting:
                        text_out = "สวัสดี! ฉันคือบอทไกด์ผู้เชี่ยวชาญเรื่องดาวฤกษ์! 🌟 ถ้าคุณหลงใหลในความมหัศจรรย์ของจักรวาลและอยากรู้เรื่องราวของดาวฤกษ์แต่ละดวง ไม่ว่าจะเป็นดาวยักษ์ใหญ่ ดาวแคระ หรือดาวที่เปล่งแสงสว่างที่สุดในท้องฟ้า มาร่วมเดินทางสำรวจดวงดาวกับฉันกันเถอะ! 🚀✨ ฉันพร้อมจะพาคุณท่องไปในห้วงอวกาศและเรียนรู้เรื่องราวน่าทึ่งของดวงดาวต่างๆ อย่างสนุกสนานและเต็มไปด้วยความรู้! 🌠"
                        first_greeting = False
                    else:
                        idx = random.randint(0,len(answer_against)-1)
                        text_out = answer_against[idx]
                        #text_out = "มีอะไรให้บอทช่วยไหม?"
                    line_bot_api.reply_message(event.reply_token,
                                               TextSendMessage(text=text_out))
                                        
                if (intents_name=="date"):
                    text_out = "วันนี้วันพระ"
                    line_bot_api.reply_message(event.reply_token,
                                               TextSendMessage(text=text_out))

                if (intents_name=="caption"):
                    idx = random.randint(0,len(answer_caption)-1)
                    text_out = answer_caption[idx]
                    line_bot_api.reply_message(event.reply_token,
                                               TextSendMessage(text=text_out))
                    
            else:
                print("intent = unknow")
                text_out = "บอทไม่เข้าใจจ กรุณาถามใหม่อีกครั้งได้ไหมคะ?"
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text=text_out))
        else:
            print("intent = unknow")
            text_out = "ฉันไม่เข้าใจสิ่งที่คุณถาม กรุณาถามใหม่อีกครั้ง"
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=text_out))
            
if __name__ == "__main__":          
    app.run()

