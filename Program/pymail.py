import smtplib

smtp_host = 'smtp.toyo-jupiter.co.jp'
smtp_port= 587
username = 'a_ogashira_toyo-jupiter'
password = 'M8AFPNDF'
from_address = 'a_ogashira@toyo-jupiter.co.jp'
to_address = 'uv_oga.930.aha@icloud.com'
subject = 'test subject'
body = 'test body'
message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (from_address, to_address, subject, body))

smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.login(username, password)
result = smtp.sendmail(from_address, to_address, message)
print(result)


