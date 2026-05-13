import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO

from app.backend import mqtt_bridge

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "face-demo-secret")
socketio = SocketIO(app, cors_allowed_origins="*")

mqtt_bridge.attach_socketio(socketio)
mqtt_bridge.start_mqtt(background=True)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", "5000"))
    socketio.run(app, host="0.0.0.0", port=port, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
