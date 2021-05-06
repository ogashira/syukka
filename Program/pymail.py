#! /user/bin/python3

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication




smtp_host = 'smtp.toyo-jupiter.co.jp'
smtp_port= 587
username = 'a_ogashira_toyo-jupiter'
password = 'M8AFPNDF'
from_address = 'a_ogashira@toyo-jupiter.co.jp'
to_address = 'uv_oga.930.aha@icloud.com'
subject = 'test subject'
body = """
<html>
    <body>
        <h1>Eメールの送信テストです。</h1>
        <p>よろしくお願いします。</p>
    </body>
</html>"""

filepath = [r'/mnt/public/営業課ﾌｫﾙﾀﾞ/testreport/櫻田/S7-A-M_21041402H_2021422142942.pdf',
            r'/mnt/bublic/営業課ﾌｫﾙﾀﾞ/testreport/櫻田/S4-PPR82-3B-U_21041903H_2021423_小糸.pdf']
filename = os.path.basename(filepath)

# message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (from_address, to_address, subject, body))
msg = MIMEMultipart()
msg["Subject"] = subject
msg["From"] = from_address
msg["To"] = to_address
msg.attach(MIMEText(body, "html"))

with open(filepath, "rb") as f:
    mb = MIMEApplication(f.read())

mb.add_header("Content-Disposition", "attachment", filename=filename)
msg.attach(mb)



smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.login(username, password)
result = smtp.sendmail(from_address, to_address, msg.as_string())
print(result)


