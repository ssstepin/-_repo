from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

import classes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

secret_key = "seemeenokap"

result = cl = same = 0


# Таблицы 
class UserAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer1 = db.Column(db.String(100), nullable=False)
    answer2 = db.Column(db.String(100), nullable=False)
    answer3 = db.Column(db.String(100), nullable=False)
    answer4 = db.Column(db.String(100), nullable=False)
    answer5 = db.Column(db.String(100), nullable=False)
    answer6 = db.Column(db.String(100), nullable=False)
    answer7 = db.Column(db.String(100), nullable=False)
    answer8 = db.Column(db.String(100), nullable=False)
    answer9 = db.Column(db.String(100), nullable=False)
    answer10 = db.Column(db.String(100), nullable=False)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    answer_type = db.Column(db.String(100), nullable=False)
    question_type = db.Column(db.String(100), nullable=False)


class QuestionsAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.Text(), nullable=False)


class QuestionsVariants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    variant = db.Column(db.Text(), nullable=False)


# Функции для формы с шансом
def get_questions_chance():
    questions = UserAnswers.query.filter(UserAnswers.id == 1)
    arr = []
    for elem in questions:
        arr.append((elem.answer1, 1))
        arr.append((elem.answer2, 2))
        arr.append((elem.answer3, 3))
        arr.append((elem.answer4, 4))
        arr.append((elem.answer5, 5))
        arr.append((elem.answer6, 6))
        arr.append((elem.answer7, 7))
        arr.append((elem.answer8, 8))
        arr.append((elem.answer9, 9))
        arr.append((elem.answer10, 10))
    return arr


def get_answer():
    res = []
    for i in range(len(get_questions_chance())):
        if request.form['q' + str(i + 1)] == 'Да':
            res.append(1)
        else:
            res.append(0)
    return res


def find_same_answer():
    res = get_answer()
    answers = UserAnswers.query.filter(UserAnswers.id > 1).all()
    cnt = 0
    for i in range(len(res)):
        if res[i]:
            res[i] = "Да"
        else:
            res[i] = "Нет"
    # print(res)
    for elem in answers:
        if elem.answer1 == res[0] and elem.answer2 == res[1] and elem.answer3 == res[2] and elem.answer4 == res[
            3] and elem.answer5 == res[4] and elem.answer6 == res[5] and elem.answer7 == res[6] and elem.answer8 == res[
            7] and elem.answer9 == res[8] and elem.answer10 == res[9]:
            cnt += 1
    return cnt


def get_chance_result():
    # res = 0
    # for i in range(len(get_questions_chance())):
    #   if request.form['q' + str(i + 1)] == 'Да':
    #      res += 1
    # return res
    res = get_answer()
    all_res = [0] * len(get_questions_chance())
    answers = UserAnswers.query.filter(UserAnswers.id > 1).all()
    cnt = len(answers)
    # print(answers)
    for elem in answers:
        # print(elem)
        if elem.answer1 == 'Да':
            all_res[0] += 1
        if elem.answer2 == 'Да':
            all_res[1] += 1
        if elem.answer3 == 'Да':
            all_res[2] += 1
        if elem.answer4 == 'Да':
            all_res[3] += 1
        if elem.answer5 == 'Да':
            all_res[4] += 1
        if elem.answer6 == 'Да':
            all_res[5] += 1
        if elem.answer7 == 'Да':
            all_res[6] += 1
        if elem.answer8 == 'Да':
            all_res[7] += 1
        if elem.answer9 == 'Да':
            all_res[8] += 1
        if elem.answer10 == 'Да':
            all_res[9] += 1

    sum_res = 0
    # print(answers)
    for i in range(len(get_questions_chance())):
        sum_res += (all_res[i] * res[i] + (cnt - all_res[i]) * (1 - res[i]))

    return str(int(round((sum_res / (cnt * len(get_questions_chance()))), 2) * 100)) + '%'


def delete_chance():
    db.session.query(UserAnswers).delete()
    db.session.commit()


def chance_list():
    # return UserAnswers.query.filter(UserAnswers.id < 4).all()
    return UserAnswers.query.all()


# Функции для тестов

def get_questions_test_subject(subject):
    questions = Questions.query.filter(Questions.subject == subject)
    questions_arr = []
    for elem in questions:
        if elem.question_type == "QuestionCheckbox":
            q = classes.QuestionCheckbox(elem.text, [], get_variants_by_id(elem.id), elem.id)
        if elem.question_type == "QuestionRadio":
            q = classes.QuestionRadio(elem.text, "aleg", get_variants_by_id(elem.id), elem.id)
        if elem.question_type == "QuestionText":
            q = classes.QuestionText("ggg", ["3t3"], "string", elem.id)
        questions_arr.append(q)
    return questions_arr


def add_question(q_dict):
    question = Questions(subject=q_dict['subject'], text=q_dict['text'], answer_type=q_dict['answer_type'],
                         question_type=q_dict['question_type'])
    db.session.add(question)
    db.session.commit()


def get_variants_by_id(qid):
    variants_db = QuestionsVariants.query.filter(QuestionsVariants.question_id == qid).all()
    variants = []
    for elem in variants_db:
        variants.append(elem.variant)
    return variants


def get_answer_by_id(qid):
    answers_db = QuestionsAnswers.query.filter(QuestionsAnswers.question_id == qid).all()
    answers = []
    for elem in answers_db:
        answers.append(elem.variant)
    return answers


# Тело сайта
@app.route('/')
def hello_world():
    return render_template('base.html')


@app.route('/chance', methods=['POST', 'GET'])
def calc_chance():
    if request.method == "POST":
        # to_bd_chance()
        # return render_template("chance_res.html", result=get_chance_result(), data=chance_list())
        global result, cl, same
        result = get_chance_result()
        same = find_same_answer()
        cl = chance_list()
        return redirect('/chance/result')
    else:
        return render_template("chance.html", questions=get_questions_chance())


@app.route('/chance/result')
def show_res():
    # to_bd_chance()
    return render_template("chance_res.html", result=result, same=same)
    # return "Hello"


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    delete_chance()
    return redirect('/')


@app.route('/test')
def test():
    new_test = classes.Test(get_questions_test_subject('aleg'), 'aleg')
    return render_template("test.html", test_questions=new_test.questions, types_array=new_test.types_arr())
    # return render_template("test.html", test_questions=get_questions_test_subject("aleg"))


@app.route('/addtestquestion')
def add():
    render_template("addq.html")


if __name__ == '__main__':
    app.run(debug=True)
