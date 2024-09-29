from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            ImageMessage,
                            ImageSendMessage,
                            StickerSendMessage)
import os
import tempfile
from PIL import Image

import google.generativeai as genai
genai.configure(api_key="AIzaSyDmnTGlifPXbV3fUH6hm9oZ2msEYlcJ5pc")
model = genai.GenerativeModel("gemini-pro-vision")

channel_secret = "d198b2eae368c5363c5f21ab40e68a23"
channel_access_token = "JTiN9V2qMgnRrmEz6Qk8GsTJev9zN2JDRWo0pNf/7jPPhTIgmDzqSM4SOkoBl1PJOMJ9/TcjtYjx78lFoneeWqMtMNiJYN/7Z2ii2Xk9IoFyinABZLrVEDiRnoGBdZMJ9DUdOaKLzXcSTGNskT94SwdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

@app.route("/", methods=["GET", "POST"])
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

    if text.lower() == "คำตอบถูกต้อง":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="เย้!🥳"),
                StickerSendMessage(package_id='11539', sticker_id='52114131')
            ]
        )
        return
    
    if text.lower() == "คำตอบผิด":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="เสียใจจุงง 🥺"),
                StickerSendMessage(package_id='11539', sticker_id='52114138')
            ]
        )
        return
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="ฉันไม่เข้าใจข้อความที่คุณส่งมา?")
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp').replace("\\", "/")
    print(static_tmp_path)
    
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='jpg' + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
        
    dist_path = tempfile_path + '.jpg'
    os.rename(tempfile_path, dist_path)

    filename_image = os.path.basename(dist_path)
    filename_fullpath = dist_path.replace("\\", "/")
    
    img = Image.open(filename_fullpath)

    # ใส่โค้ดประมวลผลภาพตรงส่วนนี้
    #-------------------------------------------------------------
    prompt = "จากรูปนี้คือกลุ่มดาวอะไร"
    print("prompt : ", prompt)

    try:
        response = model.generate_content([img, prompt])
        text_out = response.text
    except Exception as e:
        text_out = "no response"
        print("Error:", e)
    #-------------------------------------------------------------
        
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run()
