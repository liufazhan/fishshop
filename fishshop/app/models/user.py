from app.models.base import db,Base
from sqlalchemy import Column,Integer,Boolean,String,Float
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.web.book import YuShuBook
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish


class User(UserMixin,Base):
    id=Column(Integer,primary_key=True,autoincrement=True)
    nickname=Column(String(24),nullable=False)
    phone_number=Column(String(18),unique=True)
    email=Column(String(50),unique=True,nullable=False)
    confirmed=Column(Boolean,default=False)
    _password=Column('password',String(128))
    beans=Column(Float,default=0)
    send_counter=Column(Integer,default=0)
    receive_counter=Column(Integer,default=0)
    wx_open_id=Column(String(50))
    wx_name=Column(String(32))

    # python动态赋值
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            # 使用内置函数判断值是否在字典中存在
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def password(self):
        return self._password
    #使用setter方法来预先处理数据
    @password.setter
    def password(self,raw):
        self._password=generate_password_hash(raw)

    def check_password(self,raw):
        print(raw)
        return check_password_hash(self._password,raw)

    def can_save_to_list(self,isbn):
        # 首先判断搜索关键字是否是isbn,如果是则传入isbn号去搜索图书
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book=YuShuBook()
        yushu_book.search_by_isbn(isbn)
        # 如果输入的isbn编号在网站不存在则报错，存在则通过,查询出来再多也只取第一条数据返回
        if not yushu_book.first:
            return False
        # 同时还要判断当前用户不能既是赠书者又索要者。
        # 判断思路为：当前用户是否存在未赠送出去的赠书，存在且状态为未赠送出状态则不允许再次添加到赠书清单中。
        # 当前用户赠送该数已存在赠送清单中，就不允许再次添加到索要清单
        gifting=Gift.query.filter_by(isbn=isbn,uid=self.id,
                                     launched=False).first()
        wishing=Wish.query.filter_by(uid=self.id,isbn=isbn,
                                     launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False





    #在User模型中写flask特有的get_id()方法来写入cookie或者可以引用usermixin,使用USER模型继承usermixin
    # def get_id(self):
    #     return self.id


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
