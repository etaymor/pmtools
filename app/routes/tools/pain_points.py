from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

pain_points_bp = Blueprint('pain_points', __name__)

@pain_points_bp.route('/pain-points')
def pain_points():
    """Render the pain points tool page."""
    return render_template('pain_points.html', get_tools_by_category=get_tools_by_category)

@pain_points_bp.route('/api/pain-points', methods=['POST', 'OPTIONS'])
def generate_pain_points():
    """Generate customer pain points based on target segment and product information."""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Extract required fields
        target_segment = data.get('targetSegment')
        product_info = data.get('productInfo')

        if not all([target_segment, product_info]):
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Both target segment and product information are required"}), 400

        # Construct the prompt for OpenAI
        system_prompt = """You are an expert business analyst specializing in identifying customer pain points. 
        Your task is to analyze the given target customer segment and product/space information to identify 
        specific, actionable pain points that these customers experience. Focus on real, practical challenges 
        that affect their daily operations or lives."""

        user_prompt = f"""Please identify 7 specific pain points for the following scenario:

        Target Customer Segment: {target_segment}
        Product/Space Information: {product_info}

        For each pain point, provide a clear, concise description of the challenge or frustration the customer faces.
        Format each pain point as a separate bullet point.
        Focus only on the problems/challenges, without suggesting solutions.
        Be specific and actionable in describing each pain point."""

        content, success = openai_service.generate_completion(system_prompt, user_prompt)

        if success:
            result = {
                "success": True,
                "painPoints": content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": content
            }), 500

    except Exception as e:
        logger.exception('Error in pain_points: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 