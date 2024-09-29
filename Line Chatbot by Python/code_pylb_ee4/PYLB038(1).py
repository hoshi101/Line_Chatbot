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
import numpy as np

channel_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
channel_access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

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
    #---------------------------------------------------------
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # กำหนดช่วงสีสำหรับสีขาว
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 55, 255])

    # กำหนดช่วงสีสำหรับสีฟ้าอ่อน
    lower_light_blue = np.array([90, 50, 50])
    upper_light_blue = np.array([130, 255, 255])

    # กำหนดช่วงสีสำหรับสีเหลืองอ่อน
    lower_light_yellow = np.array([20, 100, 100])
    upper_light_yellow = np.array([30, 255, 255])

    # สร้างมาสก์สำหรับแต่ละสี
    mask_white = cv2.inRange(imgHSV, lower_white, upper_white)
    mask_light_blue = cv2.inRange(imgHSV, lower_light_blue, upper_light_blue)
    mask_light_yellow = cv2.inRange(imgHSV, lower_light_yellow, upper_light_yellow)

    # รวมมาสก์ทั้งหมดเข้าด้วยกัน
    combined_mask = cv2.bitwise_or(mask_white, mask_light_blue)
    combined_mask = cv2.bitwise_or(combined_mask, mask_light_yellow)

    # หาขอบเขตของวัตถุที่พบในมาสก์รวม
    contours, hierarchy = cv2.findContours(combined_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    num = 0
    if len(contours) > 0: # พบวัตถุที่ตรงกับสีที่กำหนด
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 0: # สนใจวัตถุที่มีพื้นที่ใหญ่กว่า 10 พิกเซลขึ้นไป
                num = num + 1
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #---------------------------------------------------------    
    cv2.imwrite(filename_fullpath, img)
    
    dip_url = request.host_url + os.path.join('static', 'tmp', filename_image).replace("\\","/")
    print(dip_url)
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='ประมวลผลภาพเรียบร้อยแล้ว พบดาวบนท้องฟ้าจำนวน ' + str(num) + " ดวง"),
            ImageSendMessage(dip_url,dip_url)])
    
@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)

if __name__ == "__main__":          
    app.run()
