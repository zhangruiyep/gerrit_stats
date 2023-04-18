import datetime, calendar

class GerritDate():
    def __init__(self, time_period):
        if time_period not in ['month', 'week']:
            raise ValueError('time_period must be month or week')
            
        self.today = datetime.datetime.today()
        self.period = time_period
        
        if time_period == 'month':
            self.start_date = self.get_last_month_start()
        else:
            self.start_date = self.get_last_week_start()
            
        self.end_date = datetime.date(self.today.year, self.today.month, self.today.day)
        
    def __repr__(self):
        return f'GerritDate({self.period!r}), start_date: {self.start_date!r}, end_date: {self.end_date!r}'
        
    def get_last_month_start(self):
        if self.today.month == 1:
            month = 12 
            year = self.today.year - 1
        else:
            month = self.today.month - 1
            year = self.today.year
        return datetime.date(year, month, 1)
    
    def get_last_week_start(self):
        last_day = self.today - datetime.timedelta(days=7)
        while last_day.isoweekday() != 1:
            last_day -= datetime.timedelta(days=1)
        return last_day
    
    def get_start(self):
        return self.start_date.strftime('%Y-%m-%d')

    def get_end(self):
        return self.end_date.strftime('%Y-%m-%d')
