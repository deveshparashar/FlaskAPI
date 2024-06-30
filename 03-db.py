## importing 'pymysql' module to create connection with remote database
import pymysql

## passing credential for our database

conn = pymysql.connect(
    host='sql12.freesqldatabase.com',
    database='sql12717334',
    user='sql12717334',
    password='yourPWD1234',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Cursor Object: used to execute SQL statements on the sqlite database

cursor = conn.cursor()

# defining SQL Query to create or table 

sql_query = """    CREATE TABLE book (

        id integer PRIMARY KEY, 
        author text NOT NULL,
        language text NOT NULL,
        title text NOT NULL

)"""

# Now we need to execute this query 

cursor.execute(sql_query)

conn.close() # to close the database connection