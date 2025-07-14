from flask import *
from app.db.setup import get_db
from app.services.searcher import do_query_search, do_genre_search, do_category_search
from flask import Response

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/get_categories", methods=['GET'])
def get_categories():
    return jsonify(do_category_search()), 200

@api_bp.route("/get_genres", methods=['GET'])
def get_genres():
    return jsonify(do_genre_search()), 200

@api_bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    print(data)
    query = data.get('query')
    category = data.get('category', None)
    if not category or category == []:
        category = do_category_search()
    genre = data.get('genre', None)
    if not genre or genre == []:
        genre = do_genre_search()
    price_start = data.get('price_start', 0.0)
    price_end = data.get('price_end', 1000000.0)
    if not query:
        return jsonify(
            {
                'error': 'Query parameter is required.'
            }
        ), 400
    df = do_query_search(query, category=category, genre=genre, price_start=price_start, price_end=price_end)
    return Response(df.to_json(orient="records"), mimetype='application/json')
