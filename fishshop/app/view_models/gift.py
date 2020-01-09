from .book import BookViewModel
from collections import namedtuple

# 使用 namedtuple
# MyGift=namedtuple('MyGift',['id','book','wish_counts'])
# 首先实例化一个类用于表示礼物清单

class MyGifts:
    def __init__(self,gifts_of_mine,wish_count_list):
        self.gifts=[]
        self.gifts_of_mine=gifts_of_mine
        self.wish_count_list=wish_count_list
        self.gifts=self.__parse()

    def __parse(self):
        # 修改实例变量时我们不可以直接修改我们的实例变量，
        # 可以通过定义我们的中间变量来实现修改
        temp_gifts=[]
        for gift in self.gifts_of_mine:
            my_gift=self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self,gift):
        # 读取实例变量我们可以直接引用
        count=0
        for wish_count in self.wish_count_list:
            if gift.isbn==wish_count['isbn']:
                count=wish_count['count']
        r={
            'id':gift.id,
            'wishes_count':count,
            'book':BookViewModel(gift.book)
        }
        return r
        #my_gift=MyGift(gift.id,BookViewModel(gift.book),count)
        #return my_gift
