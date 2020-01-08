from flask_wtf import Form, FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators

class PerformerForm(FlaskForm):
    id = HiddenField()

    name = StringField("Ім'я виконавця: ", [
        validators.DataRequired("Це поле є обов'язковим."),
        validators.Length(3, 15, "Ім'я має містити від 3 до 15 символів.")
    ])

    submit = SubmitField("Зберегти")