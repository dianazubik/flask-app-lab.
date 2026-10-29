
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Введіть ім'я"),
            Length(min=4, max=10, message="Ім'я має містити від 4 до 10 символів")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email"),
            Email(message="Введіть правильну email-адресу")
        ]
    )

    phone = StringField(
        "Phone",
        validators=[
            Regexp(
                r"^\+380\d{9}$",
                message="Формат телефону: +380XXXXXXXXX"
            )
        ]
    )

    subject = SelectField(
        "Subject",
        choices=[
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("other", "Інше")
        ],
        validators=[DataRequired(message="Оберіть тему")]
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Введіть повідомлення"),
            Length(max=500, message="Максимум 500 символів")
        ]
    )

    submit = SubmitField("Send Message")
 