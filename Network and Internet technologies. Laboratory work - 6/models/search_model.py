import datetime
import pandas


def get_book(conn, reader_id, name, genre, author, publisher):
    return pandas.read_sql('''
        WITH get_reader( book_id, status )
        AS(
            SELECT
                book_id, "disabled" AS 'status'
            FROM
                reader
                JOIN book_reader USING(reader_id)
            WHERE
                reader.reader_id == :reader AND
                book_reader.return_date IS NULL
            GROUP BY book_id
        )
        
        SELECT
            book_id AS 'id', get_reader.status AS 'status',
            book.title AS 'name', genre.genre_name AS 'genre',
            author.author_name AS 'author', publisher.publisher_name AS 'publisher'
        FROM
            book
            JOIN genre USING(genre_id)
            JOIN book_author USING(book_id)
            JOIN author USING(author_id)
            JOIN publisher USING(publisher_id)
            LEFT JOIN get_reader USING(book_id)
        WHERE book.title LIKE :name AND genre.genre_name LIKE :genre AND
              author.author_name LIKE :author AND publisher.publisher_name LIKE :publisher AND
              book.available_numbers > 0
        GROUP BY book_id
    ''', conn, params={
        "reader": reader_id,
        "name": f"%{name}%",
        "genre": f"%{genre}%",
        "author": f"%{author}%",
        "publisher": f"%{publisher}%"
    })


def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE book
        SET available_numbers = available_numbers - 1
        WHERE book_id == {book_id}
    """)
    cur.execute(f"""
        INSERT INTO book_reader (book_id, reader_id, borrow_date, return_date) VALUES
        ({book_id}, {reader_id}, '{ datetime.datetime.now().strftime('%Y-%m-%d') }', NULL);
    """)

    conn.commit()

    return
