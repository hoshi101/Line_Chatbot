from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            ImageMessage,
                            ImageSendMessage)
import os
import tempfile
import cv2

channel_secret = "d198b2eae368c5363c5f21ab40e68a23"
channel_access_token = "JTiN9V2qMgnRrmEz6Qk8GsTJev9zN2JDRWo0pNf/7jPPhTIgmDzqSM4SOkoBl1PJOMJ9/TcjtYjx78lFoneeWqMtMNiJYN/7Z2ii2Xk9IoFyinABZLrVEDiRnoGBdZMJ9DUdOaKLzXcSTGNskT94SwdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp').replace("\\","/")
    print(static_tmp_path)
    
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='jpg' + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
        
    dist_path = tempfile_path + '.jpg'  # เติมนามสกุลเข้าไปในชื่อไฟล์เป็น jpg-xxxxxx.jpg
    os.rename(tempfile_path, dist_path) # เปลี่ยนชื่อไฟล์ภาพเดิมที่ยังไม่มีนามสกุลให้เป็น jpg-xxxxxx.jpg

    filename_image = os.path.basename(dist_path) # ชื่อไฟล์ภาพ output (ชื่อเดียวกับ input)
    filename_fullpath = dist_path.replace("\\","/")   # เปลี่ยนเครื่องหมาย \ เป็น / ใน path เต็ม
    
    img = cv2.imread(filename_fullpath)

    # ใส่โค้ดประมวลผลภาพตรงส่วนนี้
    #--------------------------------------------------------
    cv2.line(img,(50,50),(200,200),(0,255,0),5)         #color(BGR)
    cv2.rectangle(img,(200,50),(250,150),(0,0,255),10)
    cv2.circle(img,(120,120),30,(0,255,255),8)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,"LINE Chatbot",(20,300),font,5.5,(255,255,0),3)
    #--------------------------------------------------------
    
    cv2.imwrite(filename_fullpath,img)
    
    dip_url = request.host_url + os.path.join('static', 'tmp', filename_image).replace("\\","/")
    print(dip_url)
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='ประมวลผลภาพเรียบร้อยแล้ว'),
            ImageSendMessage(dip_url,dip_url)])
    
@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)

if __name__ == "__main__":          
    app.run()

