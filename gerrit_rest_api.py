# Use Gerrit REST API to get changes list

import requests
import json
import datetime, calendar

class gerritDate():
    def __init__(self, period):
        self.today = datetime.datetime.today()
        if period == 'month':
            # find last month 1st day
            if self.today.month == 1:
                month = 12
                year = self.today.year - 1
            else:
                month = self.today.month - 1
                year = self.today.year
            day = 1
            self.date = datetime.date(year, month, day)
        else:
            # find last monday
            self.date = self.today + datetime.timedelta(days=-1)
            while self.date.weekday() != calendar.MONDAY:
                self.date = self.date + datetime.timedelta(days=-1)

    def get(self):
        return self.date.strftime('%Y-%m-%d')

class gerritUrl():
    def __init__(self, serverName, queryOptions, userName=None, password=None):
        self.serverName = serverName
        self.queryOptions = queryOptions
        self.userName = userName
        self.password = password

    def get(self):
        self.url = 'http://'
        if (self.userName != ''):
            self.url = self.url + self.userName + ':' + self.password + '@'
        self.url = self.url + self.serverName + '/changes/'
        if (self.queryOptions != ''):
            self.url = self.url + self.queryOptions
        return self.url

class gerritChanges():
    def __init__(self, server, period):
        gDate = gerritDate(period)
        #UTC time
        startDate = gDate.get() + ' 00:00:00'
        #print(startDate)
        options = '?q=status:merged+after:\"' + startDate + '\"&o=DETAILED_ACCOUNTS'
        gUrl = gerritUrl(server, options, 'admin', 'admin')
        self.url = gUrl.get()

    def get(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            return None

        text = resp.content
        json_str = text.decode('UTF-8')[5:] # skip '{[(!\n'

        self.changes = json.loads(json_str)
        #print(self.changes)

        return self.changes

