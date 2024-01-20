from flask import render_template, request, session

from app import app
from utils import get_db_connection
from models.search_model import get_book, borrow_book


@app.route('/search', methods=['get'])
def search():
    conn = get_db_connection()

    if request.values.get('name'):
        name = str(request.values.get('name'))
    else:
        name = ""
    if request.values.get('genre'):
        genre = str(request.values.get('genre'))
    else:
        genre = ""
    if request.values.get('author'):
        author = str(request.values.get('author'))
    else:
        author = ""
    if request.values.get('publisher'):
        publisher = str(request.values.get('publisher'))
    else:
        publisher = ""

    if request.values.get('book_id'):
        borrow_book(conn, int(request.values.get('book_id')), int(request.values.get('reader_id')))

    df_book = get_book(conn, int(request.values.get('reader_id')), name, genre, author, publisher)

    html = render_template(
        'search.html',
        name=name,
        genre=genre,
        author=author,
        publisher=publisher,
        reader_id=int(request.values.get('reader_id')),
        book=df_book,

        len=len
    )
    return html