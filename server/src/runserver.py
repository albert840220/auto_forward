import smtpd
import asyncore
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, filename='test.log',
	format='[%(asctime)s %(levelname)-8s]\n %(message)s',
	datefmt='%Y%m%d %H:%M:%S',
	)

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None,rcpt_options=None):
        print("function in")
        ALLOWED_HOSTS = ["192.168.55.25","192.168.55.26","192.168.55.29"]
        if peer[0] in ALLOWED_HOSTS:
            str_data = str(data, 'utf-8') # raw_data is Bytes
            data = str_data.split("\n")
            print(data)
            data_dict = {}
            for i in range(0, len(data)):
                if 'Subject:' in data[i]:
                    list_split = data[i].split(": ")
                    data_dict["subject"] = list_split[1]
                    continue
                if 'From:' in data[i]:
                    list_split = data[i].split(": ")
                    data_dict["sender"] = list_split[1]
                    continue
                if 'To:' in data[i]:
                    list_split = data[i].split(": ")
                    data_dict["recipients"] = [list_split[1]]
                    continue

            # spell word
            text_list = data[7:]
            text = ""
            for word in text_list:
                text += word + "\n"
                
            # Data processed as json
            data_dict["body"] = text
            
            try:
                h_data = {'Authorization': 'Basic ' + 'bm90aWZpY2F0aW9uOjM4MzZ5MWVkNzQ5ejQ3ejI4MGUyNXk2M2Y5N2I5OHlj'}
                result = requests.post(
                    "http://127.0.0.1:8002" + "/notification/send_mail/",
                    json=data_dict, headers=h_data)
                result_json = json.loads(result.content)
                logging.info('IP:'+peer[0]+"\nMsg:"+str(result_json['stat_code'])+'\nFrom:'+data_dict["sender"]+'\nTo:'+str(data_dict["recipients"])+'\nSubject:'+data_dict["subject"]+'\nBody:'+data_dict["body"])
                return
            except:
                print("Send_mail API Error")
        else:
            print("invalid IP")

if __name__ == "__main__":
    server = CustomSMTPServer(('0.0.0.0', 5025), None)
    print('server in')
    asyncore.loop()

