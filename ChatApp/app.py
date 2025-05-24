from flask import Flask, render_template, request, flash, redirect, url_for
import logging
from flask import session
from models import db_pool, User, Child
from models import Friends
import sys
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.secret_key = 'your_secret_key' 
#csrf = CSRFProtect(app) htmlファイルを書き換えるまでコメントオフ
csrf = CSRFProtect(app)
#formタグのすぐ直下に<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">と記述
#GETメソッドのときは不要
#POSTメソッドのみに書く


#Cokie設定！
app.config['SESSION_COOKIE_SECURE'] = False  #Trueにしない
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

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
        if password and len(password) < 8:
            errors.append("パスワードは8文字以上で入力してください")

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
        if password and len(password) < 8:
            errors.append("パスワードは8文字以上で入力してください")

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
    flash('ログアウトしました', 'info')
    return redirect(url_for('login'))

@app.route('/parent/dashboard', methods=['GET'])
def parent_dashboard():
    if 'uid' not in session or session.get('user_type') != 'parent':
        flash('ログインしてください', 'info')
        return redirect(url_for('login'))

    parent = User.find_by_id(session['uid'])
    # DBから子どもリストを取得
    children = Child.find_by_parent_id(session['uid'])
    return render_template('parent/home.html', parent=parent, children=children)

@app.route('/child/add', methods=['GET', 'POST'])
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
        elif len(password) < 8:
            errors.append("パスワードは8文字以上で入力してください")

        if not password_confirmation:
            errors.append("パスワード確認は必須です")

        if password and password_confirmation and password != password_confirmation:
            errors.append("パスワードが一致しません")

        if errors:
            for error in errors:
                flash(error)
            return render_template('parent/child/add.html', identification_id=identification_id, child_user_name=child_user_name, email=email)



        # friend_child_user_idの生成（identification_idがなければuuid）
        import uuid
        friend_child_user_id = identification_id or str(uuid.uuid4())

        # 親ID取得
        parent_id = session.get('uid')

        # DB保存
        try:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash(password)
            Child.create(child_user_name, email, hashed_password, friend_child_user_id, parent_id)
            flash('子どもアカウントを追加しました', 'info')
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
    flash('子どもアカウントの状態を更新しました', 'info')
    return redirect(url_for('parent_dashboard'))

@app.route('/parent/child/delete/', methods=['POST'])
def delete_child():
    child_id = request.form.get('child_id')
    if child_id:
        Child.delete(child_id)
        flash('子どもアカウントを削除しました', 'info')
    else:
        flash('子どもIDが指定されていません')
    return redirect(url_for('parent_dashboard'))



#子どものログイン処理
@app.route('/child/dashboard',methods=['GET'])
def child_home():
    if 'uid' not in session or session.get('user_type') != 'child':
        flash('ログインしてください')
        return redirect(url_for('login'))
    child = Child.find_by_id(session['uid'])
    friends = Friends.get_friends(session['uid'])
    return render_template('child/home.html', child=child, friends=friends)

#子どもの友達検索処理
@app.route('/child/friends/search', methods=['POST'])
def search_friends():
    if 'uid' not in session or session.get('user_type') != 'child':
        flash('ログインしてください')
        return redirect(url_for('login'))

    identification_id = request.form.get('identification_id')
    if not identification_id:
        flash('検索IDを入力してください')
        return render_template('child/friends/add.html')

    # 自分自身のIDで検索していないかチェック
    child = Child.find_by_id(session['uid'])
    if child['friend_child_user_id'] == identification_id:
        flash('自分のIDは検索できません')
        return render_template('child/friends/add.html')

    # 友達を検索
    friend = Friends.find_by_friend_child_user_id(identification_id)
    if not friend:
        flash('該当する友だちが見つかりません')
        return render_template('child/friends/add.html')

    # 既に友達関係にあるかチェック
    if Friends.is_friend_exists(session['uid'], identification_id):
        flash('すでに友だちに追加されています')
        return render_template('child/friends/add.html')

    return render_template('child/friends/add.html', results=[friend])

#子どもの友達追加処理
@app.route('/child/friends/add', methods=['GET', 'POST'])	
def add_friends():
    if 'uid' not in session or session.get('user_type') != 'child':
        flash('ログインしてください')
        return redirect(url_for('login'))

    if request.method == 'POST':
        child_id = request.form.get('child_id')
        if not child_id:
            flash('友だちを選択してください')
            return render_template('child/friends/add.html')

        # 友達の情報を取得
        friend = Child.find_by_id(child_id)
        if not friend:
            flash('友だちが見つかりません')
            return render_template('child/friends/add.html')

        # チャンネル作成と友達追加
        channel_id = Friends.create_with_channel(session['uid'], friend['friend_child_user_id'])
        if channel_id:
            flash('友だちを追加しました', 'info')
            return redirect(url_for('child_home'))
        else:
            flash('友だちの追加に失敗しました')
            return render_template('child/friends/add.html')

    return render_template('child/friends/add.html')


@app.route('/child/channel/1',methods=['GET'])
def child_channel():
    child_id =1
    friend ='田中たろう'
    messages = [
        {'child_id':1,'message_content':'おはよう'},
        {'child_id':2,'message_content':'今日の待ち合わせ時間12時だったっけ？'},
        {'child_id':1,'message_content':'合ってるよ！'},
        {'child_id':2,'message_content':'ありがとう！'},

    ]
    return render_template('child/chat.html',child_id=child_id,friend=friend,messages=messages)

#子ども友達削除処理
@app.route('/child/friends/delete', methods=['POST'])
def delete_friends():
    friend_id = request.form.get('friend_id')
    print('friend_id:', friend_id)
    if not friend_id:
        flash('友だちIDが指定されていません')
        return redirect(url_for('child_home'))
    try:
        Friends.delete(friend_id)
        flash('友だちを削除しました')
    except Exception as e:
        flash(f'削除に失敗しました: {e}')
    return redirect(url_for('child_home'))

#エラー404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404

#エラー500
@app.errorhandler(500)
def page_not_found(error):
    return render_template('error/500.html'),500

#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)