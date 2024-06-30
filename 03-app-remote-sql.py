# Flask module - will provide us the application instance
# request module - will allow to add methods to roads
# jsonify - will encode python dictionaries into json strings

from flask import Flask, request, jsonify
import json


## importing 'pymysql' module to create connection with database
import pymysql


app = Flask(__name__) # consturctor / dunder  __name__ which is the main module

# we will be using sqlite module to store our values in database
# we have already created the database using db.py file

# now creating the connection with sqlite database to make any query in database
# instead of creating connection every time we can define it in a function 


def db_connection():
    conn = None
    try:
        conn = pymysql.connect(

            host='sql12.freesqldatabase.com',
            database='sql12717334',
            user='sql12717334',
            password='yourPWD123',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor

        ) # creating connection
    except pymysql.error as e:
        print(e)
    return conn # returning the connection

@app.route('/books', methods=['GET','POST']) #decorator
def books():
    conn = db_connection() # making connection and saving it in variable
    cursor = conn.cursor() # used to execute SQL queries

    if request.method == "GET": # executing the query under GET request
        cursor.execute("SELECT * FROM book") # saving the result in cursor variable
        books = [

            # iterating through this object to get all the items in the result bu calling 
            # fetchall() method , we need to pass dict keys of our coulmn name
            dict(id=row['id'], author=row['author'],
            language=row['language'],title=row['title'])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
        else:
            return jsonify('no data found!')


    if request.method == 'POST':

        # we need to get the form values 

        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        ## we don't need to define ID as it will be automatically added to DB
        # iD = books_list[-1]['id']+1  

        # writing INSERT Query in DB, We need to mention all columns and put '%s' as a placeholders
        # and add values in a dynamic way 

        sql = """INSERT INTO book (author, language, title)
                VALUES (%s,%s,%s)

                """

        # exicuting this query and pass it in form of TUPLE
        cursor.execute(sql, (new_author, new_lang, new_title))
        last_id=cursor.lastrowid
        conn.commit() # to save the change in our DB we need to call commit() method

        # To confirm our request we will grab the ID of the Object by using 'lastrowid'
        
        return f"Book with the id: {last_id} created successfully", 201


# id we will get from the endpoint i.e. localhost:5000/book/'id' from requestor

@app.route('/book/<int:id>', methods=['GET','PUT','DELETE']) 
def single_book(id):

    #  again defining the connection and creating cursor to execute queries
    conn = db_connection()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        # ID is Primary Key so it will be unique
        cursor.execute("SELECT * FROM book WHERE id=%s",(id,)) 
        # using .fetchall() function to fetch the result of query
        rows = cursor.fetchall() # storing the query data in rows variable
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "No Result found", 404


    if request.method == 'PUT':
        # Writing SQL Query for Put operation
        sql = """UPDATE book
                SET     title=%s,
                        author=%s,
                        language=%s
                WHERE id=%s 
            """

        # we need to grab updated values(body) from requestor

        author = request.form['author']
        language = request.form['language']
        title = request.form['title']

        updated_book = {
            "id": id,
            "author": author,
            "language": language,
            "title": title
        }
        # executing UPDATE SQL query using Execute() function
        cursor = cursor.execute(sql,(author, language, title, id)) # passing the id 
        conn.commit()
        return jsonify(updated_book)

    if request.method == 'DELETE':
        sql = """ DELETE FROM book WHERE id=%s"""
        cursor = cursor.execute(sql,(id,))
        conn.commit()
        return "The book with id: {} has been deleted!".format(id), 200
    

if __name__ == '__main__':
    app.run(debug=True)