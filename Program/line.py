#! python
# -*- coding: utf-8 -*-


import requests

line_notify_token = 'rx0E3JUiU9JVbQj7WeIbZF9AAKXj3m2quZjSy6Ffhiw'
line_notify_api = 'https://notify-api.line.me/api/notify'
message = '出荷のoutputを所定のフォルダに入れました。'


payload = {'message': message}
headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
line_notify = requests.post(line_notify_api, data=payload, headers=headers)
