#from sched import schedule
import schedule
import smtplib
import requests
from requests.sessions import Session
import time
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

import smtplib, ssl


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

def send_mail(message):
    try:
        sender_email = "bastuklubbenparran@gmail.com"
        password = "password"
        receiver = "temp"
        receivers = ["temp", "temp"]
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receivers, message)
    
        
    except Exception as e:
        # Print any error messages to stdout
        print(e)

def tryBook(s, token, time, name):

    params = (
    ('Token', token),
    ('StartTimestamp','20'+ time + 'T08:00'),
    ('LengthMinutes', '180'),
    ('GroupId', '33'),
    ('MaxWaitSeconds', '60'),
)
    print(params)

    response = s.get('https://aptusbookingservice.afbostader.se/bookingservice.svc/Book', params=params)
    print(response.json())
    try:
        print(params[1])
        message = """
        Sauna booked at """ + str(params[1])+ """, by """ + name + """
        """
        if response.json()['UnBookable']:
            print('success')
        send_mail(message)
        
            
    except Exception as e:
        message = """
        Sauna could not be booked at """ + str(params[1])+ """, by """ + name + """.\n\n error: """ + str(e) + """
        """
        send_mail(message)
        
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
    #mydivs = soup.find_all("div", {"class": "price-ticket__fluctuations"})


def job():
    name = 'temp'
    Py = Account(name, 'temp')
    s = Py.login()
    token = getToken(s)
    next_time = findTime(1)

    tryBook(s, token, next_time, name)

def main():
    print('called')
    schedule.every().sunday.at("23:30").do(job)
    Py = Account('temp', 'temp')
    s = Py.login()
    token = getToken(s)
    next_date = findTime(1)
    print(next_date)
    tryBook(s, token, '22-12-03', "Hampus")    

    while True:
        schedule.run_pending()
        time.sleep(59)


#def notifyy():
    #gm = gmail()
    #gm.notify()

if __name__ == "__main__":
    send_mail("Server running")
    main()

    
    
        