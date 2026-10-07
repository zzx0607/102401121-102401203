"""数据访问层：所有用户输入都通过 SQL 参数传入。"""
from database import get_db


def create_post(data, owner_id, image=None):
    db = get_db()
    with db:
        cursor = db.execute(
            """INSERT INTO posts(owner_id,type,name,cat,place,time,description,contact,image)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (owner_id, data['type'], data['name'], data['cat'], data['place'],
             data['time'], data['description'], data['contact'], image))
    return cursor.lastrowid


def get_post(post_id):
    row = get_db().execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    return dict(row) if row else None


def list_posts(owner_id=None):
    if owner_id:
        rows = get_db().execute(
            'SELECT * FROM posts WHERE owner_id=? ORDER BY id DESC', (owner_id,)).fetchall()
    else:
        rows = get_db().execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    return [dict(row) for row in rows]


def finish_post(post_id, owner_id):
    """仅发布者本人可以结束进行中的记录；重复结束不改变任何数据。"""
    db = get_db()
    with db:
        cursor = db.execute(
            "UPDATE posts SET done=1 WHERE id=? AND owner_id=? AND done=0",
            (post_id, owner_id))
    return cursor.rowcount > 0


def delete_post(post_id, owner_id):
    """仅发布者本人可以删除记录，图片文件由调用方负责清理。"""
    db = get_db()
    with db:
        db.execute('DELETE FROM posts WHERE id=? AND owner_id=?', (post_id, owner_id))
