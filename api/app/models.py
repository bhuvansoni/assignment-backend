from app.main import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    starttime = db.Column(db.TIMESTAMP, nullable=False)
    endtime = db.Column(db.TIMESTAMP, nullable=False)

    created_by_user = db.relationship('User', foreign_keys=[created_by_user_id])
    category = db.relationship('Category', foreign_keys=[category_id])
