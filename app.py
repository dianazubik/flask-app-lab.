from flask import Flask, render_template

app = Flask(__name__)


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


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")


if __name__ == '__main__':
    app.run(debug=True)