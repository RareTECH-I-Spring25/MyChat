from flask import Flask, render_template, request, flash, redirect, url_for
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'secret_key' 

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
    print(f"ログアウトしました")
    return redirect(url_for('login'))

#以下、変数を/parent/dashbordに渡していただくとhtmlが生成されます。削除いただいて問題ないです。
# @app.route('/parent/dashbord',methods=['GET'])
# def parent_dashbord():
#     children=[
# 		{'child_id':1,'child_user_name':'山田はな','child_status':1},
# 		{'child_id':2,'child_user_name':'山田けん','child_status':0},
# 	]
#     return render_template('parent/home.html',children=children)

@app.route('/parent/child/add',methods=['GET','POST'])
def add_child():
    return render_template('parent/child/add.html')

@app.route('/parent/child/status/', methods=['POST'])
def update_child_time():
    child_id = request.form.get('child_id')
    child_status = request.form.get('child_status')
    print(f"子どもID={child_id}, status={child_status}")
    return redirect(url_for('parent_dashbord'))

@app.route('/parent/child/delete/', methods=['POST'])
def delete_child():
    child_id = request.form.get('child_id')
    print(f"子どもID={child_id}")
    return redirect(url_for('parent_dashbord'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)