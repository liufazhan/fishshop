from flask import jsonify,request,render_template,flash
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookViewModel, BookCollection
from app.web import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from app.view_models.trade import TradeInfo
from flask_login import current_user



# @web.route("/book/search/<q>/<page>")
# def search(q,page):
@web.route("/book/search")
def search():
    """
        q:普通关键字和isbn
        page
    :return:
    """
    # ?方式连接参数，使用request方式
    # 查询关键字参数要求必须要大于0，最长不能超过30个字符
    # q = request.args['q']

    # page参数，必须要有值，且是正整数，长度限制
    # page = request.args['page']
    # 将不可变的字典转化为可变的字典
    # a=request.args.to_dict()

    #引入验证层
    form = SearchForm(request.args)
    books = BookCollection()

    #调用form.validate引用校验
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book=YuShuBook()

        if isbn_or_key == 'isbn':
            # alt+enter快捷键导入模块
            yushu_book.search_by_isbn(q)
            books.fill(yushu_book,q)
            # result = BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q,page)
            books.fill(yushu_book,q)
            # result = YuShuBook.search_by_keyword(q, page)
            # result = BookViewModel.package_collection(result, q)
        # dict 序列化
        # json.dumps() 返回的是： Content-Type:text/html
        # jsonify() 返回的是：Content-Type: application/json
        #改写后的功能 __dict__内置字典
        #return json.dumps(books, default=lambda o:o.__dict__)
        # return jsonify(result)
        # return json.dumps(result),200,{'content-type':'application/json'}
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        #return jsonify(form.errors)
    return render_template('search_result.html',books=books,form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 要想判断书籍是否在赠送或者心愿清单中，先对其赋初始值
    has_in_gifts=False
    has_in_wishes=False

    # 获取书籍详情页面
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    # 首先判断用户是否登录系统，可以使用is_authenticated插件
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,
                                isbn=isbn,launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id,
                                isbn=isbn,launched=False).first():
            has_in_wishes = True
    # 查询包含所有赠送者的信息
    trade_gifts = Gift.query.filter_by(isbn=isbn,launched=False).all()
    #查询包含所有索要者的清单
    trade_wishes=Wish.query.filter_by(isbn=isbn,launched=False).all()

    # 查询数据传入到TradeInfo视图模型中处理数据
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)


    return render_template('book_detail.html',book=book,
                           wishes=trade_wishes_model,gifts=trade_gifts_model,
                           has_in_wishes=has_in_wishes,has_in_gifts=has_in_gifts)


