from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def hello():
    return render_template("/home/home.html")

if __name__ == "__main__":
    app.run(debug=True)
