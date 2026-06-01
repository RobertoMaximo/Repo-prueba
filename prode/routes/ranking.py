from flask import Blueprint, jsonify
from db import get_connection

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/', methods=['GET'])
def obtener_ranking():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        return jsonify(ranking), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
