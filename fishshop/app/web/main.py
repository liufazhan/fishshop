from . import web
from app.models.gift import Gift
from app.view_models.book import BookViewModel
from flask import render_template


__author__ = '七月'


@web.route('/')
def index():
    # 获取上传的书籍数据
    recent_gifts=Gift.recent()
    # 获取的上传的书籍礼物是以书籍数据展示的，如何获取书籍的数据可以使用书籍礼物列表中的书籍的isbn编号
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)



@web.route('/personal')
def personal_center():
    pass
