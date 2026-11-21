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
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)

from generator import THEMES, generate_text


# ========================================
# 環境設定
# ========================================

load_dotenv()

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    raise RuntimeError("LINE認証情報が設定されていません。")


# ========================================
# LINE Bot設定
# ========================================

app = Flask(__name__)

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)

handler = WebhookHandler(CHANNEL_SECRET)


# ========================================
# テーマ一覧の作成
# ========================================

def create_theme_menu():

    lines = [
        "【テーマ一覧】",
        "",
    ]

    for i, theme in enumerate(THEMES, start=1):
        lines.append(f"{i}. {theme['name']}")

    lines.extend([
        "",
        "生成したいテーマの番号を送ってください。",
        "「メニュー」と送ると一覧を再表示します。",
    ])

    return "\n".join(lines)


# ========================================
# 動作確認用エンドポイント
# ========================================

@app.route("/", methods=["GET"])
def index():
    return "LINE Bot server is running."


# ========================================
# LINE Webhook
# ========================================

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


# ========================================
# メッセージ受信処理
# ========================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    received_text = event.message.text.strip()

    # メニュー表示
    if received_text in ["メニュー", "menu", "MENU", "一覧"]:
        reply_text = create_theme_menu()

    # テーマ番号を受信
    elif received_text.isdecimal():

        theme_number = int(received_text)

        if 1 <= theme_number <= len(THEMES):
            reply_text = generate_text(theme_number)

        else:
            reply_text = (
                f"テーマ番号は1〜{len(THEMES)}で指定してください。\n"
                "「メニュー」と送ると一覧を確認できます。"
            )

    # その他のメッセージ
    else:
        reply_text = (
            "テーマ番号を送ってください。\n"
            "「メニュー」と送るとテーマ一覧を表示します。"
        )

    # LINEに返信
    with ApiClient(configuration) as api_client:

        line_bot_api = MessagingApi(api_client)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=reply_text)
                ]
            )
        )


# ========================================
# サーバー起動
# ========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )
