from flask import Blueprint, jsonify
from .services import get_vegetables

api = Blueprint("api", __name__)

@api.route("/vegetables", methods=["GET"])
def vegetables():
    data = get_vegetables()

    return jsonify({
        "count": len(data),
        "data": data
    }), 200