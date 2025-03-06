#!/usr/bin/env python3
import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.Text, nullable=True)



class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"id": "name"})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"id": "lastname"})
    login = StringField('Login', validators=[DataRequired()], render_kw={"id": "login"})
    desc = TextAreaField('Description', render_kw={"id": "desc"})

@app.route('/home')
def home():
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():  
        # Créer un nouvel utilisateur
        user = User(
            name=form.name.data.strip(),
            lastname=form.lastname.data.strip(),
            login=form.login.data.strip(),
            desc=form.desc.data.strip() if form.desc.data else None
        )
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('list_user'))

        except Exception as e:
            # Gérer les erreurs, exemple sur un user avec les mêmes données
            db.session.rollback()  
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
            return render_template(
                'add_user.html',
                form=form,
                error="Une erreur est survenue,réessayer. "
                      "Assurez-vous que le login est unique."
            )
    return render_template('add_user.html', form=form)



@app.route('/list_user')
def list_user():
    users = User.query.all()
    return render_template('list_user.html', users=users)

@app.route('/show_user/<int:user_id>')
def show_user(user_id):

    user = db_session.query(User).filter(User.id == user_id).first()

    return render_template('show_user.html', user=user)

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
