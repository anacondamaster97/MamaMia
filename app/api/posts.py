from flask import Blueprint, jsonify, request
from ..models.post_model import Post
from .. import db

posts_blueprint = Blueprint('posts', __name__)

@posts_blueprint.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_data = [{'id': post.id, 'title': post.title, 'content': post.content} for post in posts]
    return jsonify(posts_data), 200

@posts_blueprint.route('/', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created'}), 201
