from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from forms import ParentRegistrationForm
from forms import ChildRegistrationForm
import logging






# デバッグログの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'



@app.route('/')
def hello():
    return "Hello"


posts = {
    1:"post-1",
    2:"post-2",
    3:"post-3"
}


# 🔗 MySQLへの接続設定（ユーザー名・パスワード・ホスト名・DB名を適宜書き換えてください）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_username:your_password@mysql_container_name/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB初期化
db.init_app(app)

# ログインマネージャー
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



#親のサインアップ
@app.route('/signup/parent', methods=['GET', 'POST'])
def signup_parent():
    form = ParentRegistrationForm()
    if form.user_type.data in registered_emails:
        flash('このメールアドレスは既に登録されています。', 'error')
        return render_template('signup_parent.html', form=form)

    if form.validate_on_submit():
        registered_emails.add(form.email.data)
        flash('保護者用アカウントの登録が完了しました！ログインしてください。', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup_parent.html', form=form)
#子のサインアップ
@app.route('/signup/child', methods=['GET', 'POST'])
def signup_child():
    form = ChildRegistrationForm()
    if form.email.data in registered_emails:
        flash('このメールアドレスは既に登録されています。', 'error')
        return render_template('signup_child.html', form=form)

    if form.validate_on_submit():
        registered_emails.add(form.email.data)
        flash('子供アカウントの登録が完了しました！ログインしてください。', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup_child.html', form=form)



# 親と子のアカウントをどちらも読み込めるように
@login_manager.user_loader
def load_user(user_id):
    user = ParentUser.query.get(int(user_id))
    if user:
        return user
    return ChildUser.query.get(int(user_id))

# ログイン処理
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == 'parent':
            user = ParentUser.query.filter_by(email=form.email.data).first()
        else:
            user = ChildUser.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"{form.role.data}アカウントでログインしました", 'success')
            return redirect(url_for('dashboard'))

        flash('メールアドレスかパスワードが間違っています', 'error')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return f'ようこそ、{current_user.email} さん！'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました', 'info')
    return redirect(url_for('login'))






#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)