import sys
sys.path.append('./')

from consumptions_repository import ConsumptionsRepository
import datetime

nowDate = datetime.datetime.now()
stringNowDate = nowDate.strftime("%Y-%m-%d %H:%M:%SZ")
response = ConsumptionsRepository.createConsumption({'pet_id': 147 , 'date': stringNowDate, 'quantity': 109 })
print(response)