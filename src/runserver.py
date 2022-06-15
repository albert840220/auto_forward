import smtpd
import asyncore
import logging, sys, datetime
import smtplib, ssl
from email.policy import default
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# parser package
import quopri
from io import BytesIO
from email.parser import BytesParser

logging.basicConfig(level=logging.INFO, filename='receive.log',
                    format='[%(asctime)s %(levelname)-8s]\n %(message)s',
                    datefmt='%Y%m%d %H:%M:%S',
                    )
ALLOWED_HOSTS = ["192.168.55.26", "192.168.55.27", "192.168.55.22"]
MAIL_RELAY_PORT = 25
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
SENDER_EMAIL = ""  # Gmail 帳號
PASSWORD = ""  # Gmail 應用程式密碼


def current_time():
    data = datetime.datetime.utcnow()
    return str(datetime.datetime.strftime(data, '%Y%m%d %H:%M:%S'))


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None,
                        rcpt_options=None):
        if not peer[0] in ALLOWED_HOSTS:
            return logging.info("IP " + peer[0] + " not allowed")

        print(f'{current_time()} function in')
        headers = BytesParser(policy=default).parsebytes(data)
        html_content = None
        plain_content = None

        for part in headers.walk():
            content_type = part.get_content_type()
            if content_type == 'text/html':
                payload = part.get_payload(decode=True)
                # decode quoted-printable in html
                outputFile = BytesIO()
                inputFile = BytesIO(bytes(payload))  # create binary input file
                quopri.decode(inputFile, outputFile)  # generate decoded data
                output = outputFile.getvalue()  # extract output
                html_content = output.decode('utf-8', errors='ignore')  # extract text
            elif content_type == 'text/plain':
                payload = part.get_payload(decode=True)
                plain_content = payload.decode("utf-8")
            else:
                print(content_type)
                payload = part.get_payload(decode=True)
                print(payload)
                print('---------------')

        # Create MIMEMultipart object
        # 撰寫 Email 的收件內容
        msg = MIMEMultipart()
        msg["Subject"] = headers["subject"]
        msg["From"] = mailfrom
        msg["To"] = headers.get("To", "")
        msg["Cc"] = headers.get("Cc", "")
        if html_content:
            msg.attach(MIMEText(html_content, "html"))
        if plain_content:
            msg.attach(MIMEText(plain_content, "plain"))

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT,
                                  context=context) as server:
                server.login(SENDER_EMAIL, PASSWORD)
                server.sendmail(
                    SENDER_EMAIL, rcpttos, msg.as_string()
                )
            print(f'{current_time()} send mail success')
        except:
            print(f'{current_time()} send mail fail')

        try:
            logging.info('IP:' + peer[0] + '\n'
                         + 'From:' + msg["From"] + '\n'
                         + 'To:' + msg["To"] + '\n'
                         + 'Cc:' + msg["Cc"] + '\n'
                         + 'Subject:' + msg["Subject"] + '\n')
        except:
            print(f'{current_time()} LOGGING ERROR')
        sys.stdout.flush()


if __name__ == "__main__":
    server = CustomSMTPServer(('0.0.0.0', MAIL_RELAY_PORT), None)
    print(f'{current_time()} server in')
    asyncore.loop()
