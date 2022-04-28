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

### 存在的问题：

统计时间的计算还不完善。按周统计时，从当前日期的前一个周一计算到当前日期。按月统计时，是从前一个月的1日计算到当前日期。

目前是每周一和每月1日定时触发，所以没有问题。后续考虑增加配置开始日期和结束日期。
