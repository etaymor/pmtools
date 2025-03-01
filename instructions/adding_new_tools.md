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
        'url': '/your-tool-url',  # IMPORTANT: This must match your main route path
        'category': 'Generators'  # or another appropriate category
    }
]
```

### 2. Create Route Handler

Create a new file in `app/routes/tools/your_tool.py`. You MUST include both the main route for the HTML page AND the API endpoint:

```python
from flask import Blueprint, request, jsonify, render_template
from app.utils.logging_config import logger
from app.services.openai_service import openai_service
from config.tools import get_tools_by_category  # Required for tool_links component

your_tool_bp = Blueprint('your_tool', __name__)

# IMPORTANT: Main route to serve the HTML page
@your_tool_bp.route('/your-tool-url')  # Must match the 'url' in tools.py
def your_tool():
    """Render the tool's main page."""
    return render_template('your_tool.html', get_tools_by_category=get_tools_by_category)

# API endpoint for tool functionality
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
        system_prompt = "System prompt defining AI's role"
        user_prompt = f"""Your prompt template here:
        Field1: {field1}
        Field2: {field2}

        Format your response as needed."""

        content, success = openai_service.generate_completion(system_prompt, user_prompt)

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

Create a new file in `templates/your_tool.html`. The template MUST extend base.html and include the tool_links component:

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
    <h1
      class="text-3xl md:text-4xl font-bold text-gray-800 dark:text-gray-100 mb-4 leading-tight"
    >
      Your Tool Name
    </h1>
    <div
      class="prose prose-base mx-auto text-gray-600 dark:text-gray-300 max-w-2xl"
    >
      <p class="text-base md:text-lg leading-relaxed">
        Your tool's description here.
      </p>
    </div>
  </div>

  <!-- Main Form Card -->
  <div
    class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-12 transform transition-all duration-300 hover:shadow-2xl"
  >
    <form id="yourToolForm" class="space-y-8">
      <!-- Example form field with dark mode support -->
      <div class="relative">
        <label
          for="exampleField"
          class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
        >
          Example Field
        </label>
        <input
          type="text"
          id="exampleField"
          name="exampleField"
          required
          class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 bg-gray-50 dark:bg-gray-700 hover:bg-white dark:hover:bg-gray-600 dark:text-gray-100"
          placeholder="Enter some text here"
        />
      </div>

      <button
        type="submit"
        class="w-full bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-4 rounded-lg font-semibold text-lg hover:from-green-600 hover:to-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
      >
        Generate Result
      </button>
    </form>

    <!-- Loading Spinner -->
    <div id="loading" class="hidden mt-8 text-center">
      <div
        class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-green-500 border-t-transparent"
      ></div>
      <p class="mt-2 text-gray-600 dark:text-gray-300">
        Processing your request...
      </p>
    </div>

    <!-- Result Section -->
    <div id="result" class="hidden mt-8 transform transition-all duration-300">
      <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">
        Your Result:
      </h2>
      <div
        id="resultContent"
        class="p-6 bg-gradient-to-br from-green-50 to-blue-50 dark:from-gray-700 dark:to-gray-600 rounded-lg text-gray-700 dark:text-gray-200 text-lg leading-relaxed border border-green-100 dark:border-gray-500 shadow-sm"
        contenteditable="false"
      ></div>
      <div class="mt-4 flex space-x-2">
        <button
          onclick="copyToClipboard()"
          class="inline-flex items-center justify-center rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 px-4 text-sm font-medium text-gray-700 dark:text-gray-200 shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
            <path
              d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z"
            />
          </svg>
          Copy to Clipboard
        </button>
        <button
          onclick="toggleEdit()"
          id="editButton"
          class="inline-flex items-center justify-center rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 px-4 text-sm font-medium text-gray-700 dark:text-gray-200 shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
            />
          </svg>
          Edit
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div
      id="error"
      class="hidden mt-6 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800"
    >
      <p class="text-red-600 dark:text-red-400 text-center"></p>
    </div>
  </div>

  <!-- Share Buttons -->
  {{ share_buttons() }}

  <!-- FAQ Section -->
  <section class="mb-12">
    <h2
      class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-8 text-center"
    >
      Frequently Asked Questions
    </h2>
    <div class="space-y-4">
      <details class="group bg-white dark:bg-gray-800 rounded-xl shadow-sm">
        <summary
          class="flex items-center justify-between p-6 text-lg font-medium text-gray-800 dark:text-gray-200 cursor-pointer hover:text-green-600 dark:hover:text-green-400 transition-colors duration-200"
        >
          Your Question Here
          <span
            class="transform group-open:rotate-180 transition-transform duration-200"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>
          </span>
        </summary>
        <div class="px-6 pb-6 text-gray-600 dark:text-gray-300">
          <p>Your answer here.</p>
        </div>
      </details>
    </div>
  </section>

  <!-- IMPORTANT: Include the tool_links component with your tool's ID -->
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
            // Your form data here
          }),
        });

        const data = await response.json();

        if (data.success) {
          resultContentDiv.innerHTML = data.result;
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
        // Use a more subtle notification in dark mode
        const isDarkMode = document.documentElement.classList.contains("dark");
        const alertBg = isDarkMode ? "#374151" : "white";
        const alertText = isDarkMode ? "#e5e7eb" : "#374151";
        const alertEl = document.createElement("div");
        alertEl.style.position = "fixed";
        alertEl.style.bottom = "20px";
        alertEl.style.right = "20px";
        alertEl.style.padding = "10px 20px";
        alertEl.style.background = alertBg;
        alertEl.style.color = alertText;
        alertEl.style.borderRadius = "4px";
        alertEl.style.boxShadow = "0 2px 8px rgba(0, 0, 0, 0.15)";
        alertEl.style.zIndex = "9999";
        alertEl.textContent = "Copied to clipboard!";
        document.body.appendChild(alertEl);

        setTimeout(() => {
          alertEl.style.opacity = "0";
          alertEl.style.transition = "opacity 0.5s ease";
          setTimeout(() => document.body.removeChild(alertEl), 500);
        }, 2000);
      })
      .catch(() => {
        alert("Failed to copy to clipboard");
      });
  }

  function toggleEdit() {
    const resultContentDiv = document.getElementById("resultContent");
    const editButton = document.getElementById("editButton");
    const isEditing = resultContentDiv.contentEditable === "true";

    if (isEditing) {
      // Save mode
      resultContentDiv.contentEditable = "false";
      resultContentDiv.classList.remove("ring-2", "ring-green-500");
      editButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
        Edit
      `;
    } else {
      // Edit mode
      resultContentDiv.contentEditable = "true";
      resultContentDiv.classList.add("ring-2", "ring-green-500");
      editButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        Save
      `;
      resultContentDiv.focus();
    }
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

### 4. Register the Blueprint

In `app/__init__.py`, import and register your blueprint:

```python
# Register blueprints
from app.routes.tools.your_tool import your_tool_bp  # Import your blueprint
app.register_blueprint(your_tool_bp)  # Register it
```

## Common Errors and Solutions

### 404 Not Found Error

If you get a 404 error when accessing your tool's page:

1. Verify that the `url` in your tool configuration matches exactly with your main route path
2. Ensure you have created the main route handler (not just the API endpoint)
3. Check that your blueprint is properly registered in `app/__init__.py`

### Template Context Errors

If you get a "jinja2.exceptions.UndefinedError" about missing functions:

1. Make sure to import `get_tools_by_category` from `config.tools`
2. Pass it to the template context in your main route handler:
   ```python
   return render_template('your_tool.html', get_tools_by_category=get_tools_by_category)
   ```

### Blueprint Registration

Common blueprint issues:

1. Import the blueprint in `app/__init__.py`
2. Register it with `app.register_blueprint()`
3. Ensure the blueprint name matches your file name
4. Check for any import errors in the console

## Testing Your New Tool

Before committing your changes:

1. Test the main page loads without errors
2. Test the API endpoint with valid and invalid inputs
3. Verify all components (forms, buttons, results) work as expected
4. Check that related tools are displayed correctly
5. Test error handling and loading states

Remember to follow the existing patterns and maintain consistency with other tools in the application.

## Best Practices

1. **Consistent Styling**: Use the existing color scheme (green accents) and UI components
2. **Error Handling**: Always include proper error handling and loading states
3. **Responsive Design**: Ensure your tool works well on all screen sizes
4. **Documentation**: Add clear comments and update this documentation if needed
5. **Testing**: Test your tool thoroughly before deployment
6. **Logging**: Use the logger for important events and errors
7. **User Interaction**: Include edit and copy functionality for generated content
8. **Accessibility**: Ensure all interactive elements are keyboard-accessible
9. **Dark Mode Support**: Implement dark mode styling for all UI elements

## Dark Mode Implementation

All tools must support dark mode. Follow these guidelines to ensure consistent dark mode styling:

### 1. Text Colors

- Headings: `text-gray-800 dark:text-gray-100`
- Regular text: `text-gray-600 dark:text-gray-300`
- Secondary text: `text-gray-500 dark:text-gray-400`
- Input labels: `text-gray-700 dark:text-gray-300`
- Input text: `dark:text-gray-100`
- Error messages: `text-red-600 dark:text-red-400`

### 2. Background Colors

- Main card backgrounds: `bg-white dark:bg-gray-800`
- Input fields: `bg-gray-50 dark:bg-gray-700` with `hover:bg-white dark:hover:bg-gray-600`
- Button hover states: `hover:bg-gray-50 dark:hover:bg-gray-600`
- Error message backgrounds: `bg-red-50 dark:bg-red-900/20`
- Result content backgrounds: `from-green-50 to-blue-50 dark:from-gray-700 dark:to-gray-600`

### 3. Border Colors

- Input fields: `border-gray-300 dark:border-gray-600`
- Buttons: `border-gray-300 dark:border-gray-600`
- Error messages: `border-red-200 dark:border-red-800`

### 4. Focus and Hover States

- Focus rings: `focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800`
- Text hover: `hover:text-green-600 dark:hover:text-green-400`

### 5. Clipboard Notification

Replace basic alerts with custom notifications that adapt to dark mode:

```javascript
function copyToClipboard() {
  const content = document.getElementById("resultContent").textContent;
  navigator.clipboard
    .writeText(content)
    .then(() => {
      // Use a more subtle notification in dark mode
      const isDarkMode = document.documentElement.classList.contains("dark");
      const alertBg = isDarkMode ? "#374151" : "white";
      const alertText = isDarkMode ? "#e5e7eb" : "#374151";
      const alertEl = document.createElement("div");
      alertEl.style.position = "fixed";
      alertEl.style.bottom = "20px";
      alertEl.style.right = "20px";
      alertEl.style.padding = "10px 20px";
      alertEl.style.background = alertBg;
      alertEl.style.color = alertText;
      alertEl.style.borderRadius = "4px";
      alertEl.style.boxShadow = "0 2px 8px rgba(0, 0, 0, 0.15)";
      alertEl.style.zIndex = "9999";
      alertEl.textContent = "Copied to clipboard!";
      document.body.appendChild(alertEl);

      setTimeout(() => {
        alertEl.style.opacity = "0";
        alertEl.style.transition = "opacity 0.5s ease";
        setTimeout(() => document.body.removeChild(alertEl), 500);
      }, 2000);
    })
    .catch(() => {
      alert("Failed to copy to clipboard");
    });
}
```

### 6. Testing Dark Mode

Always test your tool in both light and dark modes:

1. Toggle dark mode in your browser using the theme switcher in the application
2. Verify all text is readable and has sufficient contrast
3. Check that all interactive elements are clearly visible
4. Ensure transitions between states work correctly in both modes

## Common Features to Include

1. Loading states
2. Error handling
3. Copy to clipboard functionality
4. Edit functionality with pencil/save icons
5. Markdown rendering if needed
6. FAQ section with expandable details
7. Related tools section
8. SEO meta tags
9. Responsive design elements
10. Social sharing buttons

## FAQ Section Example

Each tool should include an FAQ section with expandable details. Here's the standard pattern:

```html
<!-- FAQ Section -->
<section class="mb-12">
  <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">
    Frequently Asked Questions
  </h2>
  <div class="space-y-4">
    <details class="group bg-white rounded-xl shadow-sm">
      <summary
        class="flex items-center justify-between p-6 text-lg font-medium text-gray-800 cursor-pointer hover:text-green-600 transition-colors duration-200"
      >
        Your Question Here
        <span
          class="transform group-open:rotate-180 transition-transform duration-200"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            ></path>
          </svg>
        </span>
      </summary>
      <div class="px-6 pb-6 text-gray-600">
        <p>Your answer here.</p>
      </div>
    </details>
  </div>
</section>
```

Key features of the FAQ section:

- Uses HTML5 `<details>` and `<summary>` elements for native expand/collapse
- Includes animated chevron that rotates on expansion
- Consistent styling with hover effects
- Accessible keyboard navigation
- Smooth transitions

## Social Sharing Integration

Each tool should include social sharing buttons. To add them to your tool:

1. Import the share buttons component at the top of your template:

```jinja2
{% from "components/share_buttons.html" import share_buttons with context %}
```

2. Add the share buttons after your main form card and before the FAQ section:

```jinja2
{{ share_buttons() }}
```

The share buttons will:

- Desktop: Display as a vertical floating bar on the left side
- Mobile: Transform into a horizontal bar fixed at the bottom of the screen
- Include sharing options for:
  - General share (AddToAny)
  - X (Twitter)
  - Email
  - LinkedIn
  - Facebook
  - Bluesky

The share buttons are automatically styled and positioned, with responsive behavior built-in. The AddToAny script is loaded in the base template, so there's no need to include it in your tool's template.

## Helpful Tips

1. Use the existing OpenAI service for AI-powered features
2. Follow the established pattern for API endpoints (/api/your-endpoint)
3. Maintain consistent UI/UX across tools
4. Use the existing logging configuration
5. Keep the code modular and maintainable
6. Include edit functionality for all generated content
7. Provide clear visual feedback for user actions
8. Use consistent button styling and layout
