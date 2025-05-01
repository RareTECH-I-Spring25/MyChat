from flask import Flask, render_template, request, flash, redirect, url_for
import logging
from flask import session
from models import db_pool, User

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


@app.route("/")
def index():
    return render_template("auth/login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"ログイン試行: ユーザー種別={user_type}, メールアドレス={email}, パスワード={password}")
        session['uid'] = '仮のユーザーID'
        session['user_type'] = user_type
        
        if not email or not password:
            flash('メールアドレスとパスワードを入力してください')
            return redirect(url_for('login'))
        
        if user_type == 'parent':
            return redirect(url_for('parent_dashboard'))
        elif user_type == 'child':
            return redirect(url_for('child_home'))
        
    return render_template('auth/login.html')

@app.route('/signup/parent', methods=['GET', 'POST'])
def signup_parent():
    email = ''
    parent_user_name = ''
    
    if request.method == 'POST':
        email = request.form.get('email')
        parent_user_name = request.form.get('parent_user_name')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        user_type = request.form.get('user_type')
        
        if not email or not password:
            flash('メールアドレスとパスワードを入力してください')
            return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)
        
        # ここでDBにユーザーを登録
        try:
            import uuid
            uid = str(uuid.uuid4())
            User.create(uid, parent_user_name, email, password)
            flash('アカウント登録が完了しました。ログインしてください。')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'登録に失敗しました: {e}')
            return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)
        
    return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)

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

@app.route('/parent/child/add',methods=['GET','POST'])
def add_child():
    return render_template('parent/child/add.html')




@app.route('/child/dashboard',methods=['GET'])
def child_home():
    return render_template('child/home.html')


#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)