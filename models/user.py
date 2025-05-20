from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False) 
  
  refeicoes = db.relationship("Meal", backref='user', lazy=True)

  def total_refeicoes(self):
        return len(self.refeicoes)