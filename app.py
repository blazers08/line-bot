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
        message1 = TextMessage(text="Hello Guys, I'm Denny. I'm from Taipei")
        line_bot_api.reply_message(event.reply_token, message1)
    elif key == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        message4 = TextMessage(text="Hello world")
        line_bot_api.reply_message(event.reply_token, message4)




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
