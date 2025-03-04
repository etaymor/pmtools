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
        system_prompt = """You are a market research and business strategy expert specializing in market sizing and opportunity assessment."""

        user_prompt = f"""Your mission is to provide a detailed TAM (Total Addressable Market), SAM (Serviceable Addressable Market), 
and SOM (Serviceable Obtainable Market) analysis using a conservative bottom-up approach that starts with 
specific customer segments and builds up to the total market size.

---

**ANALYSIS REQUIREMENTS**:
1. **TAM (Total Addressable Market)**  
   - Estimated total market size (in dollars and potential customers)  
   - Key assumptions made in the calculation  
   - Sources or methodologies used for estimation  

2. **SAM (Serviceable Addressable Market)**  
   - Subset of the TAM that the product/service can serve  
   - Segmentation criteria used  
   - Percentage of TAM and dollar value  

3. **SOM (Serviceable Obtainable Market)**  
   - Realistic share of the SAM the business can capture  
   - Factors influencing market capture (competition, go-to-market strategy, etc.)  
   - Percentage of SAM and dollar value  
   - Timeline considerations for achieving the estimated SOM  

4. **Visualization Description**  
   - Text-based description of a funnel with TAM at the top, SAM in the middle, and SOM at the bottom  
   - Approximate percentages and dollar values for each layer  

5. **Detailed Breakdown**  
   - Calculations and assumptions in a separate section  
   - Clearly separated so it can be shown/hidden in the UI  

6. **Recommendations**  
   - Strategic implications of this market sizing  
   - Suggested next steps for further validation or refinement  

**OUTPUT FORMAT**:
- Provide realistic **ranges** rather than single figures.  
- Maintain **conservative estimates**.  
- Explain your **reasoning** and any assumptions clearly.  
- Use a clear Markdown structure (e.g., headers, bullet points) for readability.
        
        Please provide a comprehensive TAM/SAM/SOM analysis for the following:
**INPUT DETAILS**:
- **Industry/Market**: {industry}
- **Product/Service Description**: {product_description}
- **Target Customer Segments**: {target_customers}
{"- **Additional Information**: " + additional_info if additional_info else ""}
- **Calculation Approach**: {approach} (conservative estimates)
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
        logger.exception('Error in tam_sam_som_handler: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 