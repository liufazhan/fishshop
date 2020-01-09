# 改写
class BookViewModel:
    def __init__(self,book):
        self.title=book['title']
        self.publisher=book['publisher'] or ''
        self.pages=book['pages']
        self.author='、'.join(book['author'])
        self.price=book['price']
        self.isbn=book['isbn']
        self.pubdate=book['pubdate']
        self.binding=book['binding']
        self.summary=book['summary'] or ''
        self.image=book['image']


class BookCollection:
    def __init__(self):
        self.total=0
        self.keyword=''
        self.books=[]
    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


# class BookViewModel:
#     # 面向对象的描述特征 （包含类变量、实例变量）
#     #行为（方法）
#     #面向过程
#     @classmethod
#     def package_single(cls,data,keyword):
#         returned={
#             'books':[],
#             'total':0,
#             'keyword':keyword
#         }
#         if data:
#             returned['total']=0
#             returned['books']=[cls.__cut_book_data(data)]
#         return returned
#         pass
#     @classmethod
#     def package_collection(cls,data,keyword):
#         returned={
#             'books':[]
#             'total':0
#             'keyword':keyword
#         }
#         if data:
#             returned['total']=data['total']
#             returned['books']=[cls.__cut_book_data(book) for book in data['books']]
#         return returned
#         pass
#
#     @classmethod
#     def __cut_book_data(cls,data):
#         book={
#             'title':data['title'],
#             'publisher':data['publisher'] or '',
#             'pages':data['pages'],
#             'author':'、'.join(data['author']),
#             'price':data['price'],
#             'summary':data['summary'] or '',
#             'image':data['image']
#         }
#         return book
#         pass