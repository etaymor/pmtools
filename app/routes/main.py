from flask import Blueprint, render_template
from config.tools import get_other_tools, get_tools_by_category

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/value-proposition')
def value_proposition():
    return render_template('value_proposition.html')

@main_bp.route('/user-story')
def user_story():
    return render_template('user_story.html')

# Make tools available to all templates
@main_bp.context_processor
def inject_tools():
    def get_tools_by_category_wrapper(current_tool=None):
        return get_tools_by_category(current_tool)
        
    return {
        'get_other_tools': get_other_tools,
        'get_tools_by_category': get_tools_by_category_wrapper
    } 