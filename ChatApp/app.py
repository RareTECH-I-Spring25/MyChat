from flask import Flask, render_template, request, flash, redirect, url_for
import logging
from flask import session
from models import db_pool, User
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route("/")
def index():
    return render_template("auth/login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    import re
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')
        errors = []

        # 必須チェック
        if not user_type:
            errors.append("ユーザー種別は必須です")
        if not email:
            errors.append("メールアドレスは必須です")
        if not password:
            errors.append("パスワードは必須です")

        # メールアドレス形式チェック
        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append("正しいメールアドレス形式で入力してください")

        # パスワード長さチェック
        if password and len(password) < 6:
            errors.append("パスワードは6文字以上で入力してください")

        if errors:
            for error in errors:
                flash(error)
            return render_template('auth/login.html', email=email, user_type=user_type)

        # DB認証処理（親のみ）
        if user_type == 'parent':
            user = User.find_by_email(email)
            print('userの中身:', user, type(user))
            sys.stdout.flush()
            if not user:
                flash('メールアドレスまたはパスワードが違います')
                return render_template('auth/login.html', email=email, user_type=user_type)
            hashed_password = user['password']
            from werkzeug.security import check_password_hash
            if not check_password_hash(hashed_password, password):
                flash('メールアドレスまたはパスワードが違います')
                return render_template('auth/login.html', email=email, user_type=user_type)
            session['uid'] = user['parent_id']
            session['user_type'] = user_type
            return redirect(url_for('parent_dashboard'))
        elif user_type == 'child':
            flash('子どもユーザーのログインは未実装です')
            return render_template('auth/login.html', email=email, user_type=user_type)
    return render_template('auth/login.html')

@app.route('/signup/parent', methods=['GET', 'POST'])
def signup_parent():
    import re
    if request.method == 'POST':
        email = request.form.get('email')
        parent_user_name = request.form.get('parent_user_name')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        errors = []

        # 必須チェック
        if not email:
            errors.append("メールアドレスは必須です")
        if not parent_user_name:
            errors.append("ユーザー名は必須です")
        if not password:
            errors.append("パスワードは必須です")
        if not password_confirmation:
            errors.append("パスワード確認は必須です")

        # メールアドレス形式チェック
        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append("正しいメールアドレス形式で入力してください")

        # ユーザー名長さチェック
        if parent_user_name and (len(parent_user_name) < 1 or len(parent_user_name) > 10):
            errors.append("ユーザー名は1文字以上10文字以内で入力してください")

        # パスワード長さチェック
        if password and len(password) < 6:
            errors.append("パスワードは6文字以上で入力してください")

        # パスワード一致チェック
        if password and password_confirmation and password != password_confirmation:
            errors.append("パスワードが一致しません")

        if errors:
            for error in errors:
                flash(error)
            return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)

        try:
            import uuid
            from werkzeug.security import generate_password_hash
            uid = str(uuid.uuid4())
            hashed_password = generate_password_hash(password)
            User.create(uid, parent_user_name, email, hashed_password)
            flash('アカウント登録が完了しました。ログインしてください。')
            return redirect(url_for('login'))
        except ValueError as ve:
            flash(str(ve))
        except Exception as e:
            flash(f'登録に失敗しました: {e}')
        return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)
    return render_template('auth/signup-parent.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('ログアウトしました')
    return redirect(url_for('login'))

@app.route('/parent/dashboard', methods=['GET'])
def parent_dashboard():
    if 'uid' not in session or session.get('user_type') != 'parent':
        flash('ログインしてください')
        return redirect(url_for('login'))
    return render_template('parent/home.html')


#仮実装です
@app.route('/parent/update_child_time', methods=['POST'])
def update_child_time():
    child_id = request.form.get('child_id')
    status = request.form.get('status')
    flash('子どもアカウントの状態を更新しました')
    return redirect(url_for('parent_dashboard'))


#仮実装です
@app.route('/parent/add_child', methods=['GET', 'POST'])
def add_child():
    return render_template('parent/add_child.html')



@app.route('/child/dashboard',methods=['GET'])
def child_home():
    return render_template('child/home.html')


#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)