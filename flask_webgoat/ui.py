from pathlib import Path
import sqlite3
import subprocess
from flask import request

from flask import (
    Blueprint, jsonify, request, jsonify, session, render_template
)
from flask import current_app as app
from . import query_db

bp = Blueprint('ui', __name__)


@bp.route('/search')
def search():
    query_param = request.args.get('query')
    if query_param is None:
        message = 'please provide the query parameter'
        return render_template('error.html', message=message)

    try:
        query = "SELECT username, access_level FROM user WHERE username LIKE ?;"
        results = query_db(query, (query_param,))
        return render_template('search.html', results=results, num_results=len(results), query=query_param)
    except sqlite3.Error as err:
        message = 'Error while executing query ' + query_param
        return render_template('error.html', message=message)
