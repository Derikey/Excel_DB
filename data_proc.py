import DB_func as db

if __name__ == '__main__':
  cmd = 0
  month = db.monthChoose(False)
  data = db.read(month)
  db.menu(data)