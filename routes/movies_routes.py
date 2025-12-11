from flask import Blueprint, request
from bson.objectid import ObjectId
from models.movie_model import serialize_movie

def create_movies_bp(db):
    movies_bp = Blueprint("movies", __name__, url_prefix="/movies")

    # Get all movies
    @movies_bp.route("/", methods=["GET"])
    def get_movies():
        movies = db.movies.find()
        return [serialize_movie(m) for m in movies]

    # Get a single movie by ObjectId
    @movies_bp.route("/<movie_id>", methods=["GET"])
    def get_movie(movie_id):
        try:
            movie = db.movies.find_one({"_id": ObjectId(movie_id)})
        except Exception:
            return {"error": "Invalid movie ID"}, 400
        if movie:
            return serialize_movie(movie)
        return {"error": "Movie not found"}, 404

    # Add a new movie
    @movies_bp.route("/", methods=["POST"])
    def add_movie():
        data = request.json
        inserted = db.movies.insert_one(data)
        new_movie = db.movies.find_one({"_id": inserted.inserted_id})
        return serialize_movie(new_movie)

    # Update a movie by ObjectId
    @movies_bp.route("/<movie_id>", methods=["PUT"])
    def update_movie(movie_id):
        data = request.json
        try:
            db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": data})
            updated_movie = db.movies.find_one({"_id": ObjectId(movie_id)})
        except Exception:
            return {"error": "Invalid movie ID"}, 400
        if updated_movie:
            return serialize_movie(updated_movie)
        return {"error": "Movie not found"}, 404

    # Delete a movie by ObjectId
    @movies_bp.route("/<movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        try:
            result = db.movies.delete_one({"_id": ObjectId(movie_id)})
        except Exception:
            return {"error": "Invalid movie ID"}, 400
        if result.deleted_count == 0:
            return {"error": "Movie not found"}, 404
        return {"message": "Movie deleted successfully"}

    # Top-rated movies (vote_average)
    @movies_bp.route("/top-rated", methods=["GET"])
    def top_rated():
        movies = db.movies.find().sort("vote_average", -1).limit(10)
        return [serialize_movie(m) for m in movies]

    # Movies by language
    @movies_bp.route("/language/<lang>", methods=["GET"])
    def movies_by_language(lang):
        movies = db.movies.find({"original_language": {"$regex": lang, "$options": "i"}})
        return [serialize_movie(m) for m in movies]

    # Average vote
    @movies_bp.route("/average-vote", methods=["GET"])
    def average_vote():
        pipeline = [{"$group": {"_id": None, "avgVote": {"$avg": "$vote_average"}}}]
        result = list(db.movies.aggregate(pipeline))
        return {"average_vote": result[0]["avgVote"] if result else None}
    
    # Movies by year (release_date)
    @movies_bp.route("/stats/year", methods=["GET"])
    def movies_by_year():
        pipeline = [
            {"$group": {"_id": {"$substr": ["$release_date", 0, 4]}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        result = list(db.movies.aggregate(pipeline))
        return result

    return movies_bp
