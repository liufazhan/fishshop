from app.models.wish import Wish
from app.models.gift import Gift
from app.models.base import db
from flask import flash,redirect,url_for,render_template

from app.view_models.gift import MyGifts
from . import web
# 引入flask_login 模块的login_required方法
from flask_login import login_required,current_user
from flask import current_app
__author__ = '七月'

# 使用装饰器方法要求访问该视图函数必须登录
# 要想展示我的礼物中有多少人想要，首先要实现查询我的礼物，取出Gift数据库表中的我要赠送的礼物，
# 然后将赠送的礼物的isbn编号加入到isbn列表中组成一个列表，然后再去wish表中查询isbn有多少在isbn列表中
@web.route('/my/gifts')
@login_required
def my_gifts():
    uid=current_user.id
    gifts_of_mine=Gift.get_user_gifts(uid)
    isbn_list=[gift.isbn for gift in gifts_of_mine]
    wish_count_list=Gift.get_wish_count(isbn_list)
    view_model=MyGifts(gifts_of_mine,wish_count_list)
    return render_template('my_gifts.html',gifts=view_model.gifts)



@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # 事务回滚，如果添加数据库事务提交失败后，执行数据回滚
    if current_user.can_save_to_list(isbn):
        #try:
        with db.auto_commit():
            gift=Gift()
            gift.isbn=isbn
            gift.uid=current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
        #    db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     # 把异常抛出去
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或你的心愿清单，请不要重复添加')

    return redirect(url_for('web.book_detail',isbn=isbn))



@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



