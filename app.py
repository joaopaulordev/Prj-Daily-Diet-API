from flask import Flask, jsonify, request
from database import db
from models.meal import Meal
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.user import User
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "d7fe67f22404e87250775e79b8a324b0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/Prj-Daily-Diet-API'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


# =======
# Gerenciamento das refeições de usuários
# Um usuário pode ter várias refeições
# =================

# Cria refeição para o usuário logado.
@app.route("/refeicao", methods=['POST'])
@login_required
def create_meal():
    data = request.get_json()
    name = data.get("nome")
    description = data.get("descricao")
    date_meal = data.get("datahora")
    isDiet = data.get("isDiet")

    if name and description:
        meal = Meal(name=name, description=description, date_meal=date_meal, isDiet=isDiet, id_user=current_user.id)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Refeição criada com sucesso."})
    return jsonify({"message": "Dados inválidos."}), 400


# Deve ser possível visualizar uma única refeição
@app.route('/refeicao/<int:id_meal>', methods=["GET"])
@login_required
def read_meal(id_meal):
    meal = Meal.query.get(id_meal)

    if meal:
        return meal.to_dict()
    return jsonify({"message": "Refeição não encontrado."}), 404


# Deve ser possível editar uma refeição, podendo alterar todos os dados
@app.route('/refeicao/<int:id_meal>', methods=["PUT"])
@login_required
def update_meal(id_meal):
    meal = Meal.query.get(id_meal)
    if meal:
        data = request.json
        meal.name = data.get("nome")
        meal.description = data.get("descricao")
        meal.date_meal = data.get("datahora")
        meal.isDiet = data.get("isDiet")
        meal.id_user = data.get("id_usuario")
        db.session.commit()
        return jsonify({"message": f"Refeição {id_meal} atualizada com sucesso."})    
    return jsonify({"message": "Refeição não encontrada."}), 404



# Deve ser possível listar todas as refeições de um usuário
@app.route('/refeicao/usuario/<int:id_user>', methods=["GET"])
@login_required
def read_meals_by_user(id_user):
    user_meals = Meal.query.filter_by(id_user=id_user).all()

    if len(user_meals) > 0:
        list_meals_dict = [meal.to_dict() for meal in user_meals]
        return { "refeicoes": list_meals_dict }
    return jsonify({"message": "Id do usuário informado não contém refeições."}), 404


# Deve ser possível apagar uma refeição
@app.route('/refeicao/<int:id_meal>', methods=["DELETE"])
@login_required
def delete_meal(id_meal):
    meal = Meal.query.get(id_meal)
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Refeição {id_meal} deletada com sucesso."})    
    return jsonify({"message": "Refeição não encontrada."}), 404




#============
###Gerenciamento de usuários
#===================

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso."})


@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if current_user.is_authenticated:
        return jsonify({"message": "Você já está autenticado."})

    if username and password:
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)            
            return jsonify({"message": "Autenticação realizada com sucesso."})
    return jsonify({"message": "Credenciais inválidas."}), 400



@app.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso."})
    return jsonify({"message": "Dados inválidos."}), 400


@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {
            "username": user.username,            
            "total_refeicoes": user.total_refeicoes()
        }
    return jsonify({"message": "Usuário não encontrado."}), 404


@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    if id_user != current_user.id:
        return jsonify({"message": "Operação não permitida"}), 403

    user = User.query.get(id_user)
    data = request.json    
    if user and data.get('password'):
        hashed_password = bcrypt.hashpw(str.encode(data.get('password')), bcrypt.gensalt())
        user.password = hashed_password
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso."})    
    return jsonify({"message": "Usuário não encontrado."}), 404


@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    if current_user.id == id_user:
        return jsonify({"message": "Deleção não permitida."}), 403
    
    user = User.query.get(id_user)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso."})    
    return jsonify({"message": "Usuário não encontrado."}), 404


if __name__ == '__main__':
    app.run(debug=True)