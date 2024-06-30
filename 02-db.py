import sqlite3

# we need to make connection to sql-lite database using sqlite3 module

# calling connect method of sqlite3
# if database represented by the file does'nt exist one will be created automatically at the path
conn = sqlite3.connect('books.sqlite') 


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