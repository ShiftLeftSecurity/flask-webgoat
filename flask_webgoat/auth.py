from flask import (
    Blueprint, jsonify, request, jsonify, session
)
from werkzeug.security import check_password_hash
from flask import current_app as app

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return jsonify({'error': 'username and password parameter have to be provided'}), 400

    query = "SELECT id, username, access_level FROM user WHERE username = '%s' AND password = '%s'" % (username, password)
    result = app.query_db(query, [], True)
    if result is None:
        return jsonify({'bad_login': True}), 400
    session['user_info'] = (result[0], result[1], result[2])
    return jsonify({'success': True})

