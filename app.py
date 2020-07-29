from flask import Flask, render_template,request,url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonForm
from models import Person

app = Flask(__name__)

#database config
USER_DB = 'postgres'
PASS_DB = 'admin123'
URL_DB = '127.0.0.1'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#config flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#flask-wtk config
app.config['SECRET_KEY']='secret_key'


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    #person list
    persons = Person.query.all()
    total_person = Person.query.count()
    app.logger.debug(f'Person List: {persons}')
    app.logger.debug(f'Person Count: {total_person}')
    return render_template('index.html', persons=persons, total_person=total_person)

@app.route('/view/<int:id>')
def view_detail(id):
    #get person data
    person = Person.query.get_or_404(id)
    app.logger.debug(f'Person: {person}')
    return render_template('detail.html', person=person)

@app.route('/add', methods=['GET','POST'])
def add():
    person = Person()
    personForm =PersonForm(obj=person)
    if request.method == 'POST':
        if personForm.validate_on_submit():
            personForm.populate_obj(person)
            app.logger.debug(f'Insert Person: {person}')
            db.session.add(person)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add.html', form=personForm)
    
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    person = Person.query.get_or_404(id)
    personForm = PersonForm(obj=person)
    if request.method == 'POST':
        if personForm.validate_on_submit():
            personForm.populate_obj(person)
            app.logger.debug(f'Update Person: {person}')
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', form=personForm)

@app.route('/delete/<int:id>')
def delete(id):
    person = Person.query.get_or_404(id)
    app.logger.debug(f'Delete Person: {person}')
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

