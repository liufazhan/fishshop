from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length,NumberRange,DataRequired



class SearchForm(Form):
    #使用validate数组对象可以传入多个参数
    q=StringField(DataRequired(),validators=[Length(min=1,max=30)])
    page=IntegerField(validators=[NumberRange(min=1,max=99)],default=1)