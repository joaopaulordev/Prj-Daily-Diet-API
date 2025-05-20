from database import db
from flask_login import UserMixin


class Meal(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(300), nullable=False)
  description = db.Column(db.String(600), nullable=False)
  date_meal= db.Column(db.DateTime)
  isDiet = db.Column(db.Boolean, nullable=False, default=True)
  # ForeignKey
  id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


  def to_dict(self):
      return {
         "id": self.id,
         "nome": self.name,
         "descricao": self.description,
         "datahora": self.date_meal,
         "isDiet": self.isDiet,
         "id_usuario": self.id_user
      }