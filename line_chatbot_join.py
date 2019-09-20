import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent, LeaveEvent, TextMessage, TextSendMessage
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

@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "謝謝邀請我這個機器來至此群組！！我會盡力為大家服務的～"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)

@handler.add(LeaveEvent)
def handle_leave(event):
    print("leave Event =", event)
    print("我被踢掉了QQ 相關資訊", event.source)

                            
@app.route('/')
def homepage():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()
