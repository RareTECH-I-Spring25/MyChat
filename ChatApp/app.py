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
        
        
        try:
            import uuid
            uid = str(uuid.uuid4())
            User.create(uid, parent_user_name, email, password)
            flash('アカウント登録が完了しました。ログインしてください。')
            return redirect(url_for('login'))
        except ValueError as ve:
            flash(str(ve))
            return render_template('auth/signup-parent.html', email=email, parent_user_name=parent_user_name)
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

    # 仮のデータを設定（後でデータベースから取得する実装に変更する）
    parent = {
        'parent_id': 1,
        'parent_user_name': '山田太郎'
    }
    
    children = [
        {'child_id': 1, 'child_user_name': '山田はな', 'child_status': 1},
        {'child_id': 2, 'child_user_name': '山田けん', 'child_status': 0}
    ]
    
    return render_template('parent/home.html', parent=parent, children=children)


#サンプルソースです。childrenをフロントへ渡していただくと子供リストが生成されます。削除いただいて大丈夫です。 by fuku
# @app.route('/parent/dashbord',methods=['GET'])
# def parent_dashbord():
#     parent=[
# 		{'parent_id':1,'parent_user_name':'山田太郎'}
# 	]
#     children=[
# 		{'child_id':1,'child_user_name':'山田はな','child_status':1},
# 		{'child_id':2,'child_user_name':'山田けん','child_status':0},
# 	]
#     return render_template('parent/home.html',parent=parent[0],children=children)

@app.route('/parent/child/add',methods=['GET','POST'])
def add_child():
	if request.method == 'POST':
		identification_id = request.form.get('identification_id')
		child_user_name = request.form.get('child_user_name')
		email = request.form.get('email')
		password = request.form.get('password')
		password_confirmation = request.form.get('password_confirmation')
		print(f"ログイン試行: identification_id={identification_id}, child_user_name={child_user_name}, email={email}, password={password}, password_confirmation={password_confirmation}")
		return render_template('parent/child/add.html',identification_id=identification_id,child_user_name=child_user_name,email=email)

	return render_template('parent/child/add.html')

@app.route('/parent/child/status/', methods=['POST'])
def update_child_time():
    child_id = request.form.get('child_id')
    status = request.form.get('status')
    flash('子どもアカウントの状態を更新しました')
    return redirect(url_for('parent_dashboard'))

@app.route('/parent/child/delete/', methods=['POST'])
def delete_child():
    child_id = request.form.get('child_id')
    print(f"子どもID={child_id}")
    return redirect(url_for('parent_dashbord'))

@app.route('/child/dashboard',methods=['GET'])
def child_home():
    return render_template('child/home.html')

#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)