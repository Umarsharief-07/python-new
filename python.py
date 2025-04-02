from flask import Flask, jsonify, request
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Hardcoded API key (security issue)
API_KEY = "12345-SECRET-KEY"

# Bug: Unused variable
unused_variable = "This variable is never used"

def get_message():
    return "Umar Sharief Shaik"

def get_message_duplicate():
    return "Umar Sharief Shaik"  # Duplicate function

def insecure_eval(expression):
    """Dangerous function: Executes arbitrary code"""
    return eval(expression)  # Security vulnerability (code injection)

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

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        result = insecure_eval(expression)  # Code injection vulnerability
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 400

# Bug: Division by zero potential
@app.route('/divide', methods=['POST'])
def divide_numbers():
    try:
        data = request.get_json()
        num1 = data.get('num1', 1)
        num2 = data.get('num2', 0)  # Issue: Possible division by zero
        result = num1 / num2
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 400

# Vulnerability: OS command injection
@app.route('/run', methods=['POST'])
def run_command():
    command = request.get_json().get('command', '')
    output = os.popen(command).read()  # Security issue: Executes arbitrary system commands
    return jsonify(output=output)

# Bug: Incorrect error handling
@app.route('/error_handling', methods=['GET'])
def error_handling():
    try:
        1 / 0  # Intentional error
    except:
        return "Error occurred", 200  # Issue: Returns 200 instead of an error code

# Security Hotspot: Hardcoded credentials
USERNAME = "admin"
PASSWORD = "password123"  # Security issue

# Code Smell: Redundant condition
@app.route('/check_status', methods=['GET'])
def check_status():
    status = request.args.get('status', 'ok')
    if status == "ok":
        return jsonify(message="Everything is fine")
    elif status == "ok":  # Redundant condition
        return jsonify(message="Still fine")
    else:
        return jsonify(message="Something is wrong")

# Code Smell: Unnecessary list comprehension
@app.route('/list_comprehension', methods=['GET'])
def list_comprehension():
    numbers = [x for x in range(10)]  # Can be replaced with list(range(10))
    return jsonify(numbers=numbers)

# Intentional small issue: Debug mode should not be True in production
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # SonarQube should flag this
