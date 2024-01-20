from flask import render_template, request, session

from app import app


@app.route('/new_reader', methods=['get'])
def new_reader():
    return render_template(
        'new_reader.html'
    )
