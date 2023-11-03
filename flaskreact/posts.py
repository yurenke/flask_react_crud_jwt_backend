from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flaskreact.models import db, Post
from sqlalchemy.orm import joinedload

bp = Blueprint("posts", __name__, url_prefix="/v1/posts")
    
@bp.route("/", methods=["GET", "POST"], strict_slashes=False)
@jwt_required()
def list_or_create_posts():
    if request.method == 'POST':
        author = get_jwt_identity()
        title = request.json.get('title', None)
        content = request.json.get('content', '')

        if not title:
            return jsonify({'message': 'title is required'}), 400
        
        newpost = Post(title=title, content=content, author_id=author)
    
        db.session.add(newpost)
        db.session.commit()
        return jsonify({'message': 'new post created successfully'})
    
    args = request.args
    per_page = 5
    if not args:
        page = 1
        term = None
    
    page = args.get('page', default=1, type=int)
    term = args.get('term', default=None, type=str)

    # .filter(Post.title.like(title))\
    if term:
        postspaging = db.session.query(Post)\
            .options(joinedload(Post.accounts))\
            .filter(Post.__ts_vector__.match(term, postgresql_regconfig='english'))\
            .order_by(Post.update_time.desc())\
            .paginate(page=page, per_page=per_page)
    else:
        postspaging = db.session.query(Post)\
            .options(joinedload(Post.accounts))\
            .order_by(Post.update_time.desc())\
            .paginate(page=page, per_page=per_page)

    totalPages = postspaging.pages
    next_page = postspaging.next_num
    if next_page == None:
        next_page = -1
        
    prev_page = postspaging.prev_num
    if prev_page == None:
        prev_page = -1
         
    return jsonify({
        'totalPages': totalPages,
        'next_page': next_page,
        'prev_page': prev_page,
        'results': [{'id': post.id, 'title': post.title, 'content': post.content, 
                     "create_time": post.create_time.strftime("%m/%d/%Y, %H:%M"), 
                     'update_time': post.update_time.strftime("%m/%d/%Y, %H:%M"), 
                     'author_name': post.accounts.name,
                     'author_email': post.accounts.email} for post in postspaging.items]
    })

@bp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def single_post(id):
    current_user_id = get_jwt_identity()
    # post = Post.query.get(id)
    post = db.session.query(Post)\
            .filter(Post.id == id)\
            .one()
    if not post:
        return jsonify({"message": "not found"}), 404
    
    if request.method == 'PUT':
        if post.author_id != current_user_id:
            return jsonify({"message": "not allowed to edit other person's post"}), 401
        
        title = request.json.get('title', None)
        content = request.json.get('content', '')

        if not title:
            return jsonify({'message': 'title is required'}), 400
        
        post.title = title
        post.content = content
  
        db.session.commit()
        return jsonify({'message': "successfully updated"})
    
    elif request.method == 'DELETE':
        if post.author_id != current_user_id:
            return jsonify({"message": "not allowed to delete other person's post"}), 401
        
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "successfully delete the post"})
    
    return jsonify({"id": post.id, "title": post.title, "content": post.content, 
                    "create_time": post.create_time.strftime("%m/%d/%Y, %H:%M"), 
                    "update_time": post.update_time.strftime("%m/%d/%Y, %H:%M"), 
                    "author": post.accounts.name})
