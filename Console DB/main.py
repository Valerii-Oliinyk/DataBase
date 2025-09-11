import pyodbc as odbc

DRIVER_NAME = 'ODBC Driver 18 for SQL Server'
SERVER_NAME = 'student-sql-server-822931182'
DATABASE_NAME = 'voliynik'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""

conn = odbc.connect(connection_string)
print(conn)

#cursor = connection.cursor()
#cursor.execute('SELECT * FROM CustomersData')
