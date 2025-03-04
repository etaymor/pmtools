from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

market_gap_bp = Blueprint('market_gap', __name__)

@market_gap_bp.route('/market-gap')
def market_gap():
    """Render the Market Gap Identifier tool's main page."""
    return render_template('market_gap.html', get_tools_by_category=get_tools_by_category)

@market_gap_bp.route('/api/market-gap', methods=['POST', 'OPTIONS'])
def market_gap_handler():
    """Handle Market Gap Identifier tool requests."""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Extract fields from request
        industry = data.get('industry')
        customer_type = data.get('customerType')
        competitor = data.get('competitor')
        pain_point = data.get('painPoint')

        if not industry or not customer_type:
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Industry and Customer Type are required"}), 400

        # Construct the prompt for OpenAI
        system_prompt = """You are a market research expert identifying gaps in different industries. 
Focus on actionable insights and specific niches that could be exploited."""

        user_prompt = f"""Your mission is to analyze the market and suggest a unique, underserved opportunity. 

        INSTRUCTIONS:
1. **Identified Market Gap** - Provide a concise statement of the gap.   
2. **Why This Gap Exists** - Explain the root causes behind this market gap.
3. **Potential Solutions or Product Ideas** - Offer 2–3 innovative solutions that address the gap.
4. **Example Differentiators** - Describe how a business can stand out from competitors.

Here is the provided user input:
Industry/Market: {industry}
Target Customer: {customer_type}
{"Main Competitor: " + competitor if competitor else ""}
{"Known Pain Point: " + pain_point if pain_point else ""}

Please present your analysis in this four-part structure, keeping each section focused and actionable.
"""

        content, success = openai_service.generate_completion(system_prompt, user_prompt)

        if success:
            result = {
                "success": True,
                "analysis": content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": content
            }), 500

    except Exception as e:
        logger.exception('Error in market_gap_handler: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 