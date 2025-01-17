from . import web
from app.models.base import db
from flask_login import login_required,current_user
from flask import current_app
from app.models.wish import Wish
from flask import flash,render_template,url_for,redirect
from app.view_models.wish import MyWishes

__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    uid=current_user.id
    wishes_of_mine=Wish.get_user_wishes(uid)
    isbn_list=[wish.isbn for wish in wishes_of_mine]
    gift_count_list=Wish.get_gift_count(isbn_list)
    # 获取解析后的数据，渲染到模板中
    view_model=MyWishes(wishes_of_mine,gift_count_list)
    return render_template('my_wish.html',wishes=view_model.gifts)



@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish=Wish()
            wish.uid=current_user.id
            wish.isbn=isbn
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或者你的心愿清单，请勿重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))





@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
