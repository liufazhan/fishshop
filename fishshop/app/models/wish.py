from app.models.base import db,Base
from sqlalchemy import Column,Boolean,String,Integer,ForeignKey,desc,func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook



class Wish(Base):
    id=Column(Integer,primary_key=True)
    # 和User模型做关联使用relationship
    user = relationship('User')
    uid = Column(Integer,ForeignKey('user.id'))
    isbn=Column(String(15),nullable=False)
    launched=Column(Boolean,default=False)

    @property
    def book(self):
        yushu_book=YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls,uid):
        wishes=Wish.query.filter_by(uid=uid,launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_count(cls,isbn_list):
        # 循环导入解决方法，在哪调用的在哪导入
        from app.models.gift import Gift
        count_list=db.session.query(func.count(Gift.id),Gift.isbn).filter(
            Gift.launched==False,Gift.isbn.in_(isbn_list)).group_by(
            Gift.isbn).all()
        count_list=[{'count':w[0],'isbn':w[1]} for w in count_list]
        return count_list

