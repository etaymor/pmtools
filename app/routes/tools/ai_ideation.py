from flask import Blueprint, jsonify, render_template, request
from app.utils.logging_config import logger
from config.tools import get_tools_by_category
from app.data.ai_ideation_prompts import AI_IDEATION_PROMPTS
import random

ai_ideation_bp = Blueprint('ai_ideation', __name__)

@ai_ideation_bp.route('/ai-ideation')
def ai_ideation():
    """Render the AI Ideation Prompts tool's main page."""
    return render_template('ai_ideation.html', get_tools_by_category=get_tools_by_category)

@ai_ideation_bp.route('/api/ai-ideation/random', methods=['GET', 'OPTIONS'])
def get_random_prompt():
    """Return a random AI Ideation prompt."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        prompt = random.choice(AI_IDEATION_PROMPTS)
        return jsonify({
            "success": True,
            "prompt": prompt
        })
    except Exception as e:
        logger.exception('Error in get_random_prompt: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 