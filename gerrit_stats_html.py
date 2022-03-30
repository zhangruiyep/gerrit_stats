import datetime
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, Tabs, Panel
from bokeh.layouts import gridplot

from gerrit_rest_api import *

changes = gerritChanges('dal-server-2:8081')
counter = gerritCounter(changes.get())
users = counter.getUsers()
all_commits = []
lines = []
for user in users:
    #print(user +  str(counter.getCountByUser(user)))
    all_commits.append(counter.getCountByUser(user))
    lines.append(counter.getLinesByUser(user))
print(users)
print(all_commits)
print(lines)

html = 'gerrit_stats_' + datetime.datetime.now().strftime('%Y%m%d') + '.html'
output_file(filename=html, title="Gerrit Stats Weekly")

source = ColumnDataSource(data=dict(username=users, commits=all_commits, lines=lines))
# 创建一个包含标签的data，对象类型为ColumnDataSource

tipsCommits = [
    ("owner", "@username"),
    ("commits", "@commits"),
]

#p = figure(x_range=users, y_range=(0,max(all_commits)*1.1), plot_height=350, title="Gerrit Stats") #x_range一开始就要设置成一个字符串的列表；要一一对应
pCommits = figure(x_range=users, plot_height=350, title="Gerrit Commits", tooltips=tipsCommits) #x_range一开始就要设置成一个字符串的列表；要一一对应

pCommits.vbar(x='username', top='commits', source=source,    # 加载数据另一个方式
       width=0.6, alpha = 0.8, legend_label="commits", color='green'
       )

tipsLines = [("owner", "@username"), ("lines", "@lines")]
pLines = figure(x_range=users, plot_height=350, title="Gerrit Lines", tooltips=tipsLines)
pLines.vbar(x='username', top='lines', source=source,    # 加载数据另一个方式
       width=0.6, alpha = 0.8, legend_label="lines"
       )

# add plot to grid
gpCommits = gridplot([[pCommits, pLines]])
tabCommits = Panel(child=gpCommits, title='Changes')
# add gridplot to tab
tabs = Tabs(tabs=[tabCommits])
# save file
save(tabs)
