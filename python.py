from flask import Flask

app = Flask(__name__)

@app.route("/")

def client1():
    return "<h1>Welcome to Client-1 welcome checking-1 </h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

