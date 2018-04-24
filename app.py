from flask import Flask, request, abort

import requests
import re
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

# line_bot_api.push_message('Ub1dec77c8763f4e3da7489afffaf7d09', TextSendMessage(text="I'll give you some hints to let you know how touse it"))
# tips = TextMessage(text="You can type some keywords: profile, confirm, buttons, carousel, image_carousel, hello, sticker or 貼圖")
# line_bot_api.reply_message(event.reply_token, tips)
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
    if event.message.text == "eyny":
        content = eyny_movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "蘋果即時新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "PTT 表特版 近期大於 10 推的文章":
        content = ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "來張 imgur 正妹圖片":
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    if event.message.text == "隨便來張正妹圖片":
        image = requests.get(API_Get_Image)
        url = image.json().get('Url')
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    if event.message.text == "近期熱門廢文":
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "即時廢文":
        content = ptt_gossiping()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "近期上映電影":
        content = movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "科技新報":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "PanX泛科技":
        content = panx()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "開始玩":
        buttons_template = TemplateSendMessage(
            alt_text='開始玩 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='新聞',
                        text='新聞'
                    ),
                    MessageTemplateAction(
                        label='電影',
                        text='電影'
                    ),
                    MessageTemplateAction(
                        label='看廢文',
                        text='看廢文'
                    ),
                    MessageTemplateAction(
                        label='正妹',
                        text='正妹'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "新聞":
        buttons_template = TemplateSendMessage(
            alt_text='新聞 template',
            template=ButtonsTemplate(
                title='新聞類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                actions=[
                    MessageTemplateAction(
                        label='蘋果即時新聞',
                        text='蘋果即時新聞'
                    ),
                    MessageTemplateAction(
                        label='科技新報',
                        text='科技新報'
                    ),
                    MessageTemplateAction(
                        label='PanX泛科技',
                        text='PanX泛科技'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "電影":
        buttons_template = TemplateSendMessage(
            alt_text='電影 template',
            template=ButtonsTemplate(
                title='服務類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/sbOTJt4.png',
                actions=[
                    MessageTemplateAction(
                        label='近期上映電影',
                        text='近期上映電影'
                    ),
                    MessageTemplateAction(
                        label='eyny',
                        text='eyny'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "看廢文":
        buttons_template = TemplateSendMessage(
            alt_text='看廢文 template',
            template=ButtonsTemplate(
                title='你媽知道你在看廢文嗎',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/ocmxAdS.jpg',
                actions=[
                    MessageTemplateAction(
                        label='近期熱門廢文',
                        text='近期熱門廢文'
                    ),
                    MessageTemplateAction(
                        label='即時廢文',
                        text='即時廢文'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "正妹":
        buttons_template = TemplateSendMessage(
            alt_text='正妹 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/qKkE2bj.jpg',
                actions=[
                    MessageTemplateAction(
                        label='PTT 表特版 近期大於 10 推的文章',
                        text='PTT 表特版 近期大於 10 推的文章'
                    ),
                    MessageTemplateAction(
                        label='來張 imgur 正妹圖片',
                        text='來張 imgur 正妹圖片'
                    ),
                    MessageTemplateAction(
                        label='隨便來張正妹圖片',
                        text='隨便來張正妹圖片'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='選擇服務',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/kzi5kKy.jpg',
            actions=[
                MessageTemplateAction(
                    label='開始玩',
                    text='開始玩'
                ),
                URITemplateAction(
                    label='影片介紹 阿肥bot',
                    uri='https://youtu.be/1IxtWgWxtlE'
                ),
                URITemplateAction(
                    label='如何建立自己的 Line Bot',
                    uri='https://github.com/twtrubiks/line-bot-tutorial'
                ),
                URITemplateAction(
                    label='聯絡作者',
                    uri='https://www.facebook.com/TWTRubiks?ref=bookmarks'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)
    # # tips = TextMessage(text="You can type some keywords: profile, confirm, buttons, carousel, image_carousel, hello, sticker or 貼圖")
    # # line_bot_api.reply_message(event.reply_token, tips)
    # # line_bot_api.push_message('Ub1dec77c8763f4e3da7489afffaf7d09', TextSendMessage(text="I'll give you some hints to let you know how touse it"))
    # print("event.reply_token:", event.reply_token)
    # print("event.message.text:", event.message.text)
    # key = event.message.text
    # if key == 'profile':
    #     message1 = TextMessage(text="Hello Guys, I'm Denny. I come from Taipei")
    #     line_bot_api.reply_message(event.reply_token, message1)
    # #     profile = line_bot_api.get_profile('Ub1dec77c8763f4e3da7489afffaf7d09')
    # #     line_bot_api.reply_message(event.reply_token, TextMessage(text='Display name: ' + profile.display_name))
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
    #     return 0
    # buttons_template = TemplateSendMessage(
    #     alt_text='目錄 template',
    #     template=ButtonsTemplate(
    #         title='選擇服務',
    #         text='請選擇',
    #         thumbnail_image_url='https://i.imgur.com/kzi5kKy.jpg',
    #         actions=[
    #             MessageTemplateAction(
    #                 label='buttons',
    #                 text='buttons'
    #             ),
    #             URITemplateAction(
    #                 label='影片介紹 阿肥bot',
    #                 uri='https://youtu.be/1IxtWgWxtlE'
    #             ),
    #             URITemplateAction(
    #                 label='如何建立自己的 Line Bot',
    #                 uri='https://github.com/twtrubiks/line-bot-tutorial'
    #             ),
    #             URITemplateAction(
    #                 label='聯絡作者',
    #                 uri='https://www.facebook.com/TWTRubiks?ref=bookmarks'
    #             )
    #         ]
    #     )
    # )
    # line_bot_api.reply_message(event.reply_token, buttons_template)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
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
