# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Duplicate function - Intentional Code Duplication
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

# Intentional small issue: Debug mode should not be True in production
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # SonarQube should flag this
