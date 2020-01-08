from flask_wtf import Form, FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators

class GenreForm(FlaskForm):

    id = HiddenField()

    genre_name = StringField("Назва жанру: ", [
        validators.DataRequired("Введіть, будь ласка, назву жанру."),
        validators.Length(3, 15, "Назва має містити від 3 до 15 символів.")
    ])

    psychotype = StringField("Психотип: ", [
        validators.DataRequired("Введіть, будь ласка, психотип."),
        validators.Length(3, 15, "Назва має містити від 3 до 15 символів.")
    ])

    submit = SubmitField("Зберегти")