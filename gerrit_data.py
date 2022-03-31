import requests
import json
import datetime

class gerritUser():
    def __init__(self, name):
        self.name = name
        self.commits = 0
        self.lines = 0
        self.branches = []
        self.brCommits = []
        self.brLines = []

    def addCommit(self, branch):
        if not branch in self.branches:
            self.branches.append(branch)
            self.brCommits.append(0)
            self.brLines.append(0)

        self.brCommits[self.branches.index(branch)] += 1
        self.commits += 1

    def addLine(self, branch, line):
        if not branch in self.branches:
            self.branches.append(branch)
            self.brCommits.append(0)
            self.brLines.append(0)

        self.brLines[self.branches.index(branch)] += line
        self.lines += line


class gerritBranch():
    def __init__(self, name):
        self.name = name
        self.commits = 0
        self.lines = 0
        self.users = []
        self.userCommits = []
        self.userLines = []

    def addCommit(self, user):
        if not user in self.users:
            self.users.append(user)
            self.userCommits.append(0)
            self.userLines.append(0)

        self.userCommits[self.users.index(user)] += 1
        self.commits += 1

    def addLine(self, user, line):
        if not user in self.users:
            self.users.append(user)
            self.userCommits.append(0)
            self.userLines.append(0)

        self.userLines[self.users.index(user)] += line
        self.lines += line

class gerritCounter():
    def __init__(self, changes):
        self.changes = changes
        self.users = []
        self.branches = []
        self.count()

    def count(self):
        for ch in self.changes:
            chUser = ch['owner']['username']
            chBr = ch['project'] + '-' + ch['branch']
            chLine = ch['insertions'] + ch['deletions']

            userFound = False
            for user in self.users:
                if user.name == chUser:
                    userFound = True
                    user.addCommit(chBr)
                    user.addLine(chBr, chLine)
                    break
            if not userFound:
                user = gerritUser(chUser)
                user.addCommit(chBr)
                user.addLine(chBr, chLine)
                self.users.append(user)

            brFound = False
            for br in self.branches:
                if br.name == chBr:
                    brFound = True
                    br.addCommit(chUser)
                    br.addLine(chUser, chLine)
                    break
            if not brFound:
                br = gerritBranch(chBr)
                br.addCommit(chUser)
                br.addLine(chUser, chLine)
                self.branches.append(br)
        #print(self.users)
        #print(self.branches)

    def getUserCommitsLines(self):
        userList = []
        commitList = []
        lineList = []
        for user in self.users:
            userList.append(user.name)
            commitList.append(user.commits)
            lineList.append(user.lines)
        return (userList, commitList, lineList)

    def getBranchCommitsLines(self):
        brList = []
        commitList = []
        lineList = []
        for br in self.branches:
            brList.append(br.name)
            commitList.append(br.commits)
            lineList.append(br.lines)
        return (brList, commitList, lineList)

