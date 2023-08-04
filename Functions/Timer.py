from datetime import datetime

class Timer():

    def now(self):
        return datetime.now()

    def currentTime(self):
        return self.now().strftime("""%H:%M:%S.%f""")
    
    def currentDayMonthYear(self):
        return self.now().strftime("""%Y-%m-%d""")

    def currentMonth(self, is_decimal=True):
        if is_decimal:
            return self.now().strftime("""%m""")
        return self.now().strftime("""%B""")
    
    def currentWeekday(self, is_decimal=True):
        if is_decimal:
            return self.now().strftime("""%w""")
        return self.now().strftime("""%A""")

    def getTimer(self):
        return {
            "time": self.currentTime(),
            "day": self.currentDayMonthYear(),
            "weekday": self.currentWeekday()
        }