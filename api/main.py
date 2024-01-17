from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:yc0FVPEaOli6@ep-weathered-smoke-19253145.us-east-1.postgres.vercel-storage.com:5432/verceldb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)
origins = ['*']
CORS(
    app,
    origins=origins,
    methods=["GET", "POST", "OPTIONS", "DELETE"],
)


from category_routes import category_bp
from user_routes import auth_bp
from booking_routes import booking_bp
app.register_blueprint(category_bp, url_prefix='/categories')
app.register_blueprint(auth_bp, url_prefix='/users')
app.register_blueprint(booking_bp, url_prefix='/bookings')

@app.route('/health', methods=['GET'])
def health_check():
    return 'Health check passed'
