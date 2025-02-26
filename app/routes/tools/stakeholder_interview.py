from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

stakeholder_interview_bp = Blueprint('stakeholder_interview', __name__)

@stakeholder_interview_bp.route('/stakeholder-interview')
def stakeholder_interview():
    """Render the stakeholder interview guide generator's main page."""
    return render_template('stakeholder_interview.html', get_tools_by_category=get_tools_by_category)

@stakeholder_interview_bp.route('/api/generate-stakeholder-interview', methods=['POST', 'OPTIONS'])
def generate_stakeholder_interview():
    """Handle stakeholder interview guide generation requests."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        stakeholder_role = data.get('stakeholderRole')
        interview_objectives = data.get('interviewObjectives')
        interview_duration = data.get('interviewDuration', 'medium')
        focus_areas = data.get('focusAreas', '')
        
        if not all([stakeholder_role, interview_objectives]):
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Stakeholder role and interview objectives are required"}), 400
        
        # Construct the prompt
        system_prompt = "You are a product management expert specialized in creating effective stakeholder interview guides for product discovery."
        
        user_prompt = f"""Create a comprehensive stakeholder interview guide for:
        Stakeholder Role: {stakeholder_role}
        Interview Objectives: {interview_objectives}
        Interview Duration: {interview_duration}
        Specific Focus Areas: {focus_areas}
        
        The interview guide should include:
        1. A brief introduction explaining the purpose of the interview
        2. Background questions to understand the stakeholder's role and perspective
        3. Product-specific questions related to the objectives
        4. North star goal questions to align on vision and direction
        5. Follow-up probing questions to dig deeper
        6. Closing questions and next steps
        
        Format the guide with clear sections using markdown formatting (## for section headers, * for bullet points, etc.).
        Include numbered questions and interviewer instructions in [brackets].
        
        For a {interview_duration} interview, include an appropriate number of questions.
        """
        
        guide_content, success = openai_service.generate_completion(system_prompt, user_prompt)
        
        if success:
            result = {
                "success": True,
                "interview_guide": guide_content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": guide_content  # Error message is returned when success is False
            }), 500
            
    except Exception as e:
        logger.exception('Error in generate_stakeholder_interview: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 