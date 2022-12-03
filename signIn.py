import json
import schedule
import smtplib
import requests
from requests.sessions import Session
import time
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

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

def getToken(s):
    """Return the unique token. Required to make call to booking service"""
    URL = 'https://www.afbostader.se/dina/sidor/boka-tvattid/'
    r = s.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        value = soup.find('input', {'id': 'hidAptusToken'}).get('value')
        print(value)
        return value
    except Exception as e:
        print("Got unhandled exception %s" % str(e))

def sign(name, password):
    Py = Account(name, password)
    s = Py.login()
    token = getToken(s)
    return token, s