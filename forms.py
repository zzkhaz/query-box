# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length, Email, Regexp, DataRequired,EqualTo

#登录表单
class Login(Form):
    name=StringField('用户名',validators=[DataRequired(message=u"用户名不能为空")
        ,Length(6,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入用户名'})
    pwd=PasswordField('密码',validators=[DataRequired(message=u"密码不能为空")
        ,Length(6,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入密码'})
    submit = SubmitField(label=u'提交')
    
#注册表单
class Register(Form):
    name=StringField('用户名',validators=[DataRequired(message=u"用户名不能为空")
        ,Length(6,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入用户名'})
    pwd=PasswordField('密码',validators=[DataRequired(message=u"密码不能为空")
        ,Length(6,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入密码'})
    repwd=PasswordField('确认密码',validators=[DataRequired(message=u"密码不能为空")
        ,Length(6,20,message=u'长度位于10~20之间'),EqualTo('pwd', message=u'密码必须一致')],render_kw={'placeholder':u'再次输入密码'})
    submit=SubmitField(label=u'注册')