import pyodbc

connection_string = "Driver={ODBC Driver 17 for SQL Server};"\
"Server=tcp:84.252.140.138;"\
"Database=Cinema;"\
"uid=ucinema;pwd=P@sswordCinema;"

print(connection_string)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor() # Подключились к SQL серверу

# Нужно создать таблицу
cursor.execute('''
CREATE TABLE MoskvaN1
(
Link nvarchar(4000),
Description nvarchar(4000),
Address nvarchar(4000),
Price int,
Photo TEXT
)
''')