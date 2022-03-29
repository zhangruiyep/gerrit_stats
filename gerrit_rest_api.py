import requests
import json
import datetime
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

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

gDate = gerritDate(-7)
#UTC time
startDate = gDate.get() + ' 00:00:00'
print(startDate)
options = '?q=status:merged+after:\"' + startDate + '\"&o=DETAILED_ACCOUNTS'
gUrl = gerritUrl('dal-server-2:8081', options, 'admin', 'admin')
url = gUrl.get()

print(url)
resp = requests.get(url)

print(resp)
#print(resp.headers)
#print(resp.content)

if resp.status_code != 200:
    quit()

#print(resp.content)
text = resp.content
json_str = text.decode('UTF-8')[5:]
#print(json_str)

changes = json.loads(json_str)
print(changes)

counter = gerritCounter(changes)
users = counter.getUsers()
all_commits = []
for user in users:
    #print(user +  str(counter.getCountByUser(user)))
    all_commits.append(counter.getCountByUser(user))
print(users)
print(all_commits)

source = ColumnDataSource(data=dict(username=users, commits=all_commits))
# ����һ��������ǩ��data����������ΪColumnDataSource

p = figure(x_range=users, y_range=(0,max(all_commits)*1.1), plot_height=350, title="Gerrit Stats") #x_rangeһ��ʼ��Ҫ���ó�һ���ַ������б�Ҫһһ��Ӧ

p.vbar(x='username', top='commits', source=source,    # ����������һ����ʽ
       width=0.6, alpha = 0.8, legend_label="commits"
       #color = factor_cmap('fruits', palette=Spectral6, factors=fruits),    # ������ɫ
       #legend="fruits")
       )
# ������״ͼ������ֱ����ʾ��ǩ
# factor_cmap(field_name, palette, factors, start=0, end=None, nan_color='gray')����ɫת��ģ�飬����һ����ɫת������
# field_name����������
# palette����ɫ��
# factors�������ڵ�ɫ���з���ɫ�Ĳ���
# �ο��ĵ���http://bokeh.pydata.org/en/latest/docs/reference/transform.html

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"
# ������������
#cmd -->> conda install bokeh  ;  conda install json
show(p)
