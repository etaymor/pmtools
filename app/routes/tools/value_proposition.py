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
        
        prompt = f"""INSTRUCTIONS:
1. Craft a **single-sentence value proposition** that clearly communicates:
   - The product’s name
   - The target customer segment
   - The primary benefits
2. **Avoid jargon** and keep the language straightforward and compelling.
3. **No additional explanation**—only provide the single-sentence value proposition.

PRODUCT DETAILS:
- Product Name: {product_name}
- Target Customer Segment: {target_audience}
- Main Benefits: {main_value}
    """

        system_prompt = "You are an experienced marketing strategist and copywriter specializing in concise, impactful value propositions."
        
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