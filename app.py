from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
# Flask - непосредственно класс приложения
# render_template - для того, чтобы вернуть html документ
# url_for - для шаблона html (подключение css)
# request - для обработки отправки формы
# redirect - для переброски после создания объявления
# SQLAlchemy - для работы с бд
# datetime - для вставления в бд текущей даты

# datetime.strptime(str(ad.creation_date), "%Y-%m-%d")
# json.loads(convertDataToJson(ad))["description"]

def convertDataToJson(ad): # Преобразует запись таблицы в json
    return json.dumps(convertDataToDict(ad), indent=4, ensure_ascii=False)


def convertDataToDict(ad): # Преобразует запись таблицы в словарь
    ad_dict = {
        "id":ad.id,
        "header": ad.header,
        "description": ad.description,
        "creation_date": str(ad.creation_date),
        "owner": ad.owner
    }
    return ad_dict


app = Flask(__name__) # Создаем объект Flask и передаем ему этот файл
# Подключение к бд
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Класс для представления элемента таблицы бд
class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300))
    creation_date = db.Column(db.Date, default=datetime.utcnow)
    owner = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Ad %r>' % self.id




"""HTML part"""
# Домашняя страница
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


# Страница показа всех объявлений
@app.route('/ads')
def adsGet():
    ads = Ad.query.order_by(Ad.creation_date.desc()).all()
    return render_template("ads.html", ads=ads)


# Страница конкретного объявления
@app.route('/ads/<int:id>')
def adGet(id):
    ad = Ad.query.get(id)
    return render_template("ad.html", ad=ad)


# Удаление объявления
@app.route('/ads/<int:id>/delete')
def adDelete(id):
    ad = Ad.query.get_or_404(id)
    try:
        db.session.delete(ad)
        db.session.commit()
        return redirect('/ads')
    except:
        return "При удалении объявления произошла ошибка"


# Редактирование объявления
@app.route('/ads/<int:id>/update', methods=['POST', 'GET'])
def adUpdate(id):
    ad = Ad.query.get(id)
    # Обработка редактирования объявления
    if request.method == 'POST':
        # Получаем данные из формы и присваиваем их соответствующим полям
        ad.header = request.form["header"]
        ad.description = request.form["description"]
        ad.owner = request.form["owner"]

        # Добавляем этот объект в бд
        try:
            db.session.commit()
            return redirect('/ads')
        except:
            return "При редактировании объявления произошла ошибка"
    else:
        return render_template("update.html", ad=ad)


# Создание объявления
@app.route('/create-ad', methods=['POST', 'GET'])
def createAd():
    # Обработка добавления объявления
    if request.method == 'POST':
        # Получаем данные из формы
        header = request.form["header"]
        description = request.form["description"]
        owner = request.form["owner"]

        # Создаем на основе этих данных объект Ad
        ad = Ad(header=header, description=description, owner=owner)

        # Добавляем этот объект в бд
        try:
            db.session.add(ad)
            db.session.commit()
            return redirect('/create-ad')
        except:
            return "При добавлении объявления произошла ошибка"
    else:
        return render_template("create-ad.html")




"""Json part"""
"""@app.route('/test_json/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def testJsonGetById(id):
    ad = Ad.query.get_or_404(id)
    if request.method == 'GET':
        #ad = Ad.query.get(id)
        return convertDataToJson(ad)
    elif request.method == 'DELETE':
        #ad = Ad.query.get_or_404(id)
        try:
            db.session.delete(ad)
            db.session.commit()
            return redirect('/test_json')
        except:
            return "При удалении объявления произошла ошибка"
    elif request.method == 'PUT':
        ad.header = request.json["header"]
        ad.description = request.json["description"]
        ad.owner = request.json["owner"]
        try:
            db.session.commit()
            return redirect('/test_json')
        except:
            return "При редактировании объявления произошла ошибка"""


@app.route('/json/<int:id>', methods=['GET'])
def jsonGet(id):
    ad = Ad.query.get(id)
    return convertDataToJson(ad)


@app.route('/json/<int:id>', methods=['PUT'])
def jsonPut(id):
    ad = Ad.query.get(id)
    ad.header = request.json["header"]
    ad.description = request.json["description"]
    ad.owner = request.json["owner"]
    try:
        db.session.commit()
        return redirect('/json')
    except:
        return "При редактировании объявления произошла ошибка"


@app.route('/json/<int:id>', methods=['DELETE'])
def jsonDelete(id):
    ad = Ad.query.get_or_404(id)
    try:
        db.session.delete(ad)
        db.session.commit()
        return redirect('/json')
    except:
        return "При удалении объявления произошла ошибка"


"""@app.route('/test_json', methods=['GET', 'POST'])
def testJsonGetPost():
    if request.method == 'POST':
        header = request.json["header"]
        description = request.json["description"]
        owner = request.json["owner"]
        ad = Ad(header=header, description=description, owner=owner)
        try:
            db.session.add(ad)
            db.session.commit()
            ads = Ad.query.order_by(Ad.creation_date.desc()).all()
            json_ads = json.dumps([convertDataToDict(ad) for ad in ads], indent=4, ensure_ascii=False)
            return json_ads
        except:
            return "При добавлении объявления произошла ошибка"
    elif (request.method == 'GET'):
        ads = Ad.query.order_by(Ad.creation_date.desc()).all()
        json_ads = json.dumps([convertDataToDict(ad) for ad in ads], indent=4, ensure_ascii=False)
        return json_ads"""


@app.route('/json', methods=['GET'])
def jsonGetAll():
    ads = Ad.query.order_by(Ad.creation_date.desc()).all()
    json_ads = json.dumps([convertDataToDict(ad) for ad in ads], indent=4, ensure_ascii=False)
    return json_ads


@app.route('/json', methods=['POST'])
def jsonPost():
    header = request.json["header"]
    description = request.json["description"]
    owner = request.json["owner"]
    ad = Ad(header=header, description=description, owner=owner)
    try:
        db.session.add(ad)
        db.session.commit()
        ads = Ad.query.order_by(Ad.creation_date.desc()).all()
        json_ads = json.dumps([convertDataToDict(ad) for ad in ads], indent=4, ensure_ascii=False)
        return json_ads
    except:
        return "При добавлении объявления произошла ошибка"


if __name__ == "__main__":
    app.run(debug=False)
