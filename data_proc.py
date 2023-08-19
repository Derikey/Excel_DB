CMD_SHOW = 1
CMD_SORT = 2
CMD_EXIT = 3

class TWork:
  date = ''
  week_d = ''
  time_ppl = ''
  time_work = ''
  admin = ''
  payment = 0
  concert = ''
  workers = []

dbName = 'work_database.csv'
dbSize = 100

data = []

with open('work_database.csv', 'r') as f:
  for line in f:
    x = line.rstrip().split(';')
    for i in range(7, len(x)):
      x[i] = x[i].strip()
    W = TWork()
    W.date, W.week_d, W.time_ppl, W.time_work, W.admin, W.payment, W.concert = x[:7]
    W.workers = sorted(x[7:])
    data.append(W)

def Error(n):
  if n == 0:  print('Введен неверный формат данных.')
  if n == 1:  print('Введена неверная команда.')

def menu():
  while True:
    try:
      cmd = int(input('''Выберите действие:
    1 - просмотр данных
    2 - сортировка
    3 - выход
    '''))
      if cmd in [CMD_SHOW, CMD_SORT, CMD_EXIT]:
        break;
      else: Error(1)
    except:
      Error(0)
      return
  return cmd

def showData(data):
  print('\nБаза данных "Работа":')
  print('-'*140)
  print(f'{" "*7}{"Дата":23}{"Время":7}{"Админ":10}{"Оплата":8}{"Название концерта":20}{"Рабочие":63}')
  for i in range(len(data)):
    print(f'\n {i+1:4}. {data[i].date:20}{data[i].week_d:3}{data[i].time_work:7}{data[i].admin:10}{data[i].payment:8}{data[i].concert:20}', end = '')
    for j in range(len(data[i].workers)):
      print(f'{data[i].workers[j]:9}', end = '')
  print('\n','-'*140)

def sortData():
  key = 2
  keys = []
  data_s = []
  while key != 4:
    if keys:
      key = int(input('''Выбирете функцию:
        1. Показать текущие фильтры
        2. Добавить фильтры
        3. Сброить фильтры
        4. Выйти
      '''))
    if key == 1: print(*keys, sep=',')
    if key == 2:
      sort_key = int(input('''Выберите ключи для сортировки:
        1. Дата
        2. День недели
        3. Время начала
        4. Время прихода
        5. Админ
        6. Оплата
        7. Название концерта
        8. Рабочие
        '''))
      var = str(input())
      keys.append({sort_key})
      if not data_s:
        data_s = [x for x in data if var in list(x.__dict__.values())[sort_key-1]]
        showData(data_s)
      else:
        data_s = [x for x in data_s if var in list(x.__dict__.values())[sort_key-1]]
        showData(data_s)
    if key == 3:
      keys = []
      data_s = data
      key = 2

#-----------------------------------
#  Основная программа
#-----------------------------------
cmd = 0
while cmd != CMD_EXIT:
  cmd = menu()
  if cmd == CMD_SHOW:   showData(data)
  if cmd == CMD_SORT:   sortData()
print('Работа закончена.')