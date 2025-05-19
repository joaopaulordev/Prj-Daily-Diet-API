from flask import Flask
from database import db
from models.refeicao import Refeicao
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "d7fe67f22404e87250775e79b8a324b0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/Prj-Daily-Diet-API'

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)