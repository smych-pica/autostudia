from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studio.db'
app.config['SECRET_KEY'] = 'secret123'

db = SQLAlchemy(app)

# -------------------
# МОДЕЛИ
# -------------------

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))
    date = db.Column(db.String(50))


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    before_img = db.Column(db.String(200))
    after_img = db.Column(db.String(200))


# -------------------
# РОУТЫ
# -------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/portfolio')
def portfolio():
    items = Portfolio.query.all()
    return render_template('portfolio.html', items=items)


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    price = None

    if request.method == 'POST':
        service = request.form['service']
        car_type = request.form['car_type']

        base_prices = {
            'polish': 100,
            'ceramic': 200,
            'cleaning': 80
        }

        multipliers = {
            'sedan': 1,
            'suv': 1.5,
            'premium': 2
        }

        price = base_prices[service] * multipliers[car_type]

    return render_template('calculator.html', price=price)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        new_booking = Booking(
            name=request.form['name'],
            phone=request.form['phone'],
            service=request.form['service'],
            date=request.form['date']
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('booking.html')


# -------------------
# ЗАПУСК
# -------------------
if __name__ == '__main__':
    with app.app_context():

        # 🔥 ОДИН РАЗ ОЧИЩАЕМ БАЗУ
        db.drop_all()
        db.create_all()

        # 📦 ДОБАВЛЯЕМ 4 МАШИНЫ
        items = [
            Portfolio(
                title="BMW M5 — полировка кузова",
                before_img="https://a1.drive-data.ru/GOKXl4pBOi_siXY4QyHZkJHT_ZY-1920.jpg",
                after_img="https://a1.drive-data.ru/s3urEzcY7b_1QJBYLcsgUvBOCp4-1920.jpg"
            ),

            Portfolio(
                title="Mercedes S-Class — керамика",
                before_img="https://a.d-cd.net/bDnWOJyucrscUy6tX5l5hvoT_Xc-1920.jpg",
                after_img="https://a.d-cd.net/JiWrNpofKFv5c6Ko5W_Wq9c0GoI-960.jpg"
            ),

            Portfolio(
                title="Audi A6 — восстановление ЛКП",
                before_img="https://a1.drive-data.ru/cg63kVce0v4ATshK7G3yOo2NeJE-960.jpg",
                after_img="https://a1.drive-data.ru/aPn6ijf5dQYJbDRga4nmTf7GYVY-960.jpg"
            ),

            Portfolio(
                title="Porsche 911 — детейлинг премиум",
                before_img="https://top-tuning.ru/upload/images/news/111233/porsche_911_predprodazhnaya_detailing_podgotovka_02.jpg",
                after_img="https://top-tuning.ru/upload/images/news/111233/porsche_911_predprodazhnaya_detailing_podgotovka_01.jpg"
            ),
        ]

        db.session.add_all(items)
        db.session.commit()

    # 🚀 ЗАПУСК СЕРВЕРА (ТОЛЬКО ОДИН РАЗ)
    app.run(host="0.0.0.0", port=10000, debug=True)
    