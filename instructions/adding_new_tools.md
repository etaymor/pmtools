# Adding New Tools to PM Tools

This guide explains how to add new tools to the PM Tools application while maintaining consistency with the existing structure and design patterns.

## Directory Structure

```
project_root/
├── app/
│   ├── routes/
│   │   ├── tools/           # Tool-specific route handlers
│   │   │   ├── __init__.py
│   │   │   └── your_tool.py # Add your new route handler here
│   │   └── main.py
│   └── services/            # Shared services (e.g., OpenAI)
├── templates/
│   ├── components/          # Reusable UI components
│   └── your_tool.html      # Add your new tool template here
└── config/
    └── tools.py            # Tool definitions and configurations
```

## Step-by-Step Guide

### 1. Add Tool Configuration

In `config/tools.py`, add your tool definition to the `TOOLS` list:

```python
TOOLS = [
    # ... existing tools ...
    {
        'id': 'your_tool_id',
        'name': 'Your Tool Name',
        'description': 'Brief description of what your tool does',
        'url': '/your-tool-url',
        'category': 'Generators'  # or another appropriate category
    }
]
```

### 2. Create Route Handler

Create a new file in `app/routes/tools/your_tool.py`:

```python
from flask import Blueprint, request, jsonify
from app.utils.logging_config import logger
from app.services.openai_service import openai_service

your_tool_bp = Blueprint('your_tool', __name__)

@your_tool_bp.route('/api/your-tool-endpoint', methods=['POST', 'OPTIONS'])
def your_tool_handler():
    """Handle your tool's requests."""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Extract your tool's specific fields
        field1 = data.get('field1')
        field2 = data.get('field2')

        if not all([field1, field2]):  # Add required field validation
            logger.error('Missing required fields')
            return jsonify({"success": False, "error": "Required fields missing"}), 400

        # Construct the prompt for OpenAI
        prompt = f"""Your prompt template here:
        Field1: {field1}
        Field2: {field2}

        Format your response as needed."""

        system_prompt = "System prompt defining AI's role"

        content, success = openai_service.generate_completion(system_prompt, prompt)

        if success:
            result = {
                "success": True,
                "your_result": content
            }
            logger.debug('Success response: %s', result)
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": content
            }), 500

    except Exception as e:
        logger.exception('Error in your_tool: %s', str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500
```

### 3. Create HTML Template

Create a new file in `templates/your_tool.html`:

