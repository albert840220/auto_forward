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
                    format='[%(asctime)s %(levelname)-4s]\n %(message)s',
                    datefmt='%Y%m%d %H:%M:%S',
                    )
ALLOWED_HOSTS = [""]  # ip list
MAIL_RELAY_PORT = 25
MAIL_SERVER = ""
MAIL_PORT = 465
SENDER_EMAIL = ""
PASSWORD = ""


def current_time():
    data = datetime.datetime.utcnow()
    return str(datetime.datetime.strftime(data, '%Y%m%d %H:%M:%S'))


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None,
                        rcpt_options=None):
        print(f'{current_time()} function in')
        headers = BytesParser(policy=default).parsebytes(data)
        RECEIVER_EMAIL = str(headers['To']).split(", ")
        html = headers.get_body(preferencelist='html')
        plain = headers.get_body(preferencelist='plain')
        
        if html:
            # decode quoted-printable in html
            outputFile = BytesIO()
            inputFile = BytesIO(bytes(html))  # create binary input file
            quopri.decode(inputFile, outputFile)  # generate decoded data
            output = outputFile.getvalue()  # extract output
            html = output.decode('utf-8')  # extract text        
        if plain:
            for part in headers.walk():
                payload = part.get_payload(decode=True)
                if payload:
                    plain = payload.decode("utf-8")

        if peer[0] in ALLOWED_HOSTS:
            # Create MIMEMultipart object
            msg = MIMEMultipart()
            msg["Subject"] = headers["subject"]
            msg["From"] = SENDER_EMAIL
            msg["To"] = ", ".join(RECEIVER_EMAIL)
            if html:
                msg.attach(MIMEText(html, "html"))
            if plain:
                msg.attach(MIMEText(plain, "plain"))

            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT,
                                      context=context) as server:
                    server.login(SENDER_EMAIL, PASSWORD)
                    server.sendmail(
                        SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string()
                    )
                print(f'{current_time()} send mail success')
            except:
                print(f'{current_time()} send mail fail')

            try:
                logging.info('IP:' + peer[0] + '\nFrom:' + headers["From"]
                             + '\nTo:' + headers["To"] + '\nSubject:'
                             + headers["Subject"] + "\n")
            except:
                print(f'{current_time()} LOGGING ERROR')
            sys.stdout.flush()


if __name__ == "__main__":
    server = CustomSMTPServer(('0.0.0.0', MAIL_RELAY_PORT), None)
    print(f'{current_time()} server in')
    asyncore.loop()