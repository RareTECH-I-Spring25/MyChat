from flask import Flask, render_template, request, flash, redirect, url_for
import logging
from flask import session
from models import db_pool, User, Child
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
            # 子どもユーザーの認証処理
            child = Child.find_by_email(email)
            if not child:
                flash('メールアドレスまたはパスワードが違います')
                return render_template('auth/login.html', email=email, user_type=user_type)
            hashed_password = child['password']
            from werkzeug.security import check_password_hash
            if not check_password_hash(hashed_password, password):
                flash('メールアドレスまたはパスワードが違います')
                return render_template('auth/login.html', email=email, user_type=user_type)
            if child['child_status'] != 1:
                flash('このアカウントは現在使用できません。保護者にご確認ください。')
                return render_template('auth/login.html', email=email, user_type=user_type)
            session['uid'] = child['child_id']
            session['user_type'] = user_type
            return redirect(url_for('child_home'))
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

    parent = User.find_by_id(session['uid'])
    # DBから子どもリストを取得
    children = Child.find_by_parent_id(session['uid'])
    return render_template('parent/home.html', parent=parent, children=children)

@app.route('/parent/child/add',methods=['GET','POST'])
def add_child():
    import re
    if request.method == 'POST':
        identification_id = request.form.get('identification_id')
        child_user_name = request.form.get('child_user_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        errors = []

        # identification_idのバリデーション
        if not identification_id:
            errors.append("任意のIDは必須です")
        elif len(identification_id) < 1 or len(identification_id) > 10:
            errors.append("任意のIDは1文字以上10文字以内で入力してください")

        # バリデーション
        if not child_user_name:
            errors.append("子どもの名前は必須です")
        elif len(child_user_name) < 1 or len(child_user_name) > 10:
            errors.append("子どもの名前は1文字以上10文字以内で入力してください")

        if not email:
            errors.append("メールアドレスは必須です")
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append("正しいメールアドレス形式で入力してください")

        if not password:
            errors.append("パスワードは必須です")
        elif len(password) < 6:
            errors.append("パスワードは6文字以上で入力してください")

        if not password_confirmation:
            errors.append("パスワード確認は必須です")

        if password and password_confirmation and password != password_confirmation:
            errors.append("パスワードが一致しません")

        if errors:
            for error in errors:
                flash(error)
            return render_template('parent/child/add.html', identification_id=identification_id, child_user_name=child_user_name, email=email)

        # パスワードハッシュ化
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)

        # friend_child_user_idの生成（identification_idがなければuuid）
        import uuid
        friend_child_user_id = identification_id or str(uuid.uuid4())

        # 親ID取得
        parent_id = session.get('uid')

        # DB保存
        try:
            Child.create(child_user_name, email, hashed_password, friend_child_user_id, parent_id)
            flash('子どもアカウントを追加しました')
            return redirect(url_for('parent_dashboard'))
        except Exception as e:
            flash(f'登録に失敗しました: {e}')
            return render_template('parent/child/add.html', identification_id=identification_id, child_user_name=child_user_name, email=email)

    return render_template('parent/child/add.html')

@app.route('/parent/child/status/', methods=['POST'])
def update_child_time():
    child_id = request.form.get('child_id')
    status = request.form.get('child_status')
    # DBの状態を更新
    Child.update_status(child_id, status)
    flash('子どもアカウントの状態を更新しました')
    return redirect(url_for('parent_dashboard'))

@app.route('/parent/child/delete/', methods=['POST'])
def delete_child():
    child_id = request.form.get('child_id')
    print(f"子どもID={child_id}")
    return redirect(url_for('parent_dashboard'))

@app.route('/child/dashboard',methods=['GET'])
def child_home():
    if 'uid' not in session or session.get('user_type') != 'child':
        flash('ログインしてください')
        return redirect(url_for('login'))
    child = Child.find_by_id(session['uid'])
    return render_template('child/home.html', child=child)

#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)