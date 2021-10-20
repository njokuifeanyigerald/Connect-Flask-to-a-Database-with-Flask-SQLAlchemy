from flask import  Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy


# first step in starting a flask app
app = Flask(__name__)

# configuring the database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# initializing sqlalchemy
db = SQLAlchemy(app)


class Database(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(300), unique=True)
    age = db.Column(db.Integer, nullable=False)


    # def __repr__(self):
    #     return 
@app.route('/')
def home():
    dashboard = Database.query.all()
    return render_template('home.html', dashboard=dashboard)

# function to add profiles
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        first = request.form.get('first_name')
        last = request.form.get('last_name')
        email = request.form.get('')
        age = request.form.get('age')
        
        if first != '' and last != '' and email != '' and age is not None:
            if Database.query.filter_by(email = email).count() == 0:          
                queryset = Database(first_name=first, last_name=last, age=age)
                db.session.add(queryset)
                db.session.commit()
                flash('data successfully added', 'success')
                return redirect(url_for('home'))
            else:
                flash('email already exist', 'warning')
                return render_template ('add.html')
        else:
            flash('pls input data in tht required fields', 'warning')
            return render_template ('add.html')
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    # deletes the data on the basis of unique id and
    # directs to home page
    data = Database.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash('data successfully deleted', 'danger')
    return redirect(url_for('home'))
 
if __name__ == '__main__':
    #for flashed messages to work, you have to add a secret key
    app.secret_key = "heyyf"
    app.run(debug=True)