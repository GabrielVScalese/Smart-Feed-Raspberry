import sys
sys.path.append('./')

import datetime
from time_controller import TimeController

date1 = datetime.datetime.strptime('2021-10-05 00:00:00Z', '%Y-%m-%d %H:%M:%SZ')
date2 = datetime.datetime.strptime('2021-10-04 23:00:00Z', '%Y-%m-%d %H:%M:%SZ')

print(TimeController.oneDayDiff(date1))
print(TimeController.oneDayDiff(date2))