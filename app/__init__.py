from flask import Flask
from pathlib import Path

from .routes import main


def create_app():

    app = Flask(__name__)

    BASE_DIR = Path(__file__).resolve().parent.parent

    app.config["UPLOAD_DIR"] = BASE_DIR / "uploads"
    app.config["OUTPUT_DIR"] = BASE_DIR / "generated"

    app.config["UPLOAD_DIR"].mkdir(exist_ok=True)
    app.config["OUTPUT_DIR"].mkdir(exist_ok=True)

    app.register_blueprint(main)
    app.secret_key ="qwertyuiop"

    return app