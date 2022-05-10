import datetime, calendar

class gerritDate():
    def __init__(self, period):
        self.today = datetime.datetime.today()
        if period == 'month':
            # find last month 1st day
            if self.today.month == 1:
                month = 12
                year = self.today.year - 1
            else:
                month = self.today.month - 1
                year = self.today.year
            day = 1
            self.startDate = datetime.date(year, month, day)
            self.endDate = datetime.date(self.today.year, self.today.month, day)
        else:
            # find last monday
            self.endDate = self.today
            while self.endDate.weekday() != calendar.MONDAY:
                self.endDate = self.endDate + datetime.timedelta(days=-1)
            self.startDate = self.endDate + datetime.timedelta(days=-7)

    def getStart(self):
        return self.startDate.strftime('%Y-%m-%d')
    
    def getEnd(self):
        return self.endDate.strftime('%Y-%m-%d')
