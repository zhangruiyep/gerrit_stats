# Use Gerrit REST API to get changes list

import requests
import json
import logging

logger = logging.getLogger(__name__)

class GerritUrl():
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

class GerritChanges():
    def __init__(self, server, sD, eD, max_pages=100):
        startDate = sD + ' 00:00:00'
        endDate = eD + ' 00:00:00'
        self.options = '?q=status:merged+after:\"' + startDate + '\"+before:\"' + endDate + '\"&o=DETAILED_ACCOUNTS'
        self.server = server
        self.max_pages = max_pages

    def build_api_url(self):
        self.url = GerritUrl(self.server, self.options, 'admin', 'admin').get()
        return self.url

    def get(self):
        more = True
        s = 0
        url = self.build_api_url()
        self.changes = []
        page = 0

        while (more and page < self.max_pages):
            #print(url)
            try:
                resp = requests.get(url)
                resp.raise_for_status()
            except requests.exceptions.ConnectionError as e:
                logger.error('Connection error: %s', e)
                return None
            except requests.exceptions.HTTPError as e:
                logger.error('HTTP error: %s', e)
                return None
            
            text = resp.content
            json_str = text.decode('UTF-8')[5:] # skip '{[(!\n'

            self.changes = self.changes + json.loads(json_str)
            #print(self.changes)
            #print(self.changes[-1])
        
            try:
                more = self.changes[-1]['_more_changes']
            except:
                more = False

            s += 500
            page += 1
            url = self.url + '&S=' + str(s)

        return self.changes

