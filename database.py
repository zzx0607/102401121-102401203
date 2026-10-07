import sqlite3
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('寻物', '招领')),
    name TEXT NOT NULL,
    cat TEXT NOT NULL,
    place TEXT NOT NULL,
    time TEXT NOT NULL,
    description TEXT NOT NULL,
    contact TEXT NOT NULL,
    image TEXT,
    done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','+8 hours'))
);
CREATE INDEX IF NOT EXISTS idx_posts_owner ON posts(owner_id);
"""


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], timeout=10)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.executescript(SCHEMA)
        db.commit()
