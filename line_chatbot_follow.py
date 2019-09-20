import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, JoinEvent,
    TextSendMessage, TemplateSendMessage,
    TextMessage, ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction, 
)

app = Flask(__name__)

line_bot_api = LineBotApi('05RLiq8OaKPgNoxlNcbaOItCGLedKco2uXcgRfm3ah8Ayjg1NXbw+6HmU0IAGLjqaRBTZQOZ7S3SplRGUMVfk7sdkYHb1bfgpRuGSoRciWJ685DeFIAcTMaqYCzejvZx4NidTee3YZU3BYuxDjwcj1GUYhWQfeY8sLGRXgo3xvw=
')
handler = WebhookHandler('52b9bc6a691937c7d60f742a02c7b9b5')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)
    print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    print("in Follow")
    button_template_message =ButtonsTemplate(
                                    thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
                                    title='Menu', 
                                    text='歡迎follow',
                                    image_size="cover",
                                    actions=[
                                        MessageTemplateAction(
                                            label='功能1', text='function-1'
                                        ),
                                        MessageTemplateAction(
                                            label='功能2', text='function-2'
                                        ),
                                        MessageTemplateAction(
                                            label='功能3', text='function-3'
                                        ),
                                    ]
                                )
                                
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text="Follow Event",
            template=button_template_message
        )
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text=event.message.text)
            )




@app.route('/')
def homepage():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()
