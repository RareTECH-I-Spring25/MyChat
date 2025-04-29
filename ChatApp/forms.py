from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from models import User  

# 保護者の登録
class ParentRegistrationForm(FlaskForm):
    parent_user_name = StringField('ユーザー名', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード', validators=[
    DataRequired(message='パスワードを入力してください。'),
    Length(min=6, message='パスワードは6文字以上で入力してください。')
])
    password_confirmation = PasswordField('パスワード（確認用）', validators=[
        DataRequired(), EqualTo('password', message='パスワードが一致しません')
    ])
    submit = SubmitField('ログイン')

# 子どもアカウントの登録
class ChildRegistrationForm(FlaskForm):
    child_user_name = StringField('ユーザー名', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('パスワード', validators=[
    DataRequired(message='パスワードを入力してください。'),
    Length(min=6, message='パスワードは6文字以上で入力してください。')
])
    password_confirmation = PasswordField('パスワード（確認用）', validators=[
        DataRequired(), EqualTo('password', message='パスワードが一致しません')
    ])
    submit = SubmitField('ログイン')
    
    
#親子ログイン用設定    
class LoginForm(FlaskForm):
    user_type = SelectField('アカウント種類', choices=[('parent', '親'), ('child', '子供')], validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')