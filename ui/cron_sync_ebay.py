import requests as req
from datetime import datetime
req.get('http://35.153.183.121:3001/add-ebay-all-sellers-items/')
d=datetime.now()
last_updated_time=d.strftime('%d/%m/%y %H:%M')
print("last updated = ",last_updated_time)
