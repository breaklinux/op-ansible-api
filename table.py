from models import db
from __init__ import create_app
app = create_app()
with app.app_context():
    db.create_all()
