from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, SelectField
from wtforms import validators

class MelodyForm(FlaskForm):

    id = HiddenField()

    title = StringField("Назва: ", [
        validators.DataRequired("Введіть назву мелодії."),
        validators.Length(3, 15, "Назва має містити від 3 до 15 символів.")
    ])

    singer = SelectField("Виконавець: ", [
        validators.data_required("Це поле є обов'язковим.")
    ],
                                  choices=[], coerce=str)
    release_date = DateField("Дата релізу: ", [validators.data_required("Це поле є обов'язковим.")])

    melody_genre = SelectField("Жанр: ", [
        validators.data_required("Це поле є обов'язковим.")
    ],
                                  choices=[], coerce=str)
    album = SelectField("Альбом: ", [
        validators.data_required("Це поле є обов'язковим.")
    ],
                                  choices=[], coerce=str)

    submit = SubmitField("Зберегти")