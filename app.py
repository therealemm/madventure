import json
import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# Load narrative
with open(os.path.join("dreams", "dream1.json")) as f:
    DREAM = json.load(f)

@app.route("/")
def index():
    scene_id = session.get("scene")
    if not scene_id:
        # Player hasn't started yet, show the start page
        return render_template("start.html")

    scene = DREAM.get(scene_id, DREAM.get("start"))
    choices = scene.get("choices", [])
    return render_template(
        "index.html",
        text=scene.get("text", ""),
        choices=choices,
        scene_id=scene_id,
    )

@app.route("/choice", methods=["POST"])
def choose():
    next_scene = request.form.get("next")
    if next_scene in DREAM:
        session["scene"] = next_scene
    else:
        session["scene"] = "start"
    return redirect(url_for("index"))


@app.route("/begin", methods=["POST"])
def begin():
    """Start the story from the first scene."""
    session["scene"] = "start"
    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():
    """Clear the saved scene and restart the story."""
    session.pop("scene", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
