import datetime
from math import pi
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, Tabs, Panel
from bokeh.palettes import d3, viridis, Category20c, Set3
from bokeh.layouts import gridplot
from bokeh.transform import cumsum

from gerrit_rest_api import *
from gerrit_data import *

changes = gerritChanges('dal-server-2:8081')
counter = gerritCounter(changes.get())
(users, userCommits, userLines) = counter.getUserCommitsLines()
(brs, brCommits, brLines) = counter.getBranchCommitsLines()
#all_commits = []
#lines = []
#for user in users:
    #print(user +  str(counter.getCountByUser(user)))
    #all_commits.append(counter.getCountByUser(user))
    #lines.append(counter.getLinesByUser(user))
#print(users)
#print(all_commits)
#print(lines)

#brs = counter.getBranches()
#print(brs)

startDate = gerritDate(-7).get()
html = 'gerrit_stats_' + startDate + '_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
output_file(filename=html, title="Gerrit Stats")

source = ColumnDataSource(data=dict(username=users, commits=userCommits, lines=userLines))
# 创建一个包含标签的data，对象类型为ColumnDataSource

tipsCommits = [
    ("author", "@username"),
    ("commits", "@commits"),
]

pCommits = figure(x_range=users, plot_height=350, title="Author Commits", tooltips=tipsCommits)
pCommits.vbar(x='username', top='commits', source=source,
       width=0.6, alpha = 0.8, legend_label="commits", color='green'
       )

tipsLines = [("author", "@username"), ("lines", "@lines")]
pLines = figure(x_range=users, plot_height=350, title="Author Lines", tooltips=tipsLines)
pLines.vbar(x='username', top='lines', source=source,
       width=0.6, alpha = 0.8, legend_label="lines"
       )


source = ColumnDataSource(data=dict(branch=brs, commits=brCommits, lines=brLines))
tipsBrCommits = [("branch", "@branch"), ("commits", "@commits")]
pBrCommits = figure(x_range=brs, plot_height=500, title="Branch Commits", tooltips=tipsBrCommits)
pBrCommits.xaxis.major_label_orientation = "vertical"
pBrCommits.vbar(x='branch', top='commits', source=source,
       width=0.6, alpha = 0.8, legend_label="commits", color='purple'
       )

tipsBrLines = [("branch", "@branch"), ("lines", "@lines")]
pBrLines = figure(x_range=brs, plot_height=500, title="Branch Lines", tooltips=tipsBrLines)
pBrLines.xaxis.major_label_orientation = "vertical"
pBrLines.vbar(x='branch', top='lines', source=source,
       width=0.6, alpha = 0.8, legend_label="lines", color='brown'
       )
# add plot to grid
gpCommits = gridplot([[pCommits, pLines], [pBrCommits, pBrLines]])
# add gridplot to tab
tabCommits = Panel(child=gpCommits, title='Changes')

# branches
gpLines = []
for br in brs:
    brUsers = counter.branches[brs.index(br)].users
    brCommits = counter.branches[brs.index(br)].userCommits
    #print(br)
    #print(users)
    #print(commits)
    colors = []
    for user in brUsers:
        colors.append(Set3[12][brUsers.index(user)])
    angles = []
    for commit in brCommits:
    	angles.append(commit/sum(brCommits)*2*pi)
    cdSource = ColumnDataSource(data=dict(username=brUsers, commits=brCommits, angle=angles, color=colors))
    pBranch = figure(plot_height=350, title=br, tooltips=tipsCommits)
    pBranch.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color',	legend_field='username', source=cdSource)
    pBranch.axis.axis_label=None
    pBranch.axis.visible=False
    pBranch.grid.grid_line_color = None # 网格线颜色

    gpLine = [pBranch]
    gpLines.append(gpLine)

gpBranches = gridplot(gpLines)
tabBranches = Panel(child=gpBranches, title='Branches')

# users
gpLines = []
for user in users:
    userBrs = counter.users[users.index(user)].branches
    userCommits = counter.users[users.index(user)].brCommits
    #print(user)
    #print(userBrs)
    #print(userCommits)
    colors = []
    for br in userBrs:
        colors.append(Set3[12][userBrs.index(br)])
    angles = []
    for commit in userCommits:
    	angles.append(commit/sum(userCommits)*2*pi)
    cdSource = ColumnDataSource(data=dict(branch=userBrs, commits=userCommits, angle=angles, color=colors))
    pUser = figure(plot_height=350, title=user, tooltips=tipsBrCommits)
    pUser.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color',	legend_field='branch', source=cdSource)
    pUser.axis.axis_label=None
    pUser.axis.visible=False
    pUser.grid.grid_line_color = None # 网格线颜色

    gpLine = [pUser]
    gpLines.append(gpLine)

gpUsers = gridplot(gpLines)
tabUsers = Panel(child=gpUsers, title='Authors')

# add gridplot to tab
tabs = Tabs(tabs=[tabCommits, tabBranches, tabUsers])
#tabs = Tabs(tabs=[tabCommits])
# save file
save(tabs)
