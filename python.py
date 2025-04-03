import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Hardcoded API key (security issue)
API_KEY = "12345-SECRET-KEY"

# Bug 1: Unused variable
unused_variable = "This variable is never used"

# Bug 2: Incorrect function call (potential NameError)
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
    return jsonify(message=get_message_typo())  # Bug: Undefined function (should be get_message())

@app.route('/duplicate')
def duplicate():
    app.logger.info("Duplicate endpoint accessed")
    return jsonify(message=get_message_duplicate())

# Bug 3: Missing return statement
@app.route('/missing_return')
def missing_return():
    message = "This function does not return anything"  # Missing return statement

# Bug 4: Infinite loop
@app.route('/infinite_loop')
def infinite_loop():
    while True:
        pass  # This will cause the request to hang indefinitely

# Bug 5: Incorrect exception handling
@app.route('/error_handling', methods=['GET'])
def error_handling():
    try:
        1 / 0  # Intentional error
    except:
        return "Error occurred", 200  # Issue: Returns 200 instead of an error code

# Bug 6: Division by zero potential
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

# Bug 7: Misuse of list index
@app.route('/list_index', methods=['GET'])
def list_index():
    items = ["apple", "banana"]
    return jsonify(item=items[5])  # IndexError: List index out of range

# Bug 8: Undefined variable usage
@app.route('/undefined_variable', methods=['GET'])
def undefined_variable():
    return jsonify(message=undefined_var)  # NameError: undefined_var is not defined

# Bug 9: JSON key error
@app.route('/json_key', methods=['POST'])
def json_key_error():
    data = request.get_json()
    return jsonify(value=data['missing_key'])  # KeyError: 'missing_key' not found

# Bug 10: Incorrect boolean condition
@app.route('/bool_check', methods=['GET'])
def bool_check():
    value = None
    if value == True:  # Bug: 'is' should be used for comparison with None
        return jsonify(message="True value")
    return jsonify(message="False value")

# Intentional small issue: Debug mode should not be True in production
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # SonarQube should flag this
