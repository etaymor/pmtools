# SEO Tools

A collection of free SEO tools built with Flask and Tailwind CSS.

## Features

- Value Proposition Generator: Create compelling value propositions using AI

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Visit `http://localhost:5000` in your browser

## Usage

### Value Proposition Generator

1. Navigate to the Value Proposition Generator page
2. Enter your product name, target audience, and main value
3. Click "Generate Value Proposition"
4. The AI-generated value proposition will appear below the form

## Technologies Used

- Backend: Flask
- Frontend: HTML, JavaScript, Tailwind CSS
- AI: OpenAI GPT-3.5
