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
        profile = line_bot_api.get_profile('Ub1dec77c8763f4e3da7489afffaf7d09')
        message1 = TextMessage(text="Hello Guys, I'm Denny. I'm from Taipei")
        line_bot_api.reply_message(event.reply_token, message1)
        message2 = TextMessage(Texprofile.display_name)
        line_bot_api.reply_message(event.reply_token, message2)
    elif key == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif key == 'buttons':
        buttons_template = ButtonsTemplate(
            title="Hi I'm Denny", text="Hello Guys, press the button to know more about me", actions=[
                URITemplateAction(
                    label='Go to my github', uri='https://github.com/blazers08'),
                PostbackTemplateAction(label='Denny', data='This is my English name'),
                PostbackTemplateAction(
                    label='Show my Chinese name', data='陳禹丞',
                    text='陳禹丞'),
                MessageTemplateAction(label='Translate NCCU', text='國立政治大學')
            ])
            # title='Hi I\'m Denny', text='Hello Guys, press the button to know more about me', actions=[
            #     URITemplateAction(
            #         label='Go to my github', uri='https://github.com/blazers08'),
            #     URITemplateAction(
            #         label='This is my Chinese RESUME', uri='https://www.cakeresume.com/s--h3xa5Aw4l5GsUbluBUehjg--/denny-chen'),
            #     PostbackTemplateAction(label='Denny', data='This is my English name'),
            #     PostbackTemplateAction(
            #         label='Show my Chinese name', data='陳禹丞',
            #         text='陳禹丞'),
            #     PostbackTemplateAction(
            #         label='What is my major?', data='MIS',
            #         text='MIS'),
            #     PostbackTemplateAction(
            #         label='Where do I study at?', data='NCCU',
            #         text='NCCU'),
            #     MessageTemplateAction(label='Translate NCCU', text='國立政治大學')
            # ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="You can't leave me"))
    elif key == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='Github', title='Github', actions=[
                URITemplateAction(
                    label='Go to my github', uri='https://github.com/blazers08'),
                PostbackTemplateAction(label='ping', data='ping')
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
            ImageCarouselColumn(image_url='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiD4_iQgdHaAhWGjJQKHaaUAuEQjRx6BAgAEAU&url=https%3A%2F%2Fzh.wikipedia.org%2Fwiki%2FLINE_(%25E5%2585%25AC%25E5%258F%25B8)&psig=AOvVaw3weDrPdoHyID9jCSaim7kx&ust=1524593927482578',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwj8uNDOgdHaAhVCGpQKHcZhA20QjRx6BAgAEAU&url=%2Furl%3Fsa%3Di%26rct%3Dj%26q%3D%26esrc%3Ds%26source%3Dimages%26cd%3D%26ved%3D%26url%3Dhttps%253A%252F%252Fwww.google.org%252F%26psig%3DAOvVaw36tBHQHa_lKJNnBYATVLaz%26ust%3D1524593923674766&psig=AOvVaw36tBHQHa_lKJNnBYATVLaz&ust=1524593923674766',
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

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))

@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
