from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lectures = db.Column(db.String(20))
    hours = db.Column(db.String(10))
    instructor = db.Column(db.String(50))
    price = db.Column(db.Float)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')

# Routes
@app.route('/')
def home():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        lectures = request.form['lectures']
        hours = request.form['hours']
        instructor = request.form['instructor']
        price = request.form['price']

        new_course = Course(title=title, description=description, lectures=lectures,
                            hours=hours, instructor=instructor, price=price)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_course.html')

@app.route('/pay/<int:course_id>', methods=['GET', 'POST'])
def pay(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        user_name = request.form['user_name']
        method = request.form['method']
        amount = course.price

        payment = Payment(user_name=user_name, course_id=course_id, amount=amount, method=method, status='Completed')
        db.session.add(payment)
        db.session.commit()
        return render_template('payment_success.html', course=course, user_name=user_name)
    return render_template('pay.html', course=course)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
