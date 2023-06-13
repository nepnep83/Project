from flask import Blueprint

bp = Blueprint("main", __name__, template_folder="../templates/main")

from app.main import Render  # noqa: E402,F401
