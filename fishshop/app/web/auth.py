from . import web
from app.models.base import db
from flask import render_template,request,redirect,url_for,flash
from app.models.user import User
from app.forms.auth import RegisterForm, LoginForm
from flask_login import login_user,logout_user

# from werkzeug.security import generate_password_hash

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    #使用request.form来处理请求数据
    form = RegisterForm(request.form)
    # 判断是否是注册（request method='POST'），若是则调用User模型，写入注册信息
    if request.method == 'POST' and form.validate():
        user = User()
        # form.data包含客户端提交过来的所有数据
        user.set_attrs(form.data)
        #操作模型ORM，将注册信息提交到数据库表中
        with db.auto_commit():
            db.session.add(user)
       # db.session.commit()
        # user.password=generate_password_hash(form.password.data)
        # 使用 redirect 去重定向 要使用return返回
        return redirect(url_for('web.login'))

    return render_template('auth/register.html', form=form)



@web.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm(request.form)
    if request.method=='POST' and form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        print(form.password.data)
        if user and user.check_password(form.password.data):
            # 使用flask_login 引入login_user
            login_user(user, remember=True)
            # 登录完成之后跳转回当前访问页面
            next1=request.args.get('next')
            # 判断next 是否存在 以及是否以 ‘/’开头
            if not next1 or not next1.startswith('/'):
                next1=url_for('web.index')
            return redirect(next1)
        else:
            flash('账号不存在，或密码错误')

    return render_template('auth/login.html',form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass

# 使用 logout_user()退出系统
@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
