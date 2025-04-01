from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, TelField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

    # password2를 잘못 입력 하였을 때 비밀번호를 다시 확인해 주세요. 란 문구가 뜨는 문제가 발생 
class UserCreateForm(FlaskForm):
    username = StringField('사용자 ID를 작성해 주세요.', validators=[DataRequired(), Length(min=1, max=25)])
    password1 = PasswordField('비밀번호를 확인해 주세요', validators=[DataRequired(), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인을 작성해 주세요.', validators=[DataRequired()])
    email = EmailField('이메일을 작성해 주세요.', validators=[DataRequired(), Email()])
    tell = TelField('전화번호는 최대 15자 까지 입력 가능 합니다.', validators=[Length(max=15)])
    address = StringField('주소는 3000자 이하로 작성해 주세요.', validators=[Length(max=3000)])
    postcode = StringField('우편번호는 최대 5자 까지 입력 가능합니다.', validators=[Length(max=5)])
    
class UserLoginForm(FlaskForm):
    username = StringField('사용자 ID을 작성해 주세요', validators=[DataRequired(), Length(min=1, max=25)])
    password = PasswordField('비밀번호를 작성해주세요', validators=[DataRequired()])

class UpdateForm(FlaskForm):
    username = StringField('사용자 ID를 입력해주세요', validators=[DataRequired()])
    password = PasswordField('비밀번호를 입력해주세요', validators=[DataRequired()])
    email = EmailField('이메일을 입력해주세요', validators=[DataRequired(), Email()])
    tell = TelField('전화번호는 최대 15자 까지 입력 가능 합니다.', validators=[Length(max=15)])
    address = StringField('주소는 3000자 이하로 작성해 주세요.', validators=[Length(max=3000)])
    postcode = StringField('우편번호는 최대 5자 까지 입력 가능합니다.', validators=[Length(max=5)])
    submit = SubmitField('Update')
