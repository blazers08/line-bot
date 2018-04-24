from flask import Flask, request, abort

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    key = event.message.text
    if key == 'profile':
        keyname = line_bot_api.get_profile('Ub1dec77c8763f4e3da7489afffaf7d09')
        message1 = TextMessage(text="Hello Guys, I'm Denny. I'm from Taipei")
        line_bot_api.reply_message(event.reply_token, message1)
        message2 = TextMessage(keyname.display_name)
        line_bot_api.reply_message(event.reply_token, message2)
    elif key == 'confirm':
        confirm_template = ConfirmTemplate(text='Do I have a chance to Intern at Line?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
            # MessageTemplateAction(label='Considering', text='Let me thinl about this!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif key == 'buttons':
        buttons_template = ButtonsTemplate(
            title="Hi I'm Denny", text="Hello Guys, press the button to know more about me", actions=[
                URITemplateAction(
                    label='Go to my github', uri='https://github.com/blazers08'),
                PostbackTemplateAction(
                    label='Denny', data='This is my English name',
                    text='This is my English name'),
                PostbackTemplateAction(
                    label='Show my Chinese name', data='陳禹丞',
                    text='陳禹丞'),
                PostbackTemplateAction(
                    label='Where do I study at?', data='NCCU MIS',
                    text='NCCU MIS'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif key == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to my Chinese RESUME', uri='https://www.cakeresume.com/s--h3xa5Aw4l5GsUbluBUehjg--/denny-chen'),
                PostbackTemplateAction(label='Python', data='I understand Python')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif key == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://imgur.com/gallery/MK2jiAt',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif key == 'hello':
        message4 = TextMessage(text="Hello world")
        line_bot_api.reply_message(event.reply_token, message4)
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))

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
