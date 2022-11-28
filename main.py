import json
import schedule
import smtplib
import requests
from requests.sessions import Session
import time
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

import smtplib, ssl


#init in main method
sender_email = ""
email_password = ""


class Account:
    def __init__(self, email, password) -> None:
        self.data =  {
  '__EVENTTARGET': '',
  '__EVENTARGUMENT': '',
  '__VIEWSTATE': '/wEPDwULLTE5MDAyODUwODVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBSZjdGwwMCRjdGwyNSRMb2dpbkNvbnRyb2wkY2hrUmVtZW1iZXJNZQUmY3RsMDAkY3RsMjkkTG9naW5Db250cm9sJGNoa1JlbWVtYmVyTWUZC98b4Wwj+A0yAHw7ORlJC6N5MiZF0Jk+og9XZhqO2Q==',
  '__VIEWSTATEGENERATOR': '9345F2A8',
  '__EVENTVALIDATION': '/wEdAAwi5TmzpFG20Bu/GVe0HTOXzEHg9XOOFTnaRtup/xN2H9zfwMl9EJOElzCIu+jVJcNexydOMEOC3vxuYK/isGajffL4wvHcA8wDB9JCE0Dlxt0Bx0snz+eAxawA+B7rJmaqh4CFgckOjI3+8lIGmcRXgBKFdOsEIcs0nlYwFTfYc1ZA0XjABxVFI7uJutt2Io+xXxdkTh3DRDBznH5YqwmCTy+YXLFP1ReFt07ABaFBD7Owkpln17nCtQ6PDLIMK1P7/5CQ+iU/hx7zIv9sdahNYh84edgLg0J9b8Ku3j48Kg==',
  'ctl00$ctl25$LoginControl$UserName': email,
  'ctl00$ctl25$LoginControl$Password': password,
  'ctl00$ctl25$LoginControl$btnLogIn': 'Logga in',
  'ctl00$ctl26$hidSearchUrl': 'https://www.afbostader.se/sok/',
  'fake_chrome_username': '',
  'fake_chrome_password': '',
  'q': '',
  'quicksearch': '',
  'ctl00$ctl29$LoginControl$UserName': '',
  'ctl00$ctl29$LoginControl$Password': '',
  'ctl00$ctl29$LoginControl$email_reset': ''
}
        
    
    def login(self) -> Session:
        s = requests.Session()
        s.get('https://www.afbostader.se/')
        l = s.post('https://www.afbostader.se/', data=self.data)
        print(l)
        return s

def getCurrentDateTime():
    t = datetime.date.today()
    date = t.strftime('%y-%m-%d')
    return date

#Sends mails to all mail specified in mail.json
#@Params message: message that will be sent  
def send_mail(message: str):
    try:
        receivers = []
        mails = read_json('mail.json')
        for mail in mails:
            receivers.append(mail.get("email"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receivers, message)
    
    except Exception as e:
        # Print any error messages to stdout
        print(e)

global dates
#Tries to book the sauna
def tryBook(s, token, time, name):
    params = (
    ('Token', token),
    ('StartTimestamp','20'+ time + 'T11:00'),
    ('LengthMinutes', '180'),
    ('GroupId', '33'),
    ('MaxWaitSeconds', '60'),
)
    response = s.get('https://aptusbookingservice.afbostader.se/bookingservice.svc/Book', params=params)
    print(response.json())
    try:
        if response.json()['UnBookable']:
            dates.append(str(params[1]).replace("('StartTimestamp', '","").replace("')","").replace("T","-"))
            message = """
            Sauna booked at """ + str(params[1])+ """, by """ + name + """
            """
            print('success')
        print(dates)    
    
    except Exception as e:
        message = """
        Sauna could not be booked at """ + str(params[1])+ """, by """ + name + """.\n\n error: """ + str(e) + """
        """
        print(e)
        
#Finds date in x number of weeks
def findTime(nbr_weeks):
    current_date = datetime.today()
    result_2 = current_date + timedelta(weeks=nbr_weeks)
    result = result_2.strftime('%y-%m-%d')

    return result



def getToken(s):
    """Return the unique token. Required to make call to booking service"""
    URL = 'https://www.afbostader.se/dina/sidor/boka-bastu/'
    r = s.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        value = soup.find('input', {'id': 'hidAptusToken'}).get('value')
        print(value)
        return value
    except Exception as e:
        print("Got unhandled exception %s" % str(e))

def remove_old_dates_from_dates():
    result = []
    today = datetime.today()
    global dates
    for date in dates:
        date = date.replace(' ', '-').replace(':','-')
        date = date.split('-') 
        date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]))
        if date > today:
            result.append(str(date))
    dates = result

def job_1():
    accounts = read_json('accounts.json')
    for acc in accounts:
        name = acc.get("email")
        password = acc.get("password")
        Py = Account(name, password)
        s = Py.login()
        token = getToken(s)

        for i in range(len(accounts)):
            next_time = findTime(i+1)
            tryBook(s, token, next_time, name)

def job_2():
    

    remove_old_dates_from_dates()

    result = ""

    for x in dates:
        result = result + x + "\n"
    message = """
    Good monday!
    \nThis is the schedule for the bastuklubben: \n""" + result + """  
    """

    if len(dates) == 0:
        message = """
        The sauna is not booked :(
        """

    send_mail(message)

def main():
    print('called')
    schedule.every().sunday.at("23:45").do(job_1)   
    schedule.every().monday.at("12:00").do(job_2)

    while True:
        schedule.run_pending()
        time.sleep(55)


def read_json(file_name):
    f = open(file_name)
    data = json.load(f)
    result = []
    for i in data:
        result.append(i) 
    f.close()
    return result

if __name__ == "__main__":
    dates = []
    sender_email = ""
    email_password = ""
    main()

    
    
        