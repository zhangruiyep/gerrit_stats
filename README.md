# gerrit_stats

一个用来统计gerrit提交的小工具。

一直没有找到合适的工具，git_stats等工具只能统计单分支的情况。所以自己用python做了一个。

### 支持的功能：

统计所有owner的commit和line数量，柱状图。

统计所有branch的commit和line数量，柱状图。

统计单个branch上各owner的commit占比，饼图。

统计单个owner在各branch上的commit占比，饼图。

可以按周或月为单位统计。

### 环境需求：

Python 3.x

bokeh

Gerrit REST API的权限

### 用法：

python gerrit_stats_html.py [week|month]

week: 默认。从上周一开始，到本周一结束。

month: 从上月1日开始，到本月1日结束。
