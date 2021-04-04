from flask import Flask, render_template
from game_blueprint import game_gp

app = Flask(__name__, static_folder="static")
app.register_blueprint(game_gp)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/motivation")
def motivation_page():
    return render_template("motivation.html")

@app.route("/approach")
def approach_page():
    return render_template("approach.html")

@app.route("/concept")
def concept_page():
    return render_template("concept.html")

@app.route("/scenarios")
def scenarios_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

