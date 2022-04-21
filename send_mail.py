import smtplib
from email.message import EmailMessage

sender = "acsi_test@demo.com"
recipients = ["albert@demo.com","larry@demo.com"]

# Open the plain text file whose name is in textfile for reading.
with open("mail_content.txt") as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

msg['From'] = sender
msg['To'] = ", ".join(recipients)
msg['Subject'] = f"轉發服務正常"

s = smtplib.SMTP('192.168.55.27:5025')
s.send_message(msg)
s.quit()
