from .book import BookViewModel


class MyWishes:
    def __init__(self,gifts_of_mine,wish_count_list):
        self.gifts=[]
        self.__gifts_of_mine=gifts_of_mine
        self.__wish_count_list=wish_count_list
        self.gifts=self.__parse()

    def __parse(self):
        # 修改实例变量时我们不可以直接修改我们的实例变量，
        # 可以通过定义我们的中间变量来实现修改
        temp_gifts=[]
        for gift in self.__gifts_of_mine:
            my_gift=self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self,gift):
        # 读取实例变量我们可以直接引用
        count=0
        for wish_count in self.__wish_count_list:
            if gift.isbn==wish_count['isbn']:
                count=wish_count['count']
        r={
            'id':gift.id,
            'wishes_count':count,
            'book':BookViewModel(gift.book)
        }
        return r
