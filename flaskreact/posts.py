from datetime import datetime
from datetime import timedelta
from datetime import timezone
import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, create_access_token
from flask_jwt_extended import jwt_required
from flaskreact.models import db, Account, Post

bp = Blueprint("posts", __name__, url_prefix="/posts")

# @bp.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             data = response.get_json()
#             if type(data) is dict:
#                 data["accessToken"] = access_token 
#                 response.data = json.dumps(data)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response
    
@bp.route("/all", methods=["GET"])
@jwt_required()
def list_posts():
    args = request.args
    per_page = 5
    if not args:
        page = 1
        term = None
    
    page = args.get('page', default=1, type=int)
    term = args.get('term', default=None, type=str)

    # .filter(Post.title.like(title))\
    if term:
        postspaging = db.session.query(Post, Account)\
            .join(Account, Post.author_id == Account.id)\
            .filter(Post.__ts_vector__.match(term, postgresql_regconfig='english'))\
            .order_by(Post.update_time.desc())\
            .paginate(page=page, per_page=per_page)
    else:
        postspaging = db.session.query(Post, Account)\
            .join(Account, Post.author_id == Account.id)\
            .order_by(Post.update_time.desc())\
            .paginate(page=page, per_page=per_page)
    # postspaging = Post.query.join(Account).order_by(Post.update_time.desc()).paginate(page=page, per_page=per_page)

    # total = postspaging.total
    totalPages = postspaging.pages
    next_page = postspaging.next_num
    if next_page == None:
        next_page = -1
    # else:
    #     next_page_url = f"http://127.0.0.1:5000/posts?page={next_page}"
        
    prev_page = postspaging.prev_num
    if prev_page == None:
        prev_page = -1
    # else:
    #     prev_page_url = f"http://127.0.0.1:5000/posts?page={prev_page}"
         
    return jsonify({
        'totalPages': totalPages,
        'next_page': next_page,
        'prev_page': prev_page,
        'results': [{'id': post.id, 'title': post.title, 'content': post.content, 
                     "create_time": post.create_time.strftime("%m/%d/%Y, %H:%M"), 
                     'update_time': post.update_time.strftime("%m/%d/%Y, %H:%M"), 
                     'author_name': author.name,
                     'author_email': author.email} for post, author in postspaging.items]
    })

@bp.route("/create", methods=["POST"])
@jwt_required()
def create_post():
    author = get_jwt_identity()
    title = request.json.get('title', None)
    content = request.json.get('content', '')

    if not title:
        return jsonify({'message': 'title is required'}), 400
    
    newpost = Post(title=title, content=content, author_id=author)
 
    db.session.add(newpost)
    db.session.commit()
    return jsonify({'message': 'new post created successfully'})

@bp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def single_post(id):
    current_user_id = get_jwt_identity()
    post = Post.query.get(id)
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
