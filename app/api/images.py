from flask import Blueprint, jsonify, request
from ..models.post_model import Post
from .. import db

images_blueprint = Blueprint('images', __name__)

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@images_blueprint.route('/', methods=['POST'])
def create_image():
    UPLOAD_FOLDER = 'uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in request'}), 400
    
    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({'error': 'No files uploaded'}), 400

    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            saved_files.append(filename)
        else:
            return jsonify({'error': f'File type not allowed for {file.filename}'}), 400

    return jsonify({'message': 'Files uploaded successfully', 'files': saved_files}), 200

@images_blueprint.route('/', methods=['GET'])
def get_image():
    images = Post.query.all()
    image_data = [{'id': post.id, 'image': image.title, 'content': image.content} for image in images]
    return jsonify(image_data), 200

"""@images_blueprint.route('/', methods=['POST'])
def create_image():
    data = request.get_json()
    new_image = Post(title=data['title'], content=data['content'], image_id=data['image_id'])
    db.session.add(new_image)
    db.session.commit()
    return jsonify({'message': 'Post created'}), 201"""
