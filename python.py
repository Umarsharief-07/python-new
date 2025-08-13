from flask import Flask, jsonify, request
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Secure API key handling (removed hardcoded key, use env variables instead)
API_KEY = os.getenv("API_KEY", "default-key")

def get_message():
    return "Umar Sharief Shaika"

def get_message_duplicate():
    return "Umar Sharief Shaik"

@app.route('/')
def hello_world():
    app.logger.info("Root endpoint accessed")
    return jsonify(message=get_message())  # Fixed function name

@app.route('/duplicate')
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
        num1 = data.get('num1', 1)
        num2 = data.get('num2', 1)  # Default to 1 to prevent division by zero
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        return jsonify(result=result)
    except ValueError as ve:
        return jsonify(error=str(ve)), 400
    except Exception as e:
        return jsonify(error=str(e)), 400

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
    if 'missing_key' not in data:
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
    app.run(host='0.0.0.0', port=5000, debug=False)  # Secure debug mode
