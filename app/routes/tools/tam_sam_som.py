from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

tam_sam_som_bp = Blueprint('tam_sam_som', __name__)

@tam_sam_som_bp.route('/tam-sam-som')
def tam_sam_som():
    """Render the TAM/SAM/SOM Estimator tool's main page."""
    return render_template('tam_sam_som.html', get_tools_by_category=get_tools_by_category)

@tam_sam_som_bp.route('/api/tam-sam-som', methods=['POST', 'OPTIONS'])
def tam_sam_som_handler():
    """Handle TAM/SAM/SOM Estimator tool requests."""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Extract fields from request
        industry = data.get('industry')
        product_description = data.get('productDescription')
        target_customers = data.get('targetCustomers')
        additional_info = data.get('additionalInfo', '')
        approach = data.get('approach', 'bottom-up')  # Default to bottom-up approach

        if not industry or not product_description or not target_customers:
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Industry, Product Description, and Target Customers are required"}), 400

        # Construct the prompt for OpenAI
        system_prompt = """You are a market research and business strategy expert specializing in market sizing and opportunity assessment. 
Your task is to provide a detailed TAM (Total Addressable Market), SAM (Serviceable Addressable Market), and SOM (Serviceable Obtainable Market) analysis based on the information provided.
Use a conservative bottom-up approach that starts with specific customer segments and builds up to the total market size."""

        user_prompt = f"""Please provide a comprehensive TAM/SAM/SOM analysis for the following:

Industry/Market: {industry}
Product/Service Description: {product_description}
Target Customer Segments: {target_customers}
{"Additional Information: " + additional_info if additional_info else ""}
Calculation Approach: {approach} (conservative estimates)

Your analysis should include:

1. **TAM (Total Addressable Market)**:
   - Estimated total market size (in dollars and potential customers)
   - Key assumptions made in the calculation
   - Sources or methodologies used for estimation

2. **SAM (Serviceable Addressable Market)**:
   - Portion of TAM that can be served by the product/service
   - Segmentation criteria used
   - Percentage of TAM and dollar value

3. **SOM (Serviceable Obtainable Market)**:
   - Realistic market share that can be captured
   - Factors influencing market capture (competition, go-to-market strategy, etc.)
   - Percentage of SAM and dollar value
   - Timeline considerations for achieving the estimated SOM

4. **Visualization Description**:
   - A text description of how a funnel visualization would look with the TAM at the top, SAM in the middle, and SOM at the bottom, with approximate percentages and dollar values

5. **Detailed Breakdown**:
   - Include a section with detailed calculations and assumptions that could be expanded if the user wants to see more details
   - Keep this section clearly separated so it can be shown/hidden in the UI

6. **Recommendations**:
   - Strategic implications of this market sizing
   - Suggested next steps for validation or refinement

Please provide realistic ranges rather than single figures, and be conservative in your estimates. Explain your reasoning throughout the analysis."""

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
        logger.exception('Error in tam_sam_som_handler: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 