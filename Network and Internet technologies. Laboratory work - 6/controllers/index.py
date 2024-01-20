from flask import render_template, request, session

from app import app
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, get_new_reader, return_the_book


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()

    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id

    elif request.values.get('new_reader'):
        new_reader = request.values.get('new_reader')
        session['reader_id'] = get_new_reader(conn, new_reader)

    else:
        session['reader_id'] = 1

    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    html = render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len
    )
    return html


@app.route('/return_book', methods=['get'])
def return_book():
    conn = get_db_connection()

    if request.values.get('book_reader_id'):
        book_reader_id = int(request.values.get('book_reader_id'))
        reader_id = return_the_book(conn, book_reader_id)
    else:
        reader_id = 1

    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, reader_id)

    html = render_template(
        'index.html',
        reader_id=reader_id,
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len
    )
    return html
