from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ユーザーモデル
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_parent = db.Column(db.Boolean, default=False)  # 親か子かの判定

#上記は仮の定義なので正式な定義が決まれば消してください　えすえす