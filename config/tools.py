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