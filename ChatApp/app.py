from flask import Flask, render_template
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

@app.route('/post/<int:post_id>/<post_name>')
def show_post(post_id, post_name):
    post = posts[post_id]
    return f"{post} {post_name}"

@app.route('/hello/<string:user_name01>/<string:user_name02>')
def hekko(user_name01, user_name02):
    return f"こんにちは {user_name01}さん {user_name02}さん"

@app.route('/add/<int:num1>/<int:num2>')
def add(num1, num2):
    return f"{num1} + {num2} = {num1 + num2}"

@app.route('/div/<float:num1>/<float:num2>')
def div(num1, num2):
    return f"{num1} / {num2} = {num1 // num2}"

@app.route('/user/<string:user_name>/<int:user_number>')
def show_user(user_name, user_number):
    user_name = user_name.upper()
    return f"Hello {user_name} {user_number}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', port=5001, debug=True)