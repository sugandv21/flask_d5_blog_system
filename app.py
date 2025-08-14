from flask import Flask
from extensions import db
from routes import main

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret123"

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(main)

# Create tables if not exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
