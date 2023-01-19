from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from models import db, User, Questions, Answers
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/thanks')
def th():
    return render_template("thanks.html")


@app.route('/anketa')
def anketa():
    questions = Questions.query.all()
    return render_template("anketa.html", questions=questions)


@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')
    user = User(
        age=age,
        gender=gender,
        education=education
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    answer = Answers(id=user.id, q1=q1, q2=q2)
    db.session.add(answer)
    db.session.commit()
    return render_template("thanks.html")


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0]
    q1_answers = db.session.query(Answers.q1).all()
    all_info['q2_mean'] = db.session.query(func.avg(Answers.q2)).one()[0]
    q2_answers = db.session.query(Answers.q2).all()
    return render_template("stats.html", all_info=all_info)


if __name__ == '__main__':
    app.run(debug=True)
