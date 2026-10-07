from flask import Blueprint, request, jsonify, session, url_for
import models
from services.post_service import validate_post, require_post, require_owner, finish, status_label
from services.search_service import search_posts
from services.image_service import save_image, remove_image
bp = Blueprint('posts', __name__, url_prefix='/api/posts')

def public(post, detailed=False):
    result = {key:post[key] for key in ('id','type','name','cat','place','time','description','image','done','created_at')}
    result['mine'] = post['owner_id'] == session['visitor_id']
    result['status_label'] = status_label(post)
    if detailed:
        result['contact'] = post['contact']
    return result

@bp.get('')
def search():
    filters = {key:request.args.get(key,'') for key in ('q','type','cat','place','status')}
    return jsonify(posts=[public(p) for p in search_posts(models.list_posts(), **filters)])

@bp.post('')
def create():
    data = validate_post(request.form)
    image = save_image(request.files.get('image'))
    try:
        post_id = models.create_post(data, session['visitor_id'], image)
    except Exception:
        remove_image(image)
        raise
    return jsonify(post=public(require_post(post_id)), redirect=url_for('pages.detail', post_id=post_id, published=1)), 201

@bp.get('/<int:post_id>')
def detail(post_id):
    return jsonify(post=public(require_post(post_id), detailed=True))

@bp.patch('/<int:post_id>/finish')
def end(post_id):
    return jsonify(post=public(finish(post_id, session['visitor_id'])))

@bp.delete('/<int:post_id>')
def delete(post_id):
    post = require_owner(post_id, session['visitor_id'])
    models.delete_post(post_id, session['visitor_id'])
    remove_image(post['image'])
    return jsonify(ok=True)
