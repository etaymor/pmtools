from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI()  # This will automatically use OPENAI_API_KEY from environment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/value-proposition')
def value_proposition():
    return render_template('value_proposition.html')

@app.route('/api/generate-value-prop', methods=['POST'])
def generate_value_prop():
    data = request.json
    product_name = data.get('productName')
    target_audience = data.get('targetAudience')
    main_value = data.get('mainValue')
    
    prompt = f"""Create a compelling value proposition for:
    Product: {product_name}
    Target Audience: {target_audience}
    Main Value: {main_value}
    
    Format: Create a concise, powerful value proposition that highlights the unique benefits."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a marketing expert specialized in creating compelling value propositions."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return jsonify({
            "success": True,
            "value_proposition": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 