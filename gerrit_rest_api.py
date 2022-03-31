# Use Gerrit REST API to get changes list

import requests
import json
import datetime

class gerritDate():
    def __init__(self, delta):
        self.now = datetime.datetime.now()
        self.gerritDate = self.now + datetime.timedelta(days=delta)

    def get(self):
        return self.gerritDate.strftime('%Y-%m-%d')

class gerritUrl():
    def __init__(self, serverName, queryOptions, userName=None, password=None):
        self.serverName = serverName
        self.queryOptions = queryOptions
        #self.startTime = startTime
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
    def __init__(self, server):
        gDate = gerritDate(-7)
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
        print(self.changes)

        return self.changes

