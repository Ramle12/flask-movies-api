from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

# ---------------------- Initialize Flask ----------------------
app = Flask(__name__)
CORS(app)

# ---------------------- MongoDB Client ----------------------
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ---------------------- Import blueprint factory ----------------------
from routes.movies_routes import create_movies_bp

# ---------------------- Register blueprint ----------------------
movies_bp = create_movies_bp(db)
app.register_blueprint(movies_bp)

# ---------------------- Home ----------------------
@app.route("/")
def home():
    return {"message": "Movies API with Flask & MongoDB Atlas is running!"}

if __name__ == "__main__":
    app.run(debug=True)
