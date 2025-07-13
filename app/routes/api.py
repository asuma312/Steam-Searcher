from flask import *
from app.db.setup import get_db
from app.services.searcher import do_query_search
from flask import Response

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify(
            {
                'error': 'Query parameter is required.'
            }
        ), 400
    df = do_query_search(query)
    return Response(df.to_json(orient="records"), mimetype='application/json')
