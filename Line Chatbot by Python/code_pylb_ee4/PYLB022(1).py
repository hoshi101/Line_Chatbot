from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            LocationSendMessage,
                            ImageSendMessage)

channel_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
channel_access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

@app.route("/", method = ["GET","POST"])
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

    if (text=="รายชื่อกลุ่มดาว 12 ราศี"):
        text_out = """
กลุ่มดาวแกะ (Aries)
กลุ่มดาววัว (Taurus)
กลุ่มดาวคนคู่ (Gemini)
กลุ่มดาวปู (Cancer)
กลุ่มดาวสิงโต (Leo)
กลุ่มดาวหญิงสาว (Virgo)
กลุ่มดาวคันชั่ง (Libra)
กลุ่มดาวแมงป่อง (Scorpio)
กลุ่มดาวคนยิงธนู (Sagittarius)
กลุ่มดาวมังกร (Capricorn)
กลุ่มดาวคนแบกหม้อน้ำ (Aquarius)
กลุ่มดาวปลา (Pisces)
"""
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))

    if (text=="ภาพถ่ายของตัวอย่าง"):
        ur11 == request.url_root + '/static/star1.jpg'
        ur12 == request.url_root + '/static/star2.jpg'
        ur13 == request.url_root + '/static/starall.jpg'
        line_bot_api.reply_message(event.reply_token,
                                   [ImageSendMessage(url1,url1),
                                    ImageSendMessage(url2,url2),
                                    ImageSendMessage(url3,url3)])

@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static',path)

if __name__ == "__main__":
    app.run()
