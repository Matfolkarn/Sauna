import json
import schedule
import smtplib
import requests
from requests.sessions import Session
import time
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

import smtplib, ssl

import signIn

def trybook(token, time, s):
    for id in range(27,30):
        params = (
        ('Token', token),
        ('StartTimestamp','20'+ time + 'T19:00'),
        ('LengthMinutes', '90'),
        ('GroupId', str(id)),
        ('MaxWaitSeconds', '60'),
        )
        url = 'https://aptusbookingservice.afbostader.se/bookingservice.svc/Book'
        response = s.get(url, params=params)
        print(response.json)


def wash(email, password, date):
    token = signIn.sign(email, password)
    trybook(token[0], date,token[1])
