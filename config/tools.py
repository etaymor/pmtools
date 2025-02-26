"""
Configuration file containing all product management tool definitions.
Each tool should have:
- id: Unique identifier used for routing and comparison
- name: Display name shown in UI
- description: Short description of what the tool does
- url: URL path to access the tool
- category: Category the tool belongs to (e.g., 'Generators', 'Analysis', etc.)
"""

TOOLS = [
    {
        'id': 'value_proposition',
        'name': 'Value Proposition Generator',
        'description': 'Create compelling value propositions that resonate with your target audience',
        'url': '/value-proposition',
        'category': 'Generators'
    },
    {
        'id': 'user_story',
        'name': 'User Story Generator',
        'description': 'Generate well-structured user stories for your product backlog',
        'url': '/user-story',
        'category': 'Generators'
    },
    {
        'id': 'feature_prioritization',
        'name': 'Feature Prioritization Matrix',
        'description': 'Prioritize features based on impact and effort',
        'url': '/feature-prioritization',
        'category': 'Analysis'
    },
    {
        'id': 'pain_points',
        'name': 'Customer Pain Point Identifier',
        'description': 'Identify key pain points for your target customer segment',
        'url': '/pain-points',
        'category': 'Analysis'
    },
    {
        'id': 'oblique_strategies',
        'name': 'Oblique Strategies',
        'description': 'Get inspired with Brian Eno\'s Oblique Strategies - random prompts for breaking creative blocks',
        'url': '/oblique-strategies',
        'category': 'Random Prompts'
    },
    {
        'id': 'ai_ideation',
        'name': 'AI Ideation Prompts',
        'description': 'Generate innovative AI-driven solutions with thought-provoking prompts for team brainstorming',
        'url': '/ai-ideation',
        'category': 'Random Prompts'
    },
    {
        'id': 'market_gap',
        'name': 'Market Gap Identifier',
        'description': 'Identify potential market gaps and opportunities based on industry analysis',
        'url': '/market-gap',
        'category': 'Analysis'
    },
    {
        'id': 'interview_script',
        'name': 'User Interview Script Generator',
        'description': 'Create structured interview scripts for user research and product validation',
        'url': '/interview-script',
        'category': 'Research'
    },
    {
        'id': 'release_notes',
        'name': 'Release Notes Generator',
        'description': 'Transform your list of fixes and features into polished release notes with various style options',
        'url': '/release-notes',
        'category': 'Generators'
    },
    {
        'id': 'growth_hacking',
        'name': 'Growth Hacking Idea Generator',
        'description': 'Generate scrappy, budget-friendly growth hacking ideas tailored to your product and target audience',
        'url': '/growth-hacking',
        'category': 'Generators'
    },
    {
        'id': 'empathy_map',
        'name': 'User Empathy Map Generator',
        'description': 'Create detailed empathy maps to better understand your users\' needs, thoughts, feelings, and behaviors',
        'url': '/empathy-map',
        'category': 'Research'
    },
    {
        'id': 'stakeholder_interview',
        'name': 'Stakeholder Interview Guide Generator',
        'description': 'Create comprehensive interview guides for stakeholder interviews with focus on product discovery',
        'url': '/stakeholder-interview',
        'category': 'Research'
    },
    {
        'id': 'brainstorming_timer',
        'name': 'Brainstorming Session Timer',
        'description': 'Set a countdown timer for your brainstorming sessions with pause and restart functionality',
        'url': '/brainstorming-timer',
        'category': 'Productivity'
    }
]

def get_tools():
    """Return the list of all tools."""
    return TOOLS

def get_other_tools(current_tool_id):
    """Return all tools except the current one."""
    return [tool for tool in TOOLS if tool['id'] != current_tool_id]

def get_categories():
    """Return a sorted list of unique categories."""
    return sorted(set(tool['category'] for tool in TOOLS))

def get_tools_by_category(current_tool_id=None):
    """Return tools grouped by category, excluding the current tool."""
    categories = {}
    tools = get_other_tools(current_tool_id) if current_tool_id else TOOLS
    
    for tool in tools:
        category = tool['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(tool)
    
    return dict(sorted(categories.items())) 