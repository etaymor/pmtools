from flask import Flask, request
from flask_cors import CORS
from app.utils.logging_config import logger
from config.settings import CORS_ORIGINS, CORS_METHODS, CORS_HEADERS
import os

def create_app():
    """Application factory function."""
    # Get the directory containing this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": CORS_ORIGINS,
            "methods": CORS_METHODS,
            "allow_headers": CORS_HEADERS
        }
    })
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.tools.value_proposition import value_prop_bp
    from app.routes.tools.user_story import user_story_bp
    from app.routes.tools.pain_points import pain_points_bp
    from app.routes.tools.oblique_strategies import oblique_strategies_bp
    from app.routes.tools.ai_ideation import ai_ideation_bp
    from app.routes.tools.market_gap import market_gap_bp
    from app.routes.tools.interview_script import interview_script_bp
    from app.routes.tools.release_notes import release_notes_bp
    from app.routes.tools.growth_hacking import growth_hacking_bp
    from app.routes.tools.empathy_map import empathy_map_bp
    from app.routes.tools.stakeholder_interview import stakeholder_interview_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(value_prop_bp)
    app.register_blueprint(user_story_bp)
    app.register_blueprint(pain_points_bp)
    app.register_blueprint(oblique_strategies_bp)
    app.register_blueprint(ai_ideation_bp)
    app.register_blueprint(market_gap_bp)
    app.register_blueprint(interview_script_bp)
    app.register_blueprint(release_notes_bp)
    app.register_blueprint(growth_hacking_bp)
    app.register_blueprint(empathy_map_bp)
    app.register_blueprint(stakeholder_interview_bp)
    
    # Debug template loading
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True
    
    @app.before_request
    def log_request_info():
        """Log details about each request."""
        logger.debug('Headers: %s', dict(request.headers))
        logger.debug('Method: %s', request.method)
        logger.debug('URL: %s', request.url)
        if request.is_json:
            logger.debug('Body: %s', request.get_json())

    @app.after_request
    def after_request(response):
        """Log response and add CORS headers explicitly."""
        logger.debug('Response Headers: %s', dict(response.headers))
        logger.debug('Response Body: %s', response.get_data(as_text=True))
        
        # Add CORS headers explicitly
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        return response
    
    return app 