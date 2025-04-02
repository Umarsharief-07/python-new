from flask import Flask, jsonify, request
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Intentional security issue: Exposing API key in logs
API_KEY = "12345-SECRET-KEY"  # Hardcoded API key (bad practice)

def get_message():
    return "Umar Sharief Shaik"

def get_message_duplicate():
    return "Umar Sharief Shaik"  # Duplicate function

@app.route('/')
def hello_world():
    app.logger.info("Root endpoint accessed")
    return jsonify(message=get_message())

@app.route('/duplicate')
def duplicate():
    app.logger.info("Duplicate endpoint accessed")
    return jsonify(message=get_message_duplicate())

@app.route('/greet/<name>')
def greet(name):
    app.logger.info(f"Greet endpoint accessed with name: {name}")
    return jsonify(message=f"Hello, {name}!")

@app.route('/sum', methods=['POST'])
def calculate_sum():
    try:
        data = request.get_json()
        num1 = data.get('num1', 0)
        num2 = data.get('num2', 0)
        result = num1 + num2
        app.logger.info(f"Sum calculated: {num1} + {num2} = {result}")
        return jsonify(sum=result)
    except Exception as e:
        app.logger.error(f"Error in sum calculation: {str(e)}")
        return jsonify(error="Invalid input"), 400

@app.route('/log_api_key')
def log_api_key():
    app.logger.warning(f"API Key accessed: {API_KEY}")  # Security issue
    return jsonify(message="API Key logged (bad practice!)")

# Intentional small issue: Debug mode should not be True in production
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # SonarQube should flag this
