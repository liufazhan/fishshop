from app.models.base import db,Base
from sqlalchemy import Column,Boolean,String,Integer,ForeignKey,desc,func
from sqlalchemy.orm import relationship
from flask import current_app
from app.spider.yushu_book import YuShuBook



class Gift(Base):
    id=Column(Integer,primary_key=True)
    # 和User模型做关联使用relationship
    user = relationship('User')
    uid = Column(Integer,ForeignKey('user.id'))
    isbn=Column(String(15),nullable=False)
    launched=Column(Boolean,default=False)

    # 获取用户礼物
    @classmethod
    def get_user_gifts(cls,uid):
        gifts=Gift.query.filter_by(uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    # 获取用户每个请求礼物数量
    @classmethod
    def get_wish_count(cls,isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn,到wish表中检索出相应的礼物，并且计算出某个礼物
        # 的wish心愿清单数量
        # 计算出来的数量并不是一个而是每一个礼物的数量
        # 一组数量
        # 使用mysql的 in查询
        # 根据isbn来区分wish的数量,
        # 我们使用Gift.query查询的是一个个具体的模型，而使用db.session是查询的模型的数量，因此使用db.session.query.filter()
        # filter中使用的条件表达式
        count_list=db.session.query(func.count(Wish.id),Wish.isbn).filter(Wish.launched==False,
                                                               Wish.isbn.in_(isbn_list),
                                                               Wish.status==1).group_by(
            Wish.isbn).all()
        # 直接返回列表或者元组到外部这种不好
        # 我们可以使用返回对象或者字典的形式
        # 如若跨模型查询操作数据可以db.session的查询方式
        count_list = [{'count':w[0], 'isbn':w[1]} for w in count_list]
        return count_list


    # 获取书籍数据可以通过isbn 去搜寻
    @property
    def book(self):
        yushu_book=YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
    # 对象代表一个礼物，是具体的
    # 类是代表礼物这个事物，是抽象的，不是具体的一个，是代表一类事物。
    # 实例方法是和对象对应的，而类的方法是和类对应的。
    # 因此recent这个方法不应当看做一个具体的礼物
    @classmethod
    def recent(cls):
        # 链式调用的特征：
        # 首先存在主体 query
        # 其次存在子函数，特点是子函数最终都会返回主体 query
        # 最后链式调用中都要存在一个触发条件，例如：first()或all()
        recent_gift=Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).limit(current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift