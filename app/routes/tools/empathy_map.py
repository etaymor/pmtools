from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

empathy_map_bp = Blueprint('empathy_map', __name__)

@empathy_map_bp.route('/empathy-map')
def empathy_map():
    """Render the empathy map tool's main page."""
    return render_template('empathy_map.html', get_tools_by_category=get_tools_by_category)

@empathy_map_bp.route('/api/generate-empathy-map', methods=['POST', 'OPTIONS'])
def generate_empathy_map():
    """Handle empathy map generation requests."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        user_persona = data.get('userPersona')
        context = data.get('context')
        goals = data.get('goals')
        
        if not user_persona:
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "User persona is required"}), 400
        
        # Construct the prompt
        system_prompt = "You are a UX research expert specialized in creating detailed empathy maps to help teams understand their users better."
        
        user_prompt = f"""Create a comprehensive empathy map for the following user:
        
        User Persona: {user_persona}
        Context/Scenario: {context if context else 'General usage of the product'}
        User Goals: {goals if goals else 'Please infer appropriate goals based on the persona'}
        
        Format your response as a structured empathy map with these sections:
        1. SAYS - What the user might say out loud in this scenario
        2. THINKS - What the user might be thinking but not saying
        3. DOES - Actions and behaviors the user exhibits
        4. FEELS - Emotions the user might be experiencing
        5. PAIN POINTS - Frustrations, obstacles, or challenges
        6. GAINS - Benefits, wants, needs, and measures of success
        
        For each section, provide 4-6 specific, realistic points that reflect the user's perspective.
        Make the empathy map detailed, insightful, and actionable for product teams.
        """
        
        content, success = openai_service.generate_completion(system_prompt, user_prompt)
        
        if success:
            result = {
                "success": True,
                "empathy_map": content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": content  # Error message is returned when success is False
            }), 500
            
    except Exception as e:
        logger.exception('Error in generate_empathy_map: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 