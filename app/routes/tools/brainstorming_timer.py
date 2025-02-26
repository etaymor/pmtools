from flask import Blueprint, render_template
from config.tools import get_tools_by_category

brainstorming_timer_bp = Blueprint('brainstorming_timer', __name__)

@brainstorming_timer_bp.route('/brainstorming-timer')
def brainstorming_timer():
    """Render the Brainstorming Timer tool's main page."""
    return render_template('brainstorming_timer.html', get_tools_by_category=get_tools_by_category) 