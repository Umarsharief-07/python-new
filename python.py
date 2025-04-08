from flask import Flask

app = Flask(__name__)

@app.route("/")
def client2():
    return "<h1>Welcome to Client-2 hai ab</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
