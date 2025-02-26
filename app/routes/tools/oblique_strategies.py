from flask import Blueprint, jsonify, render_template, request
from app.utils.logging_config import logger
from config.tools import get_tools_by_category
from app.data.oblique_strategies import OBLIQUE_STRATEGIES
import random

oblique_strategies_bp = Blueprint('oblique_strategies', __name__)

@oblique_strategies_bp.route('/oblique-strategies')
def oblique_strategies():
    """Render the Oblique Strategies tool's main page."""
    return render_template('oblique_strategies.html', get_tools_by_category=get_tools_by_category)

@oblique_strategies_bp.route('/api/oblique-strategies/random', methods=['GET', 'OPTIONS'])
def get_random_strategy():
    """Return a random Oblique Strategy."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        strategy = random.choice(OBLIQUE_STRATEGIES)
        return jsonify({
            "success": True,
            "strategy": strategy
        })
    except Exception as e:
        logger.exception('Error in get_random_strategy: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 