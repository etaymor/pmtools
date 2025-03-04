from flask import Blueprint, request, jsonify
from app.utils.logging_config import logger
from app.services.openai_service import openai_service

user_story_bp = Blueprint('user_story', __name__)

def format_output(story_content: str, output_format: str = 'plain') -> str:
    """Format the story content based on the specified output format."""
    # Split content into user story and acceptance criteria
    content_parts = story_content.strip().split('\n')
    user_story = ""
    acceptance_criteria = []
    
    # Process the content
    for line in content_parts:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith('as a '):
            user_story = line
        elif not line.startswith(('###', '##', '#', 'Acceptance Criteria:', 'User Story:')):
            acceptance_criteria.append(line)
    
    if output_format.lower() == 'jira':
        formatted = "{panel:title=User Story}\n"
        formatted += "{color:#172B4D}" + user_story + "{color}\n\n"
        formatted += "h3.Acceptance Criteria\n"
        for criterion in acceptance_criteria:
            formatted += "* " + criterion + "\n"
        formatted += "{panel}"
        return formatted
        
    elif output_format.lower() == 'azure':
        formatted = "# User Story\n"
        formatted += "> " + user_story + "\n\n"
        formatted += "## Acceptance Criteria\n"
        for criterion in acceptance_criteria:
            formatted += "- " + criterion + "\n"
        return formatted
        
    else:  # plain format
        formatted = "### User Story\n"
        formatted += user_story + "\n\n"
        formatted += "### Acceptance Criteria\n"
        for criterion in acceptance_criteria:
            formatted += "- " + criterion + "\n"
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
        prompt = f"""Write a user story and acceptance criteria based on the following input. Do not include any headers or section titles in your response.

First line should be the user story in this exact format:
As a [type of user], I want [goal] so that [benefit].

Then skip a line and list 3-5 specific, testable acceptance criteria. Each criterion should be on its own line.

**INPUT DETAILS**:
- **User Type**: {user_type}
- **Desired Functionality**: {functionality}
- **Business Value**: {business_value if business_value else "Please generate an appropriate business value"}"""

        system_prompt = "You are a product management expert specialized in writing clear, actionable user stories with acceptance criteria. Write only the content without any headers or formatting."
        
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