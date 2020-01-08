from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, SelectField
from wtforms import validators

class OrderForm(FlaskForm):
    id=HiddenField()

    username = StringField("Юзернейм: ", [
        validators.DataRequired("Це поле є обов'язковим"),
        validators.Length(3, 36, "Юзернейм має містити від 3 до 36 символів"),
        validators.regexp('@([a-z]*|[A-Z]*|_*|[0-9]*)*', message= "Починайте ввід із символу @")])

    date = DateField("Дата замовлення: ", [validators.data_required("Це поле є обов'язковим.")])

    criteria = SelectField("Критерій замовлення: ",[validators.data_required("Це поле є обов'язковим.")], choices=[])

    value = StringField("Значення замовлення: ", [validators.data_required("Це поле є обов'язковим.")])

    submit=SubmitField("Замовити")