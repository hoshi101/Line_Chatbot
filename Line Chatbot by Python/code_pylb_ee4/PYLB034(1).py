from flask import Flask, request, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            StickerSendMessage)

from openpyxl import load_workbook
import time

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

    dt = time.localtime()
    DD = '{:02d}'.format(dt[2]) + '/' + '{:02d}'.format(dt[1]) + '/' + str(dt[0])
    TT = '{:02d}'.format(dt[3]) + ':' + '{:02d}'.format(dt[4]) + ':' + '{:02d}'.format(dt[5])
    print(DD)
    print(TT)

    xlsx_filename='3DAFB000.xlsx'
    wb = load_workbook(xlsx_filename)
    ws = wb['Sheet1']
    ws.append([DD,TT,text])
    wb.save(xlsx_filename)
    
    text_out = "บันทึกดาวประจำวัน เรียบร้อย!"
    p_id = 11539
    s_id = 52114110
    line_bot_api.reply_message(event.reply_token,
                               [TextSendMessage(text=text_out),
                               StickerSendMessage(package_id=p_id,
                                                  sticker_id=s_id)])
    
if __name__ == "__main__":          
    app.run()

