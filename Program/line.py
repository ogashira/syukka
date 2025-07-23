#! python
# -*- coding: utf-8 -*-

import requests
import json
import yaml

# config.yaml を読み込む
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# チャネルアクセストークン（長期）
channel_access_token = config['channel_access_token']

# 複数の送信先ユーザーID（userIdリスト）
user_ids = config['user_ids']

# 共通の送るメッセージ
message_data = {
    'type': 'text',
    'text': '出荷のoutputを所定のフォルダに入れました。'
}

# ヘッダー
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {channel_access_token}'
}

# 各ユーザーに順番に送信
for user_id in user_ids:
    payload = {
        'to': user_id,
        'messages': [message_data]
    }

    response = requests.post(
        'https://api.line.me/v2/bot/message/push',
        headers=headers,
        data=json.dumps(payload)
    )
