from app import create_app
from flask_session import Session
app = create_app()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
session = Session()
session.init_app(app)