import requests
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash


# conn = psycopg2.connect(database="service_db",
#                         user="postgres",
#                         password="0000",
#                         host="localhost",
#                         port="5432")
# cursor = conn.cursor()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


# db.create_all()

# for i in range(10):
#     new_user = User(
#                 name=f"name{i}",
#                 login=f"123{i}",
#                 password=f"qwerty123{i}",
#             )
#     db.session.add(new_user)
#     db.session.commit()




@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == "" or password == "":
                flash("Вы указали не все данные")
                return render_template('login.html')
            elif User.query.filter_by(login=f"{username}").first():
                if (User.query.filter_by(login=f"{username}").first()).password != password:
                    flash("Username or password does not exist, please try again.")
                    return render_template('login.html')

                else:

                 return render_template("account.html",
                                           full_name=(User.query.filter_by(login=f"{username}").first().name))
            else:
                flash("Username or password does not exist, please try again.")

                return render_template('login.html')
            # cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            # records = list(cursor.fetchall())



    return render_template('login.html')




@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name == "" or login == "" or password == "":
            flash("Вы указали не все данные")
        elif User.query.filter_by(login=f"{login}").first():
            flash("Вы уже зарегестрированы")
            return redirect('/login/')
        else:
            new_user = User(
                login=login,
                name=name,
                password=password,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Вы успешно зарегестрированы,используйте ваши данные для входа")
            return redirect('/login/')

    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)