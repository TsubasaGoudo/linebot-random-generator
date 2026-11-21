import random

# LINEに送信する文章の長さを制限
MAX_GENERATED_CHARS = 4000


# ========================================
# テーマデータ
# ========================================

THEMES = [
    {
        "name": "進捗どうですか",
        "words": ["進捗", "どう", "です", "か"],
        "messages": [
            "まだですか？",
            "そろそろ報告してください。",
            "期待しています。",
        ],
    },
    {
        "name": "レポートまだ終わらない",
        "words": ["レポート", "まだ", "終わら", "ない"],
        "messages": [
            "提出期限をご存じですか？",
            "参考文献は書きましたか？",
            "それ、レポートですか？",
        ],
    },
    {
        "name": "人生とはなにか",
        "words": ["人生", "とは", "なに", "か"],
        "messages": [
            "考えるだけ無駄です。",
            "正解はありません。",
            "そもそも人生とは？",
        ],
    },
    {
        "name": "貯金が増えない",
        "words": ["貯金", "が", "増え", "ない"],
        "messages": [
            "収支を確認してください。",
            "何に使ったんですか？",
            "来月から頑張りましょう。",
        ],
    },
    {
        "name": "明日から本気出す",
        "words": ["明日", "から", "本気", "出す"],
        "messages": [
            "その明日はいつですか？",
            "昨日も聞きました。",
            "明日になったら教えてください。",
        ],
    },
    {
        "name": "ちょっとだけ寝る",
        "words": ["ちょっと", "だけ", "寝る"],
        "messages": [
            "おはようございます。",
            "もう朝です。",
            "ちょっととは？",
        ],
    },
    {
        "name": "単位が足りない",
        "words": ["単位", "が", "足り", "ない"],
        "messages": [
            "必修科目は確認しましたか？",
        ],
    },
    {
        "name": "卒論が終わらない",
        "words": ["卒論", "が", "終わら", "ない"],
        "messages": [
            "先生は待ってくれません。",
        ],
    },
    {
        "name": "課題を忘れた",
        "words": ["課題", "を", "忘れ", "た"],
        "messages": [
            "提出期限は昨日でした。",
        ],
    },
    {
        "name": "テスト勉強していない",
        "words": ["テスト", "勉強", "して", "いない"],
        "messages": [
            "そろそろ教科書を開きませんか？",
        ],
    },
    {
        "name": "就活が終わらない",
        "words": ["就活", "が", "終わら", "ない"],
        "messages": [
            "内定はまだですか？",
        ],
    },
    {
        "name": "残業が終わらない",
        "words": ["残業", "が", "終わら", "ない"],
        "messages": [
            "定時とは何だったのでしょうか？",
        ],
    },
    {
        "name": "上司が怖い",
        "words": ["上司", "が", "怖い"],
        "messages": [
            "報告・連絡・相談を忘れずに。",
        ],
    },
    {
        "name": "部屋が汚い",
        "words": ["部屋", "が", "汚い"],
        "messages": [
            "床が見えていますか？",
        ],
    },
    {
        "name": "お金がない",
        "words": ["お金", "が", "ない"],
        "messages": [
            "給料日はまだですか？",
        ],
    },
    {
        "name": "ダイエットが続かない",
        "words": ["ダイエット", "が", "続か", "ない"],
        "messages": [
            "明日から頑張りましょう。",
        ],
    },
    {
        "name": "早起きできない",
        "words": ["早起き", "でき", "ない"],
        "messages": [
            "もう昼ですよ。",
        ],
    },
    {
        "name": "やればできる",
        "words": ["やれ", "ば", "できる"],
        "messages": [
            "では、やってください。",
        ],
    },
    {
        "name": "まだ本気じゃない",
        "words": ["まだ", "本気", "じゃ", "ない"],
        "messages": [
            "いつ本気になりますか？",
        ],
    },
    {
        "name": "計画だけは完璧",
        "words": ["計画", "だけ", "は", "完璧"],
        "messages": [
            "実行してください。",
        ],
    },
    {
        "name": "明日やろうは馬鹿野郎",
        "words": ["明日", "やろう", "は", "馬鹿野郎"],
        "messages": [
            "今日は何をしましたか？",
        ],
    },
    {
        "name": "完璧を目指して未完成",
        "words": ["完璧", "を", "目指", "して", "未完成"],
        "messages": [
            "まず完成させましょう。",
        ],
    },
    {
        "name": "何もしていないのに疲れた",
        "words": ["何も", "して", "いない", "のに", "疲れた"],
        "messages": [
            "何をしたんですか？",
        ],
    },
    {
        "name": "時間が足りない",
        "words": ["時間", "が", "足り", "ない"],
        "messages": [
            "時間は全員平等です。",
        ],
    },
    {
        "name": "自分へのご褒美",
        "words": ["自分", "への", "ご褒美"],
        "messages": [
            "何も達成していませんよ？",
        ],
    },
]


# ========================================
# ランダム文章生成
# ========================================

def generate_text(theme_number: int) -> str:

    if not 1 <= theme_number <= len(THEMES):
        raise ValueError("無効なテーマ番号です。")

    theme = THEMES[theme_number - 1]

    words = theme["words"]
    word_count = len(words)

    char_count = 0
    sorted_count = 0
    last_num = word_count

    generated_words = []
    truncated = False

    # Cプログラムと同じランダム生成処理
    while sorted_count != word_count - 1:

        num = random.randrange(word_count)

        word = words[num]
        generated_words.append(word)

        char_count += len(word)

        if num > last_num:
            sorted_count += 1
        else:
            sorted_count = 0

        last_num = num

        # LINEへの送信文字数を制限
        if (
            char_count >= MAX_GENERATED_CHARS
            and sorted_count != word_count - 1
        ):
            truncated = True
            break

    # テーマ専用メッセージを抽選
    message = random.choice(theme["messages"])

    # 文章を組み立てる
    generated_text = "".join(generated_words)

    result = (
        f"【今回のテーマ】{theme['name']}\n\n"
        f"{generated_text}\n\n"
        f"{message}\n"
    )

    if truncated:
        result += (
            f"{char_count}文字生成しました。"
            "文字数上限のため途中で終了しました。"
        )
    else:
        result += f"{char_count}文字生成して煽られました。"

    return result
