import datetime
from math import pi
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, Tabs, Panel
from bokeh.palettes import d3, viridis, Category20c, Set3
from bokeh.layouts import gridplot
from bokeh.transform import cumsum

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
#print(users)
#print(all_commits)
#print(lines)

brs = counter.getBranches()
#print(brs)

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

# branches
gpLines = []
for br in brs:
    users = counter.getUsersByBranch(br)
    commits = []
    colors = []
    for user in users:
        count = counter.getCountByBranchUser(br, user)
        commits.append(count)
        colors.append(Set3[12][users.index(user)])
    angles = []
    for commit in commits:
    	angles.append(commit/sum(commits)*2*pi)
    cdSource = ColumnDataSource(data=dict(username=users, commits=commits, angle=angles, color=colors))
    #print(cdSource.column_names)
    #print(cdSource.data)
# 创建一个包含标签的data，对象类型为ColumnDataSource

#tipsCommits = [
#    ("owner", "@username"),
#    ("commits", "@commits"),
#]

#p = figure(x_range=users, y_range=(0,max(all_commits)*1.1), plot_height=350, title="Gerrit Stats") #x_range一开始就要设置成一个字符串的列表；要一一对应
    pBranch = figure(plot_height=350, title="Gerrit Branch " + br, tooltips=tipsCommits) #x_range一开始就要设置成一个字符串的列表；要一一对应
    #pBranch.wedge(x=0, y=1, radius=0.4,
    #    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
    #    line_color="white", fill_color='color', legend_label='branches', source=cdSource)
    pBranch.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color',
	legend_field='username', source=cdSource) #color="#2b8cbe")
    pBranch.axis.axis_label=None
    pBranch.axis.visible=False
    pBranch.grid.grid_line_color = None # 网格线颜色

    gpLine = [pBranch]
    gpLines.append(gpLine)

gpBranches = gridplot(gpLines)
tabBranches = Panel(child=gpBranches, title='Branches')

# add gridplot to tab
tabs = Tabs(tabs=[tabCommits, tabBranches])
#tabs = Tabs(tabs=[tabBranches])
# save file
save(tabs)
