
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    SelectField,
    IntegerField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    InputRequired
)


CATEGORIES = [
    ("laptops", "Ноутбуки"),
    ("phones", "Смартфони"),
    ("computers", "Комп'ютери"),
    ("accessories", "Аксесуари"),
]


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву"),
            Length(min=3, message="Мінімум 3 символи")
        ]
    )

    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Введіть опис")
        ]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            InputRequired(message="Введіть ціну"),
            NumberRange(
                min=0.01,
                message="Ціна повинна бути більшою за нуль"
            )
        ]
    )

    category = SelectField(
        "Категорія",
        choices=CATEGORIES,
        validators=[DataRequired(message="Оберіть категорію")]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(message="Введіть кількість"),
            NumberRange(
                min=0,
                message="Кількість не може бути від'ємною"
            )
        ]
    )

    image = FileField(
        "Зображення",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Дозволені лише PNG, JPG та JPEG"
            )
        ]
    )

    submit = SubmitField("Зберегти товар")
 