```html
{% extends "base.html" %} {% from "components/tool_links.html" import tool_links
with context %} {% block title %}Your Tool Name - Free Product Management Tool{%
endblock %} {% block meta_description %}Description for SEO purposes{% endblock
%} {% block og_title %}Your Tool Name - Free Tool for Teams{% endblock %} {%
block og_description %}{{ self.meta_description() }}{% endblock %} {% block
twitter_title %}{{ self.og_title() }}{% endblock %} {% block twitter_description
%}{{ self.meta_description() }}{% endblock %} {% block content %}
<div class="max-w-4xl mx-auto">
  <!-- Hero Section -->
  <div class="text-center py-4 px-6 mb-8 rounded-2xl">
    <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-4 leading-tight">
      Your Tool Name
    </h1>
    <div class="prose prose-base mx-auto text-gray-600 max-w-2xl">
      <p class="text-base md:text-lg leading-relaxed">
        Your tool's description and value proposition.
      </p>
    </div>
  </div>

  <!-- Main Form Card -->
  <div
    class="bg-white rounded-2xl shadow-xl p-8 mb-12 transform transition-all duration-300 hover:shadow-2xl"
  >
    <form id="yourToolForm" class="space-y-8">
      <!-- Your form fields here -->
      <div class="space-y-6">
        <div class="relative">
          <label
            for="field1"
            class="block text-sm font-semibold text-gray-700 mb-2"
          >
            Field 1
          </label>
          <input
            type="text"
            id="field1"
            name="field1"
            required
            class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 bg-gray-50 hover:bg-white"
            placeholder="Field 1 placeholder"
          />
        </div>
      </div>

      <button
        type="submit"
        class="w-full bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-4 rounded-lg font-semibold text-lg hover:from-green-600 hover:to-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
      >
        Generate Result
      </button>
    </form>

    <!-- Loading Spinner -->
    <div id="loading" class="hidden mt-8 text-center">
      <div
        class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-green-500 border-t-transparent"
      ></div>
      <p class="mt-2 text-gray-600">Processing...</p>
    </div>

    <!-- Result Section -->
    <div id="result" class="hidden mt-8 transform transition-all duration-300">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Your Result:</h2>
      <div
        id="resultContent"
        class="p-6 bg-gradient-to-br from-green-50 to-blue-50 rounded-lg text-gray-700 text-lg leading-relaxed border border-green-100 shadow-sm"
      ></div>
      <button
        onclick="copyToClipboard()"
        class="mt-4 inline-flex items-center justify-center rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
      >
        Copy to Clipboard
      </button>
    </div>

    <div
      id="error"
      class="hidden mt-6 p-4 bg-red-50 rounded-lg border border-red-200"
    >
      <p class="text-red-600 text-center"></p>
    </div>
  </div>

  <!-- FAQ Section -->
  <section class="mb-12">
    <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">
      Frequently Asked Questions
    </h2>
    <div class="space-y-4">
      <!-- Add your FAQs here following the existing pattern -->
    </div>
  </section>

  <!-- Related Tools Section -->
  {{ tool_links('your_tool_id') }}
</div>

<script>
  document
    .getElementById("yourToolForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const form = e.target;
      const submitButton = form.querySelector('button[type="submit"]');
      const loadingDiv = document.getElementById("loading");
      const resultDiv = document.getElementById("result");
      const errorDiv = document.getElementById("error");
      const resultContentDiv = document.getElementById("resultContent");

      // Show loading state
      submitButton.disabled = true;
      loadingDiv.classList.remove("hidden");
      resultDiv.classList.add("hidden");
      errorDiv.classList.add("hidden");

      try {
        const response = await fetch("/api/your-tool-endpoint", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            field1: form.field1.value,
            // Add other fields as needed
          }),
        });

        const data = await response.json();

        if (data.success) {
          resultContentDiv.innerHTML = data.your_result;
          resultDiv.classList.remove("hidden");
          resultDiv.classList.add("animate-fade-in");
        } else {
          throw new Error(data.error || "Failed to process request");
        }
      } catch (error) {
        console.error("Error:", error);
        errorDiv.querySelector("p").textContent = error.message;
        errorDiv.classList.remove("hidden");
      } finally {
        submitButton.disabled = false;
        loadingDiv.classList.add("hidden");
      }
    });

  function copyToClipboard() {
    const content = document.getElementById("resultContent").textContent;
    navigator.clipboard
      .writeText(content)
      .then(() => {
        alert("Copied to clipboard!");
      })
      .catch(() => {
        alert("Failed to copy to clipboard");
      });
  }
</script>

<style>
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-fade-in {
    animation: fade-in 0.3s ease-out forwards;
  }
</style>
{% endblock %}
```

### 4. Add Route to Main App

In `app/__init__.py`, import and register your new blueprint:

```python
from app.routes.tools.your_tool import your_tool_bp

def create_app():
    # ... existing setup ...

    app.register_blueprint(your_tool_bp)

    # ... rest of setup ...
```

### 5. Add Navigation Link

In `templates/base.html`, add your tool to the navigation menu:

```html
<div class="hidden md:flex items-center space-x-1">
  <!-- ... existing links ... -->
  <a
    href="/your-tool-url"
    class="py-4 px-2 text-gray-500 hover:text-green-500 transition duration-300"
  >
    Your Tool
  </a>
</div>
```

### 6. Add to Home Page

In `templates/index.html`, add your tool to the grid:

```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
  <!-- ... existing tools ... -->
  <a href="/your-tool-url" class="block">
    <div
      class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition duration-300"
    >
      <h2 class="text-xl font-semibold text-gray-800 mb-2">Your Tool Name</h2>
      <p class="text-gray-600">Brief description of your tool.</p>
    </div>
  </a>
</div>
```

## Best Practices

1. **Consistent Styling**: Use the existing color scheme (green accents) and UI components
2. **Error Handling**: Always include proper error handling and loading states
3. **Responsive Design**: Ensure your tool works well on all screen sizes
4. **Documentation**: Add clear comments and update this documentation if needed
5. **Testing**: Test your tool thoroughly before deployment
6. **Logging**: Use the logger for important events and errors

## Common Features to Include

1. Loading states
2. Error handling
3. Copy to clipboard functionality
4. Markdown rendering if needed
5. FAQ section
6. Related tools section
7. SEO meta tags
8. Responsive design elements

## Helpful Tips

1. Use the existing OpenAI service for AI-powered features
2. Follow the established pattern for API endpoints (/api/your-endpoint)
3. Maintain consistent UI/UX across tools
4. Use the existing logging configuration
5. Keep the code modular and maintainable
