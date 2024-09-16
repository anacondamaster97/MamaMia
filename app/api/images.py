from flask import Blueprint, jsonify, request
from ..models.post_model import Post
from .. import db

images_blueprint = Blueprint('images', __name__)

@images_blueprint.route('/', methods=['GET'])
def get_image():
    images = Post.query.all()
    image_data = [{'id': post.id, 'image': image.title, 'content': image.content} for image in images]
    return jsonify(image_data), 200

@images_blueprint.route('/', methods=['POST'])
def create_image():
    data = request.get_json()
    new_image = Post(title=data['title'], content=data['content'], image_id=data['image_id'])
    db.session.add(new_image)
    db.session.commit()
    return jsonify({'message': 'Post created'}), 201
