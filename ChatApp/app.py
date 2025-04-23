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

@app.route('/')
def hello():
    return "Hello"


posts = {
    1:"post-1",
    2:"post-2",
    3:"post-3"
}

#えすえす追加

registered_emails = set() #データベースの設定が完了すれば必ず消してMYSQLと対応させるコードを書くこと

@app.route('/signup/parent', methods=['GET', 'POST'])
def signup_parent():
    form = ParentRegistrationForm()
    if form.email.data in registered_emails:
        flash('このメールアドレスは既に登録されています。', 'error')
        return render_template('signup_parent.html', form=form)

    if form.validate_on_submit():
        registered_emails.add(form.email.data)
        flash('保護者用アカウントの登録が完了しました！ログインしてください。', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup_parent.html', form=form)

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



#えすえす追加終了



#実行処理
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)