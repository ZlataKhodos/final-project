from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  PasswordField, HiddenField
from wtforms.validators import InputRequired, Length, regexp


class userlogin(FlaskForm):

    id = HiddenField()

    login = StringField('Нікнейм в Телеграм', validators = [InputRequired()])

    password = PasswordField('Пароль', validators = [InputRequired()])

    submit = SubmitField('Увійти')