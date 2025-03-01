from flask import Blueprint, render_template, make_response, url_for
from config.tools import get_other_tools, get_tools_by_category
from datetime import datetime
import urllib.parse

main_bp = Blueprint('main', __name__)

def get_all_routes():
    """Get all routes for the sitemap"""
    routes = []
    
    # Add static routes
    static_routes = ['index', 'about', 'value_proposition', 'user_story']
    for route in static_routes:
        url = url_for(f'main_bp.{route}', _external=True)
        routes.append({
            'loc': url,
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'priority': '0.8' if route == 'index' else '0.6'
        })
    
    # Add dynamic tool routes from config
    tools_by_category = get_tools_by_category()
    for category in tools_by_category:
        for tool in tools_by_category[category]:
            url = url_for('main_bp.index', _external=True) + urllib.parse.quote(tool['url'].lstrip('/'))
            routes.append({
                'loc': url,
                'lastmod': datetime.now().strftime('%Y-%m-%d'),
                'priority': '0.7'
            })
    
    return routes

@main_bp.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml"""
    routes = get_all_routes()
    
    xml_content = render_template('sitemap.xml', routes=routes)
    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    
    return response

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

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