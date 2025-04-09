from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1>Welcome to the Frontend! Try <a href='/api'>/api</a> to hit the backend via ALB.</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
