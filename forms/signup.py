from flask_wtf import FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators

class SignUpForm(FlaskForm):
    id = HiddenField()

    faculty = StringField("Факультет: ", [
        validators.DataRequired("Це поле є обов'язковим"),
        validators.Length(2, 15, "Довжина має бути від 2 до 15 символів")
    ])

    name = StringField("Ім'я: ", [
        validators.DataRequired("Це поле є обов'язковим"),
        validators.Length(3, 15, "Ім'я має містити від 3 до 15 символів")
    ])

    surname = StringField("Прізвище: ", [
        validators.DataRequired("Це поле є обов'язковим"),
        validators.Length(3, 15, "Прізвище має містити від 3 до 15 символів")
    ])

    username = StringField("Юзернейм: ", [
        validators.DataRequired("Це поле є обов'язковим"),
        validators.Length(3, 36, "Юзернейм має містити від 3 до 36 символів"),
        validators.regexp('@([a-z]*|[A-Z]*|_*|[0-9]*)*', message= "Починайте ввід із символу @")
    ])

    password = PasswordField("Пароль", [validators.DataRequired("Це поле є обов'язковим"),
        validators.Length(3, 36, "Юзернейм має містити від 3 до 36 символів")])

    submit = SubmitField("Зберегти")