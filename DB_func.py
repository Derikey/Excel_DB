def menu(data):
  data_work = data
  CMD_SHOW, CMD_SORT, CMD_PAYMENT, CMD_MONTH = 1, 2, 3, 4
  CMD_EXIT = 0
  while True:
    #try:
      cmd = int(input('''Выберите действие:
      1 - просмотр данных
      2 - сортировка
      3 - вычисление зарплаты
      4 - Сменить месяц обработки
      0 - выход
'''))
      if cmd == CMD_EXIT:       break
      elif cmd == CMD_SHOW:     showData(data_work)
      elif cmd == CMD_SORT:     keys_active, data_work = sort(data_work, data)
      elif cmd == CMD_PAYMENT:  calcPayment(data_work)
      elif cmd == CMD_MONTH:
        month = monthChoose(True)
        data_work = read(month)
        data = data_work
        keys_active = {}
      else: Error(1)
    #except: Error(0)



def Error(n):
  if n == 0:  print('Введен неверный формат данных.')
  if n == 1:  print('Введена неверная команда.')



def monthChoose(update):
  from datetime import datetime
  months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
  if update:
    month = input('Выберете номер или название месяца для обработки данных: ')
    if any(x.isalpha() for x in month):
      month = month[0].upper() + month[1:].lower()
    else: month = months[int(month)-1]
  else: month = months[datetime.now().month-1]

  return month

def update(month):
  import httplib2
  import apiclient.discovery
  from oauth2client.service_account import ServiceAccountCredentials

  CREDENTIALS_FILE = 'creds.json'
  spreadsheet_id = '1RHSskz9xMNFNsWGI6Qlrds3zvCU5lYvx0saKWXv8q6I'
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      CREDENTIALS_FILE,
      ['https://www.googleapis.com/auth/spreadsheets',
       'https://www.googleapis.com/auth/drive'])
  httpAuth = credentials.authorize(httplib2.Http())
  service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

  table = service.spreadsheets().values().get(
      spreadsheetId = spreadsheet_id,
      range = f'{month}!B1:AA14',
      majorDimension = 'COLUMNS'
  ).execute()['values']

  with open(f'DataBase/work_database_{month}.csv', 'w+') as file:
    for x in table:
      print(*x, sep=';', file=file)

  print(f'Обновление базы данных за {month} завершено.')



def read(month):
  from os.path import isfile

  class TWork:
    date = ''
    week_d = ''
    time_ppl = ''
    time_work = ''
    admin = ''
    payment = ''
    concert = ''
    workers = []

  data = []
  if isfile(f'DataBase/work_database_{month}.csv'):
    with open(f'DataBase/work_database_{month}.csv', 'r') as file:
      for line in file:
        x = line.rstrip().split(';')
        for i in range(len(x)):
          x[i] = x[i].strip()
        W = TWork()
        W.date, W.week_d, W.time_ppl, W.time_work, W.admin = x[:5]
        W.workers = sorted(x[5:-2])
        W.payment, W.concert = x[-2:]
        if any(x != '' for x in W.workers ): data.append(W)
  else:
    update(month)
    read(month)
  return data



def showData(data):
  leng = 160
  print('\nБаза данных "Работа":')
  print('-'*leng)
  print(f'{" "*7}{"Дата":25}{"Время":7}{"Админ":13}{"Оплата":7}{"Название концерта":20}{"Рабочие"}')
  for i in range(len(data)):
    print(f'\n {i+1:4}. {data[i].date:23}{data[i].week_d:3}{data[i].time_work:6}{data[i].admin:13}{data[i].payment:7}{data[i].concert:20}', end = '')
    for el in data[i].workers[::-1]:
      print(f'{el:10}', end = '')
  print('\n','-'*leng)




def sort(data, old_data):
  try: keys_active = keys_active
  except: keys_active = {}
  keys = ['date', 'week_d', 'time_ppl', 'time_workers', 'admin', 'workers', 'payment', 'concert']
  keys_ru = ['Дата', 'День недели', 'Время начала', 'Время прихода', 'Админ', 'Рабочие', 'Оплата', 'Название концерта']
  data_work = []
  while True:
    cmd = int(input('''Выбирете функцию:
        1 - Показать текущие фильтры
        2 - Добавить фильтры
        3 - Сброить фильтры
        0 - Выйти
'''))
    if cmd == 0: return keys_active, data_work
    if cmd == 1:
      if keys_active:
        for i in keys_active.keys():
          print(f'{keys_ru[keys.index(i)]}: {", ".join(keys_active[i])}')
      else: print('Нет активных ключей сортировки.')
    if cmd == 2:
      sort_key = int(input('''Выберите тип ключа для сортировки:
        1. Дата (диапазон)
        2. День недели
        3. Время начала
        4. Время прихода
        5. Админ
        6. Рабочие
        7. Оплата
        8. Название концерта
'''))
      if sort_key == 1:
        d1, d2 = map(int, input('Введите рамки диапазона через пробел: ').split())
        data_work = [x for x in data
          if (d1 <= int(list(x.__dict__.values())[0][:2]) <= d2)]
        if keys[sort_key-1] in keys_active.keys():
          keys_active[keys[sort_key-1]] += [f'{d1} - {d2}']
        else: keys_active[keys[sort_key-1]] = [f'{d1} - {d2}']

      else:
        var = str(input('Введите ключ: '))
        if keys[sort_key-1] in keys_active.keys():
          keys_active[keys[sort_key-1]] += [var]
        else: keys_active[keys[sort_key-1]] = [var]

        if not data_work:
          data_work = [x for x in data
            if var in list(x.__dict__.values())[sort_key-1]]
        else:
          data_work = [x for x in data_work
            if var in list(x.__dict__.values())[sort_key-1]]
      showData(data_work)

    if cmd == 3:
      data_work = old_data
      keys_active = {}



def calcPayment(data):
  payment = 0
  for x in data:
    payment += int(list(x.__dict__.values())[6])
  print(f'Выплата составляет {payment}р.')