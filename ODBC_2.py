# sqlite3 не стоит использовать примногопользовательских мгнвенных изменениях

import pyodbc
import json

connection_string = "Driver={ODBC Driver 17 for SQL Server};"\
"Server=tcp:84.252.140.138;"\
"Database=Cinema;"\
"uid=ucinema;pwd=P@sswordCinema;"

conn = pyodbc.connect(connection_string)
# Подключились к SQL серверу

# Нужно создать таблицу  https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27
# https://blog.finxter.com/creating-a-database-table-using-the-package-pyodbc-in-python/
# table
cursor = conn.cursor()

# nvarchar(4000) для правильной кодировки данных
cursor.execute('''
CREATE TABLE Kinoagentstvo (
Link nvarchar(4000),
Description nvarchar(4000),
Photo nvarchar(4000),
Address nvarchar(4000),
Price integer,
);
''')
conn.commit()

with open("data_file.json", "r") as write_file:
    info = json.load(write_file)

# Теперь внесем все наши данные в таблицу
for obj in range(len(info)):
    link = info[obj]['link']
    description = info[obj]['description']
    photo = ''
    for k in range(min(10, len(info[obj]['photo']))):
        photo += info[obj]['photo'][k] + " "
    address = info[obj]['header']
    price = info[obj]['price']

    sql = "INSERT INTO Kinoagentstvo (Link, Description, Photo, Address, Price) VALUES  (?, ?, ?, ?, ?)"
    val = [(link, description, photo, address, price)]
    cursor.executemany(sql, val)
    conn.commit()

conn.close()
