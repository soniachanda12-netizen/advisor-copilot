from flask import Flask, request, jsonify
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from prompts.templates import get_advisor_prompt
from queries.bigquery import get_customer_portfolio
from utils.format import format_portfolio

app = Flask(__name__)

# Initialize Google Cloud clients
project_id = os.getenv('PROJECT_ID')
location = os.getenv('LOCATION', 'us-central1')
model_name = os.getenv('MODEL_NAME', 'gemini-2.0-flash-lite-001')

# Initialize Vertex AI
vertexai.init(project=project_id, location=location)

# Initialize the model
model = GenerativeModel(model_name)

@app.route('/advice', methods=['POST'])
def get_financial_advice():
    try:
        data = request.json
        customer_id = data.get('customer_id')
        query = data.get('query')

        if not customer_id or not query:
            return jsonify({'error': 'Missing customer_id or query'}), 400

        # Get customer portfolio from BigQuery
        portfolio = get_customer_portfolio(customer_id)
        
        # Format portfolio for prompt
        formatted_portfolio = format_portfolio(portfolio)
        
        # Generate prompt with portfolio context
        prompt = get_advisor_prompt(formatted_portfolio, query)
        
        # Get response from Vertex AI
        response = model.generate_content(prompt)
        
        return jsonify({
            'advice': response.text,
            'portfolio': portfolio
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
