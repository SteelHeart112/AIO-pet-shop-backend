from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Users (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False)
    password = db.Column(db.String(255), unique=False)
    address = db.Column(db.String, nullable=False, default="god know your address")
    cell_phone = db.Column(db.Integer, nullable=False, default=1234567890)
    email = db.Column(db.String(255), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date)
    avatar_url = db.Column(db.String, nullable=False, default="https://cdn4.iconfinder.com/data/icons/animal-2-1/100/animal-15-512.png")

    # rating = db.relationship('Rating_Product', backref=db.backref('from_User_to_Rating_Product'))
    # comment = db.relationship('Comment_Product', backref=db.backref('from_User_to_Comment_Product'))

    def __repr__(self):
        return """title: {}, body: {}""".format(self.username, self.email)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Product (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    pet_size = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    # count_rate = db.Column(db.Integer, nullable=False, default=0)
    # avg_rating = db.Column(db.Float, nullable=False, default=0)

    seller_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    user = db.relationship('Users', backref=db.backref("from_Product_to_Users"))
    # rating = db.relationship('Rating_Product', backref=db.backref("from_Product_to_Rating_Product"))
    # comment = db.relationship('Comment_Product', backref=db.backref("from_Product_to_Comment_Product"))


# many to many
# class Rating_Product (db.Model):
#     product_id = db.Column(db.Integer, db.ForeignKey(Product.id), primary_key=True)
#     rater_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
#     rating = db.Column(db.Integer, nullable=False)


# many to many
# class Comment_Product (db.Model):
#     product_id = db.Column(db.Integer, db.ForeignKey(Product.id), primary_key=True)
#     product_poster_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
#     comment = db.Column(db.String, nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False)
#     updated_at = db.Column(db.DateTime)


# class Order (db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     order_datetime = db.Column(db.DateTime, nullable=False)
#     current_status = db.Column(db.String, nullable=False, default="processing")
#     order_quantity = db.Column(db.Integer, nullable=False, default=1)
#     final_price = db.Column(db.Float, nullable=False)
#     total = db.Column(db.Integer, nullable=False)
#     processed_datetime = db.Column(db.DateTime)
#     note = db.Column(db.String)
#     payment_type = db.Column(db.String, nullable=False, default="payment upon delivery")

#     buyer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
#     user = db.relationship('User', backref=db.backref('from_Order_to_User'))
#     product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
#     product = db.relationship('Product', backref=db.backref('from_Order_to_Product'))


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    user = db.relationship('Users', backref=db.backref("from_OAuth_to_Users"))


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    user = db.relationship('Users', backref=db.backref("from_Token_to_Users"))


# setup login manager
login_manager = LoginManager()
# login_manager.login_view = "facebook.login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.request_loader
def load_user_from_request(request):
    # Login Using our Custom Header
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user

    return None