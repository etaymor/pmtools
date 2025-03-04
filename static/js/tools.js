// Shared functionality for all PM Tools

// Markdown rendering function
function renderMarkdown(text) {
  // Handle headers (h1-h4)
  text = text.replace(
    /^# (.*?)$/gm,
    "<h1 class='text-2xl font-bold mb-4 mt-6'>$1</h1>"
  );
  text = text.replace(
    /^## (.*?)$/gm,
    "<h2 class='text-xl font-bold mb-3 mt-5'>$1</h2>"
  );
  text = text.replace(
    /^### (.*?)$/gm,
    "<h3 class='text-lg font-bold mb-2 mt-4'>$1</h3>"
  );
  text = text.replace(
    /^#### (.*?)$/gm,
    "<h4 class='text-base font-bold mb-2 mt-3'>$1</h4>"
  );

  // Handle bold text with double asterisks
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Handle italic text with single asterisks
  text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");

  // Handle bullet points
  text = text.replace(/^- (.*?)$/gm, "<li class='ml-4'>$1</li>");

  // Handle numbered lists
  text = text.replace(/^\d+\. (.*?)$/gm, "<li class='ml-4'>$1</li>");

  // Handle line breaks
  text = text.replace(/\n/g, "<br>");

  return text;
}

// Copy to clipboard functionality
function copyToClipboard(content) {
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

// Toggle edit functionality
function toggleEdit(contentDivId, editButtonId) {
  const contentDiv = document.getElementById(contentDivId);
  const editButton = document.getElementById(editButtonId);
  const isEditing = contentDiv.contentEditable === "true";

  if (isEditing) {
    // Save mode
    contentDiv.contentEditable = "false";
    contentDiv.classList.remove("ring-2", "ring-green-500");
    editButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
      </svg>
      Edit
    `;
  } else {
    // Edit mode
    contentDiv.contentEditable = "true";
    contentDiv.classList.add("ring-2", "ring-green-500");
    editButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      Save
    `;
    contentDiv.focus();
  }
}

// Form submission handler
async function handleFormSubmit(
  formId,
  endpoint,
  formData,
  resultDivId,
  contentDivId
) {
  const form = document.getElementById(formId);
  const submitButton = form.querySelector('button[type="submit"]');
  const loadingDiv = document.getElementById("loading");
  const resultDiv = document.getElementById(resultDivId);
  const errorDiv = document.getElementById("error");
  const contentDiv = document.getElementById(contentDivId);

  // Show loading state
  submitButton.disabled = true;
  loadingDiv.classList.remove("hidden");
  resultDiv.classList.add("hidden");
  errorDiv.classList.add("hidden");

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();

    if (data.success) {
      contentDiv.innerHTML = renderMarkdown(
        data[Object.keys(data).find((key) => key !== "success")]
      );
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
}
