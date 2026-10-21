import os

from flask import Flask, redirect, url_for
import control

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ventilador 3D</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            background: #0f0f0f;
            color: #ffffff;
            font-family: Arial, Helvetica, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            width: 100%;
            max-width: 360px;
            text-align: center;
        }

        h1 {
            margin-bottom: 30px;
            font-size: 26px;
        }

        .buttons {
            display: flex;
            justify-content: space-between;
            gap: 15px;
        }

        a {
            flex: 1;
            text-decoration: none;
            padding: 25px 0;
            font-size: 22px;
            font-weight: bold;
            border-radius: 12px;
            color: #fff;
            user-select: none;
        }

        .prev {
            background: #444;
        }

        .next {
            background: #e10600;
        }

        a:active {
            transform: scale(0.95);
        }

        .footer {
            margin-top: 30px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>🎥 Ventilador 3D</h1>

        <div class="buttons">
            <a class="prev" href="/prev">⬅ ANTERIOR</a>
            <a class="next" href="/next">SIGUIENTE ➡</a>
        </div>

        <div class="footer">
            Control remoto activo
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/next")
def next_video():
    control.video_index += 1
    control.cambiar_video = True
    return redirect(url_for("home"))

@app.route("/prev")
def prev_video():
    control.video_index -= 1
    control.cambiar_video = True
    return redirect(url_for("home"))

def run_server():
    app.run(host=os.getenv("SERVER_HOST", "0.0.0.0"), port=int(os.getenv("SERVER_PORT", "5000")))
