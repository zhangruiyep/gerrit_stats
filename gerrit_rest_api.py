# Use Gerrit REST API to get changes list

import requests
import json

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
    def __init__(self, server, sD, eD):
        startDate = sD + ' 00:00:00'
        endDate = eD + ' 00:00:00'
        options = '?q=status:merged+after:\"' + startDate + '\"+before:\"' + endDate + '\"&o=DETAILED_ACCOUNTS'
        gUrl = gerritUrl(server, options, 'admin', 'admin')
        self.url = gUrl.get()

    def get(self):
        more = True
        s = 0
        url = self.url
        self.changes = []
        while (more):
            print(url)
            resp = requests.get(url)
            if resp.status_code != 200:
                return None

            text = resp.content
            json_str = text.decode('UTF-8')[5:] # skip '{[(!\n'

            self.changes = self.changes + json.loads(json_str)
            #print(self.changes)
            print(self.changes[-1])
        
            try:
                more = self.changes[-1]['_more_changes']
            except:
                more = False

            s += 500
            url = self.url + '&S=' + str(s)

        return self.changes

