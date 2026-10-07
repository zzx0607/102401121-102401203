import sqlite3
import pytest
from app import create_app
from database import get_db
from conftest import publish

def test_persistence(app,client,data):
    id=publish(client,data).json['post']['id']
    restarted=create_app({'TESTING':True,'SECRET_KEY':'test-only',
        'DATABASE':app.config['DATABASE'],'UPLOAD_FOLDER':app.config['UPLOAD_FOLDER']})
    assert restarted.test_client().get(f'/api/posts/{id}').json['post']['name']==data['name']

def test_rollback(app,client,data):
    id=publish(client,data).json['post']['id']
    with app.app_context():
        db=get_db()
        with pytest.raises(sqlite3.IntegrityError):
            with db:
                db.execute('UPDATE posts SET name=? WHERE id=?',('错误更新',id))
                db.execute('UPDATE posts SET type=? WHERE id=?',('非法',id))
        assert db.execute('SELECT name FROM posts WHERE id=?',(id,)).fetchone()['name']==data['name']
