from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

interview_script_bp = Blueprint('interview_script', __name__)

@interview_script_bp.route('/interview-script')
def interview_script():
    """Render the interview script generator's main page."""
    return render_template('interview_script.html', get_tools_by_category=get_tools_by_category)

@interview_script_bp.route('/api/generate-interview-script', methods=['POST', 'OPTIONS'])
def generate_interview_script():
    """Handle interview script generation requests."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        product_name = data.get('productName')
        target_audience = data.get('targetAudience')
        research_goals = data.get('researchGoals')
        script_length = data.get('scriptLength', 'medium')
        script_format = data.get('scriptFormat', 'standard')
        
        if not all([product_name, target_audience, research_goals]):
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Product name, target audience, and research goals are required"}), 400
        
        # Construct the prompt
        system_prompt = "You are a user research expert specialized in creating effective interview scripts for product validation and user research."
        
        user_prompt = f"""Create a user interview script for:
        Product Name: {product_name}
        Target Audience: {target_audience}
        Research Goals: {research_goals}
        Script Length: {script_length}
        
        The script should include:
        1. A brief introduction explaining the purpose of the interview
        2. Warm-up questions to make the participant comfortable
        3. Main questions focused on the research goals
        4. Follow-up probing questions to dig deeper
        5. Closing questions and thank you
        
        Format the script with clear sections, numbered questions, and interviewer instructions in [brackets].
        
        For a {script_length} script, include an appropriate number of questions.
        """
        
        if script_format == 'behavioral':
            user_prompt += "\nFocus on behavioral questions that explore past experiences rather than hypothetical situations."
        elif script_format == 'comparative':
            user_prompt += "\nInclude questions that compare the product with alternatives or competitors."
        elif script_format == 'usability':
            user_prompt += "\nFocus on usability aspects and include task-based questions."
        
        script_content, success = openai_service.generate_completion(system_prompt, user_prompt)
        
        if success:
            result = {
                "success": True,
                "interview_script": script_content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": script_content  # Error message is returned when success is False
            }), 500
            
    except Exception as e:
        logger.exception('Error in generate_interview_script: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 