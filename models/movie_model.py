def serialize_movie(movie):
    return {
        "id": str(movie.get("_id")),  # MongoDB ObjectId
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "original_language": movie.get("original_language"),
        "popularity": movie.get("popularity"),
        "vote_count": movie.get("vote_count"),
        "vote_average": movie.get("vote_average"),
        "overview": movie.get("overview")
    }
