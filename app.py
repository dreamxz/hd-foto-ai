from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
import replicate
import base64
import os
from io import BytesIO

app = Flask(__name__)
app.secret_key = "secret-rahasia-anda"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "rahasia123":
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Username atau password salah.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/enhance", methods=["POST"])
def enhance():
    data = request.get_json()
    image_base64 = data["image_base64"]
    image_bytes = BytesIO(base64.b64decode(image_base64))

    output_url = replicate.run(
        "sczhou/codeformer:1e4493cf3086b5c7666d06e4d49ca03f21e244c42144cacf41d6c8c2d45abf3b",
        input={"image": image_bytes, "codeformer_fidelity": 1}
    )

    return jsonify({"output": output_url})
