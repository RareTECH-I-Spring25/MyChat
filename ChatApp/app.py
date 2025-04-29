from flask import Flask, render_template, request, flash, redirect, url_for
import logging
from flask import session

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login'))
    return redirect(url_for('parent_dashbord'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"ログイン試行: ユーザー種別={user_type}, メールアドレス={email}, パスワード={password}")
        
        if not email or not password:
            flash('メールアドレスとパスワードを入力してください')
            return redirect(url_for('login'))
            
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
        print(f"ログイン試行: メールアドレス={email}, ユーザー名={parent_user_name}, パスワード={password}, パスワード（確認用）={password_confirmation}")
        
        if not email or not password:
            flash('メールアドレスとパスワードを入力してください')
            return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)
        
    return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)

@app.route('/logout', methods=['POST'])
def logout():
    flash('ログアウトしました')
    return redirect(url_for('login'))

@app.route('/parent/dashbord',methods=['GET'])
def parent_dashbord():
    return render_template('parent/home.html')

@app.route('/parent/child/add',methods=['GET','POST'])
def add_child():
    return render_template('parent/child/add.html')

@app.route('/parent/child/time/', methods=['POST'])
def update_child_time():
    child_id = request.form.get('child_id')
    status = request.form.get('status')
    print(f"子どもID={child_id}, status={status}")
    return render_template('parent/home.html')

#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)