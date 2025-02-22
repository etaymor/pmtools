from flask import Blueprint, request, jsonify
from app.utils.logging_config import logger
from app.services.openai_service import openai_service

user_story_bp = Blueprint('user_story', __name__)

def format_output(story_content: str, output_format: str = 'plain') -> str:
    """Format the story content based on the specified output format."""
    lines = story_content.strip().split('\n')
    
    if output_format.lower() == 'jira':
        formatted = "{panel:title=User Story}\n"
        formatted += "{color:#172B4D}" + lines[0] + "{color}\n\n"
        formatted += "h3.Acceptance Criteria\n"
        for line in lines[1:]:
            if line.strip():
                formatted += "* " + line.strip() + "\n"
        formatted += "{panel}"
        return formatted
        
    elif output_format.lower() == 'azure':
        formatted = "# User Story\n"
        formatted += "> " + lines[0] + "\n\n"
        formatted += "## Acceptance Criteria\n"
        for line in lines[1:]:
            if line.strip():
                formatted += "- " + line.strip() + "\n"
        return formatted
        
    else:  # plain format
        formatted = "### User Story\n"
        formatted += lines[0] + "\n\n"
        formatted += "### Acceptance Criteria\n"
        for line in lines[1:]:
            if line.strip():
                formatted += "- " + line.strip() + "\n"
        return formatted

@user_story_bp.route('/api/generate-user-story', methods=['POST', 'OPTIONS'])
def generate_user_story():
    """Handle user story generation requests."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        user_type = data.get('userType')
        functionality = data.get('functionality')
        business_value = data.get('businessValue')
        output_format = data.get('outputFormat', 'plain')
        
        if not all([user_type, functionality]):
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "User type and functionality are required"}), 400
        
        # Construct the prompt
        prompt = f"""Create a user story with acceptance criteria for:
        User Type: {user_type}
        Desired Functionality: {functionality}
        Business Value: {business_value if business_value else 'Please generate an appropriate business value'}
        
        Format your response exactly as follows:
        1. First line: Write the user story in 'As a [type of user], I want [goal] so that [benefit]' format
        2. Following lines: List 3-5 specific, testable acceptance criteria
        
        Keep the response concise and focused."""

        system_prompt = "You are a product management expert specialized in writing clear, actionable user stories with acceptance criteria."
        
        story_content, success = openai_service.generate_completion(system_prompt, prompt)
        
        if success:
            formatted_content = format_output(story_content, output_format)
            result = {
                "success": True,
                "user_story": formatted_content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": story_content  # Error message is returned when success is False
            }), 500
            
    except Exception as e:
        logger.exception('Error in generate_user_story: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 