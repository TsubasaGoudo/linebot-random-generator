# LINE Random Generator Bot

LINE Messaging APIを利用したランダム文章生成Bot。
お遊びです

## Overview

ユーザーがLINE上でテーマを選択すると、
テーマに登録された単語をランダムに組み合わせて文章を生成。

生成された文章の最後には、テーマに応じたメッセージを表示します。

## Features

- 25種類のテーマを収録
- ランダムな単語の組み合わせによる文章生成
- テーマ専用メッセージの抽選
- LINE上からテーマを選択可能

## Environment

- Python 3.11
- Flask
- LINE Messaging API
- LINE Bot SDK v3

## Project Structure

```text
linebot-random-generator/
├── app.py
├── generator.py
├── requirements.txt
├── .env
└── .gitignore
