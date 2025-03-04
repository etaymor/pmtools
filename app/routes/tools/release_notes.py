from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category

release_notes_bp = Blueprint('release_notes', __name__)

@release_notes_bp.route('/release-notes')
def release_notes():
    """Render the release notes generator page."""
    return render_template('release_notes.html', get_tools_by_category=get_tools_by_category)

@release_notes_bp.route('/api/generate-release-notes', methods=['POST', 'OPTIONS'])
def generate_release_notes():
    """Handle release notes generation requests."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        changes_list = data.get('changesList')
        style = data.get('style', 'professional')
        version_number = data.get('versionNumber', '')
        release_date = data.get('releaseDate', '')
        
        if not changes_list:
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "List of changes is required"}), 400
        
        # Construct the system prompt based on the selected style
        system_prompts = {
            'professional': "You are a technical writer specializing in clear, concise, and professional release notes. Your writing is formal, precise, and focuses on communicating value to stakeholders. Format your response using proper Markdown syntax.",
            'casual': "You are a friendly product manager writing release notes in a conversational, approachable tone. Your writing is clear but casual, as if explaining changes to a colleague over coffee. Format your response using proper Markdown syntax.",
            'spicy': "You are a witty, slightly sarcastic product manager writing release notes with personality and flair. Your writing is engaging, memorable, and includes tasteful humor without being unprofessional. Format your response using proper Markdown syntax.",
            'enthusiastic': "You are an extremely enthusiastic product manager who LOVES new features! Your writing is energetic, uses plenty of emojis, and conveys genuine excitement about even the smallest improvements. Format your response using proper Markdown syntax."
        }
        
        system_prompt = system_prompts.get(style, system_prompts['professional'])
        
        # Construct the user prompt
        version_info = f"Version: {version_number}\n" if version_number else ""
        date_info = f"Release Date: {release_date}\n" if release_date else ""
        
        user_prompt = f"""Your mission is to transform the following list of changes into well-structured release notes:

INSTRUCTIONS:
1. **Headline/Title** - Create a catchy title for this release{'' if version_number else ' (include the version number if you can infer it from the changes)'}.
2. **Introduction** - Provide a brief summary of the key themes or goals for this release.
3. **Organized Sections**  - Break down the changes into logical sections (e.g., Features, Improvements, Bug Fixes).- Use bullet points to list items clearly.
4. **Conclusion**  - Thank users or highlight upcoming features/next steps.

IMPORTANT DETAILS:
- **Emphasize Value**: Explain how each change benefits or impacts the user.
- **Tone**: Keep it {style}.
- **Version & Date**: Include the version number and release date in the header if provided.
- **Markdown Formatting**: 
  - Use proper headers (`#` for title, `##` for sections).
  - Use bullet points for lists.
  - Use emphasis (italics or bold) where relevant.

OUTPUT REQUIREMENTS:
- Group similar items together.
- Maintain consistent formatting and tense.
- Keep the release notes concise yet informative.

Now, craft the release notes following these guidelines.
{changes_list}

{version_info}{date_info}

"""

        notes_content, success = openai_service.generate_completion(system_prompt, user_prompt)
        
        if success:
            result = {
                "success": True,
                "release_notes": notes_content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": notes_content  # Error message is returned when success is False
            }), 500
            
    except Exception as e:
        logger.exception('Error in generate_release_notes: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500 