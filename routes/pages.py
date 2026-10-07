from flask import Blueprint, render_template, request, session, current_app, send_from_directory
import models
from services.post_service import require_post, CATEGORIES, status_label
from services.search_service import search_posts, similar_posts
bp = Blueprint('pages', __name__)

@bp.get('/')
def index():
    filters = {key:request.args.get(key,'') for key in ('q','type','cat','place','status')}
    posts = search_posts(models.list_posts(), **filters)
    return render_template('index.html', title='寻回 · 失物招领', posts=posts,
                           filters=filters, categories=CATEGORIES)

@bp.get('/publish')
def publish():
    return render_template('publish.html', title='发布信息', categories=CATEGORIES)

@bp.get('/posts/<int:post_id>')
def detail(post_id):
    post = require_post(post_id)
    return render_template('detail.html', title='信息详情', post=post,
                           similar=similar_posts(post, models.list_posts()),
                           status_label=status_label, visitor_id=session['visitor_id'])

@bp.get('/my-posts')
def my_posts():
    return render_template('my_posts.html', title='我的发布',
                           posts=models.list_posts(owner_id=session['visitor_id']))

@bp.get('/uploads/<name>')
def uploaded(name):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], name)
