from database import db
from flask_login import UserMixin
from datetime import datetime

class Refeicao(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(300), nullable=False)
  descricao = db.Column(db.String(600), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  isDiet = db.Column(db.Boolean, nullable=False, default=True)