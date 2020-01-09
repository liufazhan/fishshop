from wtforms import Form,StringField,PasswordField
from wtforms.validators import Length,DataRequired,Email,ValidationError
from app.models.user import User



class RegisterForm(Form):
    email = StringField(validators=[DataRequired(),Length(8,64),Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入密码'),Length(6,32)])
    nickname = StringField(validators=[DataRequired(), Length(2,10,message='昵称至少为两个字符，最多为10个字符')])

    def validate_email(self,field):
        # filter_by根据查询条件来查询，通过first()方法来触发
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
    def validate_nickname(self,field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已被注册')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入密码'), Length(6, 32)])


