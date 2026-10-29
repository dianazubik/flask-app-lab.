import logging

from flask import render_template, request, redirect, url_for, flash
from . import app
from .forms import ContactForm

logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

@app.route('/')
@app.route('/resume')
def resume():
    person = {
        "name": "Діана Зубик",
        "photo": "images/profile.jpg",
    }

    about = [
        "Студентка 3-го курсу спеціальності «Інженерія програмного забезпечення» "
        "Карпатського національного університету імені Василя Стефаника. "
        "Захоплююся розробкою сучасних веб-застосунків, проектуванням архітектури "
        "програмного забезпечення та роботою з базами даних.",
        "Постійно вдосконалюю свої навички і вивчаю патерни проектування. Активна, "
        "відповідальна, прагну долучитися до реальних командних проєктів для здобуття "
        "комерційного досвіду.",
    ]

    education = [
        {
            "institution": "Карпатський національний університет імені Василя Стефаника",
            "specialty": "121 «Інженерія програмного забезпечення»",
            "years": "2024 - дотепер",
        },
    ]

    skills = [
        {"title": "Back-end розробка та Front-end розробка",
         "description": "Верстка адаптивних інтерфейсів (HTML, CSS3), основи інтерактивності на JavaScript."},
        {"title": "Бази даних",
         "description": "Проектування БД (MySQL), написання корисних SQL-запитів."},
        {"title": "Проектування ПЗ",
         "description": "Знання ООП (Python, Java, C++), розуміння основних патернів проектування та архітектурних підходів."},
        {"title": "Інструменти розробки",
         "description": "Робота з системою контролю версій Git/GitHub."},
        {"title": "Алгоритми та веб-дизайн",
         "description": "Базове розуміння алгоритмів та структур даних, основи UI/UX дизайну для створення зручних користувацьких інтерфейсів."},
        {"title": "Апаратні основи",
         "description": "Розуміння базових принципів мікроконтролерів та роботи з периферією (Основи робототехніки / C++)."},
    ]

    technologies = [
        {"name": "Python", "badge": "bg-primary"},
        {"name": "Java", "badge": "bg-secondary"},
        {"name": "PHP", "badge": "bg-secondary"},
        {"name": "C++", "badge": "bg-secondary"},
        {"name": "HTML / CSS / JavaScript", "badge": "bg-dark"},
        {"name": "SQL", "badge": "bg-info text-dark"},
        {"name": "Git / GitHub", "badge": "bg-secondary"},
        {"name": "Web-дизайн (Figma)", "badge": "bg-secondary"},
        {"name": "Основи робототехніки (Arduino)", "badge": "bg-secondary"},
    ]

    projects = [
        {"title": "Університетські навчальні проєкти",
         "description": "Розробка навчальних вебзастосунків, створення алгоритмів та "
                        "проєктування баз даних у межах курсових і лабораторних робіт."},
    ]

    return render_template(
        'resume.html',
        title="Резюме",
        person=person,
        about=about,
        education=education,
        skills=skills,
        technologies=technologies,
        projects=projects,
    )



@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            logging.info(
                "Contact form submitted: name=%s, email=%s, "
                "phone=%s, subject=%s, message=%s",
                form.name.data,
                form.email.data,
                form.phone.data,
                form.subject.data,
                form.message.data
            )

            flash("Повідомлення успішно відправлено!", "success")
            return redirect(url_for("contacts"))

        except Exception:
            logging.exception("Error while processing contact form")
            flash("Не вдалося обробити повідомлення.", "danger")
            return redirect(url_for("contacts"))

    return render_template(
        "contacts.html",
        title="Контакти",
        form=form
    )


@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("homepage.html", title="Головна", agent=agent)