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
        
        user_prompt = f"""Your mission is to create a comprehensive stakeholder interview guide for the stakeholder listed at the end. 

Your guide should include:

1. **Introduction**  - Provide a brief explanation of the interview's purpose and how it ties back to the product goals.
2. **Background Questions**  - Aim to understand the stakeholder’s role, responsibilities, and overall perspective.
3. **Product-Specific Questions**  - Address the key objectives. - Include questions about cost, budget constraints, or pricing concerns—especially opportunities to decrease price or lower costs without compromising value.
4. **North Star Goal Questions** - Explore the stakeholder’s vision, success metrics, and long-term objectives.
5. **Follow-Up Probing Questions** - Encourage deeper discussion on any points raised, including clarifying potential cost-reduction strategies or trade-offs.
6. **Closing Questions & Next Steps** - Summarize findings, confirm alignment, and outline any immediate follow-up actions.

**FORMAT REQUIREMENTS**:
- Use clear section headers in Markdown format (e.g., `## Section Title`).
- Number your questions.
- Place interviewer instructions or prompts in `[brackets]`.
- Provide an appropriate number of questions for a {interview_duration} interview.

**STAKEHOLDER INFORMATION**:
- **Stakeholder Role**: {stakeholder_role}
- **Interview Objectives**: {interview_objectives}
- **Interview Duration**: {interview_duration}
- **Specific Focus Areas**: {focus_areas}
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