import os
import sqlite3
from pathlib import Path

from flask import Flask, g


def create_app():
    app = Flask(__name__)
    app.secret_key = 'aeZ1iwoh2ree2mo0Eereireong4baitixaixu5Ee'

    db_filename = 'database.db'
    db_path = Path(db_filename)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_filename)
    create_table_query = """CREATE TABLE IF NOT EXISTS user
    (id INTEGER PRIMARY KEY, username TEXT, password TEXT, access_level INTEGER)"""
    conn.execute(create_table_query)

    insert_admin_query = """INSERT INTO user (id, username, password, access_level)
    VALUES (1, 'admin', 'maximumentropy', 0)"""
    conn.execute(insert_admin_query)
    conn.commit()
    conn.close()

    def query_db(query, args = (), one=False, commit=False):
        with sqlite3.connect(db_filename) as conn:
            cur = conn.execute(query, args)
            if commit:
                conn.commit()
            return cur.fetchone() if one else cur.fetchall()
    app.query_db = query_db

    with app.app_context():
        from . import status
        from . import auth
        from . import users
        from . import actions
        app.register_blueprint(status.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(users.bp)
        app.register_blueprint(actions.bp)
        return app

