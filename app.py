from flask import Flask, request, abort

import requests
import re
import random
from bs4 import BeautifulSoup

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('lgEV9AezXnZPQ8tSLM//vT6pHGZQJr8F1UBAna2tKy+9NFeSrX2WaN+aWR4EbDQNvViWwtojQhwgh60bOC9pETQ2P76r0mire69AkjQE7oDJM+W0rSGb7A0Dlf3qlRrDa3+CJ6otWqkginyrDlX3XwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c9163e321b81963cb22565a2e08d6983')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/callback", methods=['POST'])
def apple_news():
    target_url = 'http://www.appledaily.com.tw/realtimenews/section/new/'
    head = 'http://www.appledaily.com.tw'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 15:
            return content
        if head in data['href']:
            link = data['href']
        else:
            link = head + data['href']
        content += '{}\n\n'.format(link)
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    
    if event.message.text == "了解陳禹丞":
        buttons_template = TemplateSendMessage(
            alt_text='關於我 template',
            template=ButtonsTemplate(
                title='基本資料',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/PiuLljM.png',
                actions=[
                    MessageTemplateAction(
                        label='自我介紹',
                        text='自我介紹'
                    ),
                    MessageTemplateAction(
                        label='研究方向',
                        text='研究方向'
                    ),
                    MessageTemplateAction(
                        label='技能與課程',
                        text='技能與課程'
                    ),
                    MessageTemplateAction(
                        label='對於Line實習的期望',
                        text='對於Line實習的期望'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    if event.message.text == "實習經驗":
        content = "1.以誠研發：\n主要是利用python做寫了三支資料分析的程式及處理，並將部分資料從MongoDB放置MySQL中。\n2.Mattel, Inc.:\n主要在做新技術的研究，例如FireBase with Redux等技術。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0    

    if event.message.text == "自我介紹":
        content = "大家好我的名字叫陳禹丞，目前就讀政大資管所。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "研究方向":
        content = "我的研究方向為金融科技專利的趨勢與對於公司的營運績效。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0 

    if event.message.text == "對於Line實習的期望":
        content = "如果有機會獲取這份職缺"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "技能與課程":
        content = "如果有機會獲取這份職缺"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if key == '蘋果新聞':
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=content))
        return 0

    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='關於我',
            text='請選擇想知道些什麼',
            thumbnail_image_url='https://i.imgur.com/LCJ66TB.png',
            actions=[
                MessageTemplateAction(
                    label='了解陳禹丞',
                    text='了解陳禹丞'
                ),
                URITemplateAction(
                    label='中文履歷',
                    uri='https://www.cakeresume.com/s--h3xa5Aw4l5GsUbluBUehjg--/denny-chen'
                ),
                MessageTemplateAction(
                    label='實習經驗',
                    text='實習經驗'
                ),
                URITemplateAction(
                    label='Go To My Github',
                    uri='https://github.com/blazers08'
                ),
                MessageTemplateAction(
                    label='蘋果新聞',
                    text='蘋果新聞'
                ),

            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)
    # key = event.message.text
    # if key == 'profile':
    #     message1 = TextMessage(text="Hello Guys, I'm Denny. I come from Taipei")
    #     line_bot_api.reply_message(event.reply_token, message1)
    #     profile = line_bot_api.get_profile('Ub1dec77c8763f4e3da7489afffaf7d09')
    #     line_bot_api.reply_message(event.reply_token, TextMessage(text='Display name: ' + profile.display_name))
    #     return 0
    # elif key == 'confirm':
    #     confirm_template = ConfirmTemplate(text='Do I have a chance to Intern at Line?', actions=[
    #         MessageTemplateAction(label='Yes', text='Yes!'),
    #         MessageTemplateAction(label='No', text='No!'),
    #     ])
    #     template_message = TemplateSendMessage(
    #         alt_text='Confirm alt text', template=confirm_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    #     return 0
    # elif key == 'buttons': 
    #     buttons_template = TemplateSendMessage(
    #         alt_text='Buttons template', template=ButtonsTemplate(
    #             title="Hi I'm Denny", text="Hello Guys, press the button to know more about me", 
    #             actions=[
    #             URITemplateAction(
    #                 label='Go to my github', uri='https://github.com/blazers08'),
    #             # MessageTemplateAction(
    #             #     label='Denny', data='This is my English name',
    #             #     text='This is my English name'),
    #             MessageTemplateAction(
    #                 label='Show my Chinese name', data='陳禹丞',
    #                 text='陳禹丞'),
    #             MessageTemplateAction(
    #                 label='Where do I study at?', data='NCCU MIS',
    #                 text = "I study at NCCU MIS")
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, template_message)
    #     return 0
    # elif key == 'news':
    #     content = apple_news()
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextMessage(text=content))
    #     return 0
    # elif key == 'carousel':
    #     buttons_template = TemplateSendMessage(columns=[
    #         CarouselColumn(text='RESUME', title='RESUME', actions=[
    #             URITemplateAction(
    #                 label='Chinese RESUME', uri='https://www.cakeresume.com/s--h3xa5Aw4l5GsUbluBUehjg--/denny-chen'),
    #             # PostbackTemplateAction(label='ping', data='ping')
    #         ]),
    #         CarouselColumn(text='About me', title='Skills', actions=[
    #             PostbackTemplateAction(
    #                 label='ping with text', data='ping',
    #                 text='Python'),
    #             # MessageTemplateAction(label='Translate Rice', text='米')
    #         ]),
    #     ])
    #     buttons_template = TemplateSendMessage(
    #         alt_text='Carousel alt text', template=buttons_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    #     return 0
    # elif key == 'image_carousel':
    #     image_carousel_template = ImageCarouselTemplate(columns=[
    #         ImageCarouselColumn(image_url='https://via.placeholder.com/350x150',
    #                             action=DatetimePickerTemplateAction(label='datetime',
    #                                                                 data='datetime_postback',
    #                                                                 mode='datetime')),
    #         ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
    #                             action=DatetimePickerTemplateAction(label='date',
    #                                                                 data='date_postback',
    #                                                                 mode='date'))
    #     ])
    #     template_message = TemplateSendMessage(
    #         alt_text='ImageCarousel alt text', template=image_carousel_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    #     return 0
    # elif key == 'hello':
    #     message4 = TextMessage(text="Hello world")
    #     line_bot_api.reply_message(event.reply_token, message4)
    #     return 0
    # elif key == 'sticker' or '貼圖':
    #     line_bot_api.reply_message(
    #     event.reply_token,
    #     StickerSendMessage(
    #         package_id='1',
    #         sticker_id='100'
    #     ))
    #     return 0
    # else:
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # int(number) = random.randint(1,17)
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
    )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
