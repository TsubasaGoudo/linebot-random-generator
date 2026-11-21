import os

from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

from generator import THEMES, generate_text

load_dotenv()
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    raise RuntimeError("LINE認証情報が設定されていません。")

app = Flask(__name__)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


def create_theme_flex_message():
    bubbles = []

    for start_index in range(0, len(THEMES), 5):
        category_themes = THEMES[start_index:start_index + 5]
        buttons = []

        for offset, theme in enumerate(category_themes):
            theme_number = start_index + offset + 1
            buttons.append({
                "type": "button",
                "style": "secondary",
                "height": "sm",
                "margin": "sm",
                "color": "#EEEAFB",
                "action": {
                    "type": "postback",
                    "label": theme["name"],
                    "data": f"theme={theme_number}",
                    "displayText": f"{theme['name']}を選びました",
                },
            })

        bubbles.append({
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#39258C",
                "paddingAll": "18px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"テーマ {start_index + 1}〜{start_index + len(category_themes)}",
                        "color": "#FFFFFF",
                        "weight": "bold",
                        "size": "xl",
                    },
                    {
                        "type": "text",
                        "text": "横にスワイプして選択できます",
                        "color": "#DAD3FF",
                        "size": "xs",
                        "margin": "sm",
                    },
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#FAF9FF",
                "paddingAll": "16px",
                "contents": buttons,
            },
        })

    return FlexMessage(
        alt_text="テーマ一覧です。横にスワイプしてテーマを選んでください。",
        contents=FlexContainer.from_dict({"type": "carousel", "contents": bubbles}),
    )


@app.route("/", methods=["GET"])
def index():
    return "LINE Bot server is running."


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        abort(400)

    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.warning("Invalid signature.")
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    received_text = event.message.text.strip()

    if received_text in ["メニュー", "menu", "MENU", "一覧", "テーマ一覧", "テーマを選ぶ"]:
        reply_message = create_theme_flex_message()
    elif received_text.isdecimal():
        theme_number = int(received_text)
        if 1 <= theme_number <= len(THEMES):
            reply_message = TextMessage(text=generate_text(theme_number))
        else:
            reply_message = TextMessage(text=f"テーマ番号は1〜{len(THEMES)}で指定してください。")
    else:
        reply_message = TextMessage(text="画面下のリッチメニューからテーマ一覧を開けます。")

    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=[reply_message])
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if not data.startswith("theme="):
        return

    try:
        theme_number = int(data.split("=", 1)[1])
    except ValueError:
        return

    if 1 <= theme_number <= len(THEMES):
        reply_text = generate_text(theme_number)
    else:
        reply_text = "選択されたテーマが見つかりませんでした。"

    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
