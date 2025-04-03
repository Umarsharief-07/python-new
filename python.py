from flask import Flask, jsonify, request
import logging
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# Initialize Flask app
app = Flask(__name__)
Talisman(app)  # Add security headers

# Configure logging (Avoid logging sensitive data)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Secure API key handling
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")

# Rate Limiting to prevent DoS attacks
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per hour"])

def get_message():
    return "Umar Sharief Shaik"

def get_message_duplicate():
    return "Umar Sharief Shaik"

@app.route('/')
@limiter.limit("10 per minute")  # Limit excessive requests
def hello_world():
    app.logger.info("Root endpoint accessed")
    return jsonify(message=get_message())

@app.route('/duplicate')
@limiter.limit("10 per minute")
def duplicate():
    app.logger.info("Duplicate endpoint accessed")
    return jsonify(message=get_message_duplicate())

@app.route('/missing_return')
def missing_return():
    message = "This function now returns a response"
    return jsonify(message=message)

@app.route('/safe_divide', methods=['POST'])
def safe_divide():
    try:
        data = request.get_json()
        if not data or 'num1' not in data or 'num2' not in data:
            return jsonify(error="Missing num1 or num2 in JSON body"), 400
        
        num1, num2 = data.get('num1'), data.get('num2')
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            return jsonify(error="Invalid input type"), 400
        
        if num2 == 0:
            return jsonify(error="Cannot divide by zero"), 400
        
        result = num1 / num2
        return jsonify(result=result)
    except Exception as e:
        app.logger.error(f"Error in safe_divide: {str(e)}")
        return jsonify(error="Internal Server Error"), 500

@app.route('/list_index', methods=['GET'])
def list_index():
    items = ["apple", "banana"]
    try:
        return jsonify(item=items[1])  # Fixed: Accessing a valid index
    except IndexError:
        return jsonify(error="Index out of range"), 400

@app.route('/undefined_variable', methods=['GET'])
def undefined_variable():
    defined_var = "Now defined"
    return jsonify(message=defined_var)

@app.route('/json_key', methods=['POST'])
def json_key_error():
    data = request.get_json()
    if not data or 'missing_key' not in data:
        return jsonify(error="Missing key in JSON request"), 400
    return jsonify(value=data['missing_key'])

@app.route('/bool_check', methods=['GET'])
def bool_check():
    value = None
    if value is True:  # Fixed improper comparison
        return jsonify(message="True value")
    return jsonify(message="False value")

# Secure exception handling
@app.route('/error_handling', methods=['GET'])
def error_handling():
    try:
        1 / 0  # Intentional error
    except ZeroDivisionError:
        return jsonify(error="Division by zero is not allowed"), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=False)  # Secure port handling
