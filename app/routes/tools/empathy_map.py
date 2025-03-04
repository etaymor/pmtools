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
        system_prompt = "You are a seasoned UX research expert with a deep understanding of how to create insightful empathy maps that inform product teams and drive user-centered design."
        
        user_prompt = f"""Create a comprehensive empathy map for the following user.

        INSTRUCTIONS:
1. **SAYS** – Provide 4–6 realistic statements or questions the user might openly express.
2. **THINKS** – Provide 4–6 internal thoughts, motivations, or concerns the user keeps to themselves.
3. **DOES** – Provide 4–6 observable actions or behaviors the user exhibits in this scenario.
4. **FEELS** – Provide 4–6 emotions or emotional states the user experiences related to this scenario.
5. **PAIN POINTS** – Provide 4–6 challenges, frustrations, or obstacles the user faces.
6. **GAINS** – Provide 4–6 benefits, positive outcomes, or success metrics from the user’s perspective.

USER DETAILS:
        User Persona: {user_persona}
        Context/Scenario: {context if context else 'General usage of the product'}
        User Goals: {goals if goals else 'Please infer appropriate goals based on the persona'}
        
       REQUIREMENTS:
- Make each section specific, realistic, and actionable.
- Reflect genuine user behaviors, statements, and emotions.
- Avoid repeating the same idea in multiple sections.

Please format your response as a structured empathy map, addressing each section in order.
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