import datetime
import pytz

def convertToDate (time):   
    tz = pytz.timezone('America/Sao_Paulo')
    hour = int(time.split(':')[0])
    minute = int(time.split(':')[1])
    
    nowDate = datetime.datetime.now(tz)
    newDate = nowDate.replace(hour=hour, minute=minute, second=0, microsecond=0)

    return newDate

class TimeController:

    @staticmethod
    def oneDayDiff (date):
        nowDate = datetime.datetime.now()
        nowDate = nowDate.replace(hour=0, minute=0, second=0, microsecond=0)

        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        ret = nowDate - date
        
        if ret.days == 1:
            return True
        
        return False

    @staticmethod
    def nowIsValid (times):
        tz = pytz.timezone('America/Sao_Paulo')
        
        nowDate = datetime.datetime.now(tz)
        for time in times:
            date = convertToDate(time)
            minDate = date
            maxDate = date.replace(minute=date.minute + 1)

            if nowDate >= minDate and nowDate < maxDate:
                return True
            
        return False
