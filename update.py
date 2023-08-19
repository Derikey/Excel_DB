import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1RHSskz9xMNFNsWGI6Qlrds3zvCU5lYvx0saKWXv8q6I'
# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

class TWork:
  date = ''
  week_d = ''
  time_ppl = ''
  time_work = ''
  admin = ''
  payment = 0
  concert = ''
  workers = []

### Чтение данных
# Чтение имен
month = input('Введите название месяца для скачивания: ')
tabl = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range=f"'{month}'!B1:AA14",
    majorDimension='COLUMNS'
).execute()


### Работа с данными
data = []
for x in tabl['values']:
  try:
    W = TWork()
    W.date, W.week_d, W.time_ppl, W.time_work, W.admin, W.payment, W.concert = x[:5] + x[-2:]
    W.workers = x[5:-2]
    data.append(W)
  except: continue
with open(f'../DataBase/work_database_{month.lower()}.csv', 'w+') as f:
  for W in data:
    print(W.date, W.week_d, W.time_ppl, W.time_work, W.admin, W.payment, W.concert, *W.workers, sep=';', file=f)
