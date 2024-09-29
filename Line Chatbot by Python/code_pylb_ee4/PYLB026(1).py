from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            TemplateSendMessage,
                            MessageAction,
                            CarouselTemplate,
                            CarouselColumn,
                            ImageSendMessage)

channel_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
channel_access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

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
       
    if text == 'กลุ่มดาวฤกษ์มีอะไรบ้าง':
        # กำหนดได้ไม่เกิน 10 อัน
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(title='กลุ่มดาวนายพราน',text='กลุ่มดาวนายพราน (Orion)', actions=[
                MessageAction(label='รายละเอียด',text='รายละเอียดของ กลุ่มดาวนายพราน'),
                MessageAction(label='รูปตัวอย่าง', text='รูปกลุ่มดาวนายพราน')]),
            
            CarouselColumn(title='กลุ่มดาวลูกไก่',text='กลุ่มดาวลูกไก่ (Pleiades)', actions=[
                MessageAction(label='รายละเอียด',text='รายละเอียดของ กลุ่มดาวลูกไก่'),
                MessageAction(label='รูปตัวอย่าง', text='รูปกลุ่มดาวลูกไก่')]),

            CarouselColumn(title='กลุ่มดาวหมีเล็ก',text='กลุ่มดาวหมีเล็ก (Ursa Minor)', actions=[
                MessageAction(label='รายละเอียด',text='รายละเอียดของ กลุ่มดาวหมีเล็ก'),
                MessageAction(label='รูปตัวอย่าง', text='รูปกลุ่มดาวหมีเล็ก')]),

            CarouselColumn(title='กลุ่มดาวหมีใหญ่',text='กลุ่มดาวหมีใหญ่ หรือ จระเข้ (Ursa Major)', actions=[
                MessageAction(label='รายละเอียด',text='รายละเอียดของ ดาวหมีใหญ่'),
                MessageAction(label='รูปตัวอย่าง', text='รูปกลุ่มดาวหมีใหญ่')]),
        ])
        template_message = TemplateSendMessage(alt_text='Hello',
                                               template=carousel_template)
        line_bot_api.reply_message(event.reply_token,template_message)
        
    if text == 'รายละเอียดของ กลุ่มดาวนายพราน':
        text_out = "กลุ่มดาวนายพราน ประกอบด้วยดวงดาว 3 ดวง เรียงต่อกันเป็นรูปเข็มขัดของนายพราน และดวงอื่นๆ ที่ลากเส้นต่อกันแล้วเหมือนรูปคันธนู มีแสงสว่างปานกลาง ผู้ที่อยู่ซีกโลกเหนือสังเกตเห็นได้ในช่วงเย็นของเดือนตุลาคม ถึง มกราคม คนไทยรู้จักในชื่อกลุ่มดาวเต่า ดาวดวงที่สว่างที่สุดคือ “ดาวไรเจล”"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))

    if text == 'รูปกลุ่มดาวนายพราน':
        url = request.url_root + '/static/Screenshot 2024-05-26 120604.png'
        line_bot_api.reply_message(event.reply_token,
                                   ImageSendMessage(url,url))

    if text == 'รายละเอียดของ กลุ่มดาวลูกไก่':
        text_out = "กลุ่มดาวลูกไก่ ภาษาอังกฤษคือ Pleiades เป็นส่วนหนึ่งในนิทานพื้นบ้านของหลายประเทศ ประกอบด้วยดาวฤกษ์สีน้ำเงิน 7 ดวง มองเห็นได้ด้วยตาเปล่า"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))

    if text == 'รูปกลุ่มดาวลูกไก่':
        url = request.url_root + '/static/Screenshot 2024-05-26 120620.png'
        line_bot_api.reply_message(event.reply_token,
                                   ImageSendMessage(url,url))
        
    if text == 'รายละเอียดของ กลุ่มดาวหมีเล็ก':
        text_out = "กลุ่มดาวหมีเล็กประกอบด้วยดาวฤกษ์สว่างจ้า 3 ดวง หนึ่งในนั้นคือดาวเหนือ เป็นดาวที่มีความสำคัญมาตั้งแต่อดีต ใช้เป็นดาวนำทาง ชาวกรีกเรียกว่า ดาวหมีตัวเล็ก ชาวจีนเรียกว่าราชรถแห่งสวรรค์"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))

    if text == 'รูปกลุ่มดาวหมีเล็ก':
        url = request.url_root + '/static/Screenshot 2024-05-26 120614.png'
        line_bot_api.reply_message(event.reply_token,
                                   ImageSendMessage(url,url))
        
    if text == 'รายละเอียดของ ดาวหมีใหญ่':
        text_out = "กลุ่มดาวหมีใหญ่ประกอบด้วยดาวฤกษ์ 7 ดวงเรียงกันเป็นรูปกระบวยน้ำ หรือบางชนชาติเรียกว่า กลุ่มดาวกระบวยใหญ่ กลุ่มดาวนี้ตั้งอยู่ทางทิศเหนือทางขอบฟ้าทิศตะวันออกเฉียงเหนือ"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))

    if text == 'รูปกลุ่มดาวหมีใหญ่':
        url = request.url_root + '/static/Screenshot 2024-05-26 120611.png'
        line_bot_api.reply_message(event.reply_token,
                                   ImageSendMessage(url,url))

@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)
         
if __name__ == "__main__":          
    app.run()

