from flask import Blueprint, request, jsonify
from app.utils.logging_config import logger
from app.services.openai_service import openai_service

value_prop_bp = Blueprint('value_proposition', __name__)

@value_prop_bp.route('/api/generate-value-prop', methods=['POST', 'OPTIONS'])
def generate_value_prop():
    """Handle value proposition generation requests."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        product_name = data.get('productName')
        target_audience = data.get('targetAudience')
        main_value = data.get('mainValue')
        
        if not all([product_name, target_audience, main_value]):
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        prompt = f"""Create a compelling value proposition for:
        Product: {product_name}
        Target Audience: {target_audience}
        Main Value: {main_value}
        
        Format: Create a concise, powerful value proposition that highlights the unique benefits."""

        system_prompt = "You are a marketing expert specialized in creating compelling value propositions."
        
        value_prop, success = openai_service.generate_completion(system_prompt, prompt)
        
        if success:
            result = {
                "success": True,
                "value_proposition": value_prop
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": value_prop  # Error message is returned when success is False
            }), 500
            
    except Exception as e:
        logger.exception('Error in generate_value_prop: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 