import os
from flask import Flask, redirect, url_for, flash, render_template, jsonify, request
from flask_login import login_required, logout_user, current_user, login_user
from .config import Config
from .models import db, login_manager, Users, Product, OAuth, Token
from .oauth import blueprint
from .cli import create_db
from flask_migrate import Migrate
from app.forms import RegistrationForm, LoginForm
import wtforms_json
import uuid
from flask_wtf import Form 
from sqlalchemy.orm.exc import NoResultFound
from flask_cors import CORS, cross_origin


wtforms_json.init()


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)
db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db, compare_type=True)

# if 'DATABASE_URL' not in os.environ:
#     POSTGRES = {
#         'user': os.environ['POSTGRES_USER'],
#         'pw': os.environ['POSTGRES_PWD'],
#         'db': os.environ['POSTGRES_DB'],
#         'host': os.environ['POSTGRES_HOST'],
#         'port': os.environ['POSTGRES_PORT'],
#     }    

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
# %(port)s/%(db)s' % POSTGRES
# local
# os.environ['DATABASE_URL'] = app.config['SQLALCHEMY_DATABASE_URI']


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# create db


@app.route("/logout", methods=['GET', 'OPTIONS'])
def logout():
    if current_user.is_anonymous:
        return jsonify({
            'success': True
        })
    token = Token.query.filter_by(user_id=current_user.id).first()
    print("token here", token)
    db.session.delete(token)
    db.session.commit()
    return jsonify({
        'success': True
    })


@app.route('/product/<product_id>', methods=['GET', 'POST'])
def single_products(product_id):
    data = Product.query.filter_by(id=product_id).first()
    if request.method == 'GET':
        product_details = {
            'name': data.name,
            'price': data.price,
            'category': data.category,
            'imageUrl': data.imageUrl,
            'pet_size': data.pet_size,
            'description': data.description,
            'count_rate': data.count_rate,
            'avg_rating': data.avg_rating,
            'seller_id': data.seller_id
    }   
        return jsonify(product_details)


@app.route('/category/<product_category>', methods=['GET', 'POST'])
def single_category(product_category):
    data = Product.query.filter_by(category=product_category).all()
    list_products_category = []
    for product in data:
        products = {
            'id':product.id,
            'name': product.name,
            'price': product.price,
            'category': product.category,
            'imageUrl': product.imageUrl,
            'pet_size': product.pet_size,
            'description': product.description,
            'count_rate': product.count_rate,
            'avg_rating': product.avg_rating,
            'seller_id': product.seller_id
        }
        list_products_category.append(products)
    return jsonify(list_products_category)


@app.route("/products", methods = ['post', 'get'])
def get_products():
    data = Product.query.all()
    list_products = []
    for product in data:
        products = {
            'id':product.id,
            'name': product.name,
            'price': product.price,
            'category': product.category,
            'imageUrl': product.imageUrl,
            'pet_size': product.pet_size,
            'description': product.description,
            'count_rate': product.count_rate,
            'avg_rating': product.avg_rating,
            'seller_id': product.seller_id
        }
        list_products.append(products)
    return jsonify(list_products)


@app.route('/register', methods=['get', 'post'])
def register():
    form = RegistrationForm.from_json(request.json)

    if form.validate():
        new_user = Users(name=form.name.data,
                        email=form.email.data
                        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status":"ok","user": new_user.name, 'message': 'Thank you, Please Log in'})
    else:
        return jsonify(form.errors)


@app.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm.from_json(request.json)
    print('dataaaataaa', form.email.data)
    log_user = Users.query.filter_by(email=form.email.data).first()
    if log_user is None:
        return ({"status": "fail", "message": "There is no existing email"})
    if not log_user.check_password(form.password.data):
        return ({"status": "fail", "message": "Wrong password"})

    login_user(log_user)
    token_query = Token.query.filter_by(user_id=current_user.id)
    try:
        token = token_query.one()
    except NoResultFound:
        token = Token(user_id=current_user.id, uuid=str(uuid.uuid4().hex))
        db.session.add(token)
        db.session.commit()
    return jsonify({"status": "ok", "user": current_user.name, "token": token.uuid})


@app.route('/create_product', methods = ['POST'])
@login_required
def create_post():
    data = request.get_json()
    total = Product.query.all()
    if data is None:
        data = {}
    if request.method == "POST":
        product = Product(name = data.get('name'),
                price = data.get('price'),
                category = data.get('category'),
                imageUrl = data.get('imageUrl'),
                pet_size = data.get('pet_size'),
                description = data.get('description'),
                seller_id = current_user.id)
        db.session.add(product)
        db.session.commit()
        return jsonify({
                    "success": True,
                    "total_product": len(total)
        })


@app.route("/profile", methods = ['post', 'get'])
@login_required
def get_profile():
    user = Users.query.filter_by(id=current_user.id).first()
    data = {
        'name':user.name,
        'address':user.address,
        'cell_phone':user.cell_phone,
        'email':user.email,
        'date_of_birth':user.date_of_birth,
        'avatar_url':user.avatar_url
    }
    return jsonify(data)


@app.route('/editprofile', methods=['get','post'])
@login_required
def editprofile () :
    data = request.get_json()
    user = Users.query.filter_by(id=current_user.id).first()
    user.name = data['name']
    user.date_of_birth = data['date_of_birth']
    user.address = data['address']
    user.cell_phone = data['cell_phone']
    user.avatar_url = data['avatar_url']
    db.session.commit()
    return  jsonify({"status":"ok"})