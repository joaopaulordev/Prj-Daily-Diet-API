from database import db
from flask_login import UserMixin


class Refeicao(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(300), nullable=False)
  descricao = db.Column(db.String(600), nullable=False)
  data_ref = db.Column(db.DateTime)
  isDiet = db.Column(db.Boolean, nullable=False, default=True)
  # ForeignKey
  id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)