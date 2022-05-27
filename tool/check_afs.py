import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

smtp_server = ""
smtp_port = 25
sender = ""
recipients = [""]
text = "您好，如果您可以收到這封郵件，表示轉發服務正常。\n此為系統自動發送信件，請勿回覆，謝謝！"
smtp = smtplib.SMTP(host=smtp_server, port=smtp_port)
smtp.set_debuglevel(1)

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = ", ".join(recipients)
msg['Subject'] = Header("轉發服務正常", 'utf-8')
msg.attach(MIMEText(text, "plain"))


smtp.sendmail(sender, recipients, msg.as_string())
smtp.quit()

