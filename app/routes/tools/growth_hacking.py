from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

growth_hacking_bp = Blueprint('growth_hacking', __name__)

# Main route to serve the HTML page
@growth_hacking_bp.route('/growth-hacking')  # Must match the 'url' in tools.py
def growth_hacking():
    """Render the Growth Hacking Idea Generator page."""
    return render_template('growth_hacking.html', get_tools_by_category=get_tools_by_category)

# API endpoint for tool functionality
@growth_hacking_bp.route('/api/generate-growth-hacking', methods=['POST', 'OPTIONS'])
def generate_growth_hacking():
    """Handle growth hacking idea generation requests."""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Extract fields from the request
        product_description = data.get('productDescription')
        target_audience = data.get('targetAudience')
        growth_stage = data.get('growthStage')
        
        # Validate required fields
        if not all([product_description, target_audience, growth_stage]):
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Required fields missing"}), 400

        # Construct the prompt for OpenAI
        system_prompt = """You are an experienced growth hacker who specializes in finding creative, scrappy, and budget-friendly ways to grow products and businesses. 
You focus on data-driven strategies that can be implemented quickly with minimal resources."""

        user_prompt = f"""Generate 5 creative, scrappy, and budget-friendly growth hacking ideas for the following product:

Product Description: {product_description}
Target Audience: {target_audience}
Growth Stage Focus: {growth_stage}

For each idea:
1. Give it a catchy, descriptive name
2. Explain how to implement it in 2-3 sentences
3. Explain why it would be effective for this specific product and audience
4. Include a rough estimate of implementation time (hours/days)
5. Mention any free or low-cost tools that could help

IMPORTANT CONSTRAINTS:
- All ideas must be implementable with minimal budget
- Focus on quick wins that can show results within 1-4 weeks
- Ideas should be specific to the product and audience, not generic
- Prioritize ideas that are data-driven and measurable
- Include ideas that address the selected growth stages: {growth_stage}
- Be creative but practical - these should be actionable ideas, not theoretical concepts

Format each idea with clear headings and bullet points for readability."""

        content, success = openai_service.generate_completion(system_prompt, user_prompt)

        if success:
            result = {
                "success": True,
                "growth_hacking_ideas": content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": content
            }), 500

    except Exception as e:
        logger.exception('Error in generate_growth_hacking: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 