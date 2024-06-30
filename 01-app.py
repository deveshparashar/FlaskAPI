from flask import Flask, request, jsonify

# Flask module - will provide us the application instance
# request module - will allow to add methods to roads
# jsonify - will encode python dictionaries into json strings

app = Flask(__name__) # consturctor / dunder  __name__ which is the main module

# here we are using an in-memory list to store our books which allows 
# post data to sustain only on run time!

books_list = [

    {
        "id": 0,
        "author": "Chinua Achebe",
        "language": "English",
        "title": "Things Fall Apart",
    },
    {
        "id": 1,
        "author": "Hans Christian Andersen",
        "language": "Danish",
        "title": "Fairy tales",
    },
    {
        "id": 1,
        "author": "Amertya Sen",
        "language": "English",
        "title": "An Argumetative Indian",
    }

]

@app.route('/books', methods=['GET','POST']) #decorator
def books():
    if request.method == "GET":
        if len(books_list) > 0 :
            return jsonify(books_list)
        else: 
            'No record Found!', 404
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        iD = books_list[-1]['id']+1

        new_obj = {
            'id': iD,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }
        books_list.append(new_obj)
        return jsonify(books_list), 201

@app.route('/book/<int:id>', methods=['GET','PUT','DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
            else: 
                return 'No record Found!', 404
    if request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']
                updated_book = {
                    'id': id,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }
                return jsonify(updated_book)

    if request.method == 'DELETE':
        for index,book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify(books_list)
    

if __name__ == '__main__':
    app.run(debug=True)