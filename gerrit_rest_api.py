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
            #self.url = self.url + '+after:\'' + self.startTime + '\'' 
        return self.url

class gerritCounter():
    def __init__(self, changes):
        self.changes = changes

    def getCountByUser(self, userName):
        self.userCommits = 0
        for ch in self.changes:
            if ch['owner']['username'] == userName:
                self.userCommits += 1
        return self.userCommits

    def getUsers(self):
        self.users = []
        for ch in self.changes:
            if not ch['owner']['username'] in self.users:
                self.users.append(ch['owner']['username'])
        return self.users

    def getLinesByUser(self, userName):
        self.userLines = 0
        for ch in self.changes:
            if ch['owner']['username'] == userName:
                self.userLines += ch['insertions']
                self.userLines += ch['deletions']
        return self.userLines

    def getBranches(self):
        self.brs = []
        for ch in self.changes:
            br = ch['project'] + '-' + ch['branch']
            if not br in self.brs:
                self.brs.append(br)
        return self.brs

    def getUsersByBranch(self, branch):
        self.brUsers = []
        for ch in self.changes:
            br = ch['project'] + '-' + ch['branch']
            if br == branch:
                user = ch['owner']['username']
                if not user in self.brUsers:
                    self.brUsers.append(user)
        return self.brUsers

    def getCountByBranchUser(self, branch, user):
        self.userCommits = 0
        for ch in self.changes:
            br = ch['project'] + '-' + ch['branch']
            us = ch['owner']['username']
            if br == branch and us == user:
                self.userCommits += 1
        return self.userCommits

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
        #print(resp)
        #print(resp.headers)
        #print(resp.content)

        if resp.status_code != 200:
            quit()

        #print(resp.content)
        text = resp.content
        json_str = text.decode('UTF-8')[5:]
        #print(json_str)

        self.changes = json.loads(json_str)
        print(self.changes)

        return self.changes

