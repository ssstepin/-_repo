from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import random
import datetime
import math
from flask_login import login_user, login_required, logout_user, current_user

from .models import *
from .classes import *

result = same = 0
cur_test = []
done_test = []  # done_test - classes.TestDone; cur_test - classes.Test
start_time = 0


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

    for elem in answers:

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
        q = []
        if elem.question_type == "QuestionCheckbox":
            q = QuestionCheckbox(elem.text, get_answer_by_id(elem.id), get_variants_by_id(elem.id), elem.id, subject)
        if elem.question_type == "QuestionRadio":
            q = QuestionRadio(elem.text, get_answer_by_id(elem.id), get_variants_by_id(elem.id), elem.id, subject)
        if elem.question_type == "QuestionText":
            q = QuestionText(elem.text, get_answer_by_id(elem.id), elem.answer_type, elem.id, subject)
        questions_arr.append(q)
    return questions_arr


def add_question(q_dict, q_ans, q_var):
    question = Questions(subject=q_dict['subject'], text=q_dict['text'], answer_type=q_dict['answer_type'],
                         question_type=q_dict['question_type'])
    db.session.add(question)
    db.session.commit()

    for var in q_var:
        nvariant = QuestionsVariants(question_id=question.id, variant=var)
        db.session.add(nvariant)
        db.session.commit()

    for ans in q_ans:
        nanswer = QuestionsAnswers(question_id=question.id, answer=ans)
        db.session.add(nanswer)
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
        answers.append(elem.answer)
    return answers


# Управление пользователями и их тестами

def add_new_user(user_login, user_password):
    new_u = Users(user_login=user_login, user_password=generate_password_hash(user_password), new_u=1)
    db.session.add(new_u)
    db.session.commit()


def check_login_pass(u_login, u_password):
    this_user = Users.query.filter(Users.user_login == u_login)
    arr = []
    for elem in this_user:
        arr.append(elem)

    if len(arr) > 0:
        return "same_user"
    else:
        if len(u_password) < 8 or len(u_password) > 32:
            return "wrong_pass_format"
        for symbol in u_password:
            if not (symbol.isalpha() or symbol.isdigit()):
                return "wrong_pass_format"
        return "success"


def check_user(user_login, user_password):
    this_user = Users.query.filter(Users.user_login == user_login).first()

    if not this_user:
        return "no_such_user"

    return check_password_hash(this_user.user_password, user_password)


def add_done_test(donetest):
    donet = DoneTests(user_id=current_user.id, subject=donetest.subject)
    db.session.add(donet)
    db.session.commit()
    for index in range(len(donetest.questions)):
        done_q = DoneQuestions(question_id=donetest.questions[index].id, test_id=donet.id,
                               result=donetest.get_rw()[index])
        db.session.add(done_q)
        db.session.commit()
    return


def get_tests_id_by_user_id(user_id):
    return [elem.id for elem in DoneTests.query.filter(DoneTests.user_id == user_id)]


def get_done_test_by_id(test_id):
    subject = (DoneTests.query.filter(DoneTests.id == test_id).first()).subject
    q_a = []
    for d_question in DoneQuestions.query.filter(DoneQuestions.test_id == test_id).all():
        elem = Questions.query.filter(Questions.id == d_question.question_id).first()
        q = []
        if elem.question_type == "QuestionCheckbox":
            q = QuestionCheckbox(elem.text, get_answer_by_id(elem.id), get_variants_by_id(elem.id), elem.id,
                                 subject)
        if elem.question_type == "QuestionRadio":
            q = QuestionRadio(elem.text, get_answer_by_id(elem.id), get_variants_by_id(elem.id), elem.id, subject)
        if elem.question_type == "QuestionText":
            q = QuestionText(elem.text, get_answer_by_id(elem.id), elem.answer_type, elem.id, subject)
        q_a.append(q)
    dt = TestDone(q_a, subject, [])
    return dt


def get_test_result_by_id(test_id):
    ans_arr = []
    for d_question in DoneQuestions.query.filter(DoneQuestions.test_id == test_id):
        ans_arr.append(d_question.result)

    return ans_arr


def add_user_chance(user_id, chance, same_ch):
    new_obj = UserChance(user_id=user_id, chance=chance, same=same_ch)
    db.session.add(new_obj)
    db.session.commit()


def get_user_chance(user_id):
    try:
        res = UserChance.query.filter(UserChance.user_id == user_id).first()
        return res.chance, res.same  # Кортеж
    except:
        return False


def get_tests_id_by_user_id_and_subject(user_id, subj):
    return [elem.id for elem in DoneTests.query.filter(DoneTests.user_id == user_id, DoneTests.subject == subj)]


def get_av_result_by_subject_and_user_id(subj):
    last_tests_id = get_tests_id_by_user_id_and_subject(current_user.id, subj)
    last_results = []
    for d_test in last_tests_id:
        res = get_test_result_by_id(d_test)
        if len(res):
            last_results.append(math.floor(100 * sum(res) / len(res)))
    return math.floor(sum(last_results) / (len(last_results) + int(len(last_results) == 0)))


def get_all_results_by_subj(subj):
    last_tests_id = get_tests_id_by_user_id_and_subject(current_user.id, subj)
    last_results = []
    for d_test in last_tests_id:
        res = get_test_result_by_id(d_test)
        if len(res):
            last_results.append(math.floor(100 * sum(res) / len(res)))

    return last_results


# Тело сайта
@app.route('/')
def main():
    return render_template('main.html', cur_user=current_user)


@app.route('/chance', methods=['POST', 'GET'])
@login_required
def calc_chance():
    global result, same
    if request.method == "POST":
        # to_bd_chance()
        # return render_template("chance_res.html", result=get_chance_result(), data=chance_list())
        result = get_chance_result()
        same = find_same_answer()
        if current_user.is_authenticated:
            add_user_chance(current_user.id, result, same)
        return redirect('/chance/result')
    else:
        if current_user.is_authenticated:
            cur_user_ch = get_user_chance(current_user.id)
            if cur_user_ch:
                result = cur_user_ch[0]
                same = cur_user_ch[1]
                return redirect('/chance/result')
        return render_template("chance.html", questions=get_questions_chance(), cur_user=current_user)


@app.route('/chance/result')
@login_required
def show_res():
    # to_bd_chance()
    return render_template("chance_res.html", result=result, same=same, cur_user=current_user,
                           done_first_test=current_user.done_first_test)
    # return "Hello"


@app.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    delete_chance()
    return redirect('/')


@app.route('/testall')
def testall():
    new_test = classes.Test(get_questions_test_subject('aleg'), 'aleg')
    return render_template("test.html", test_questions=new_test.questions, types_array=new_test.types_arr(),
                           cur_user=current_user)
    # return render_template("test.html", test_questions=get_questions_test_subject("aleg"))


@app.route('/admin', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        if request.form["question-subject"] and request.form["question-answer-type"] and request.form[
            "question-type"] and request.form["question-text"] and [request.form["question-answer"]]:
            q_d = {}
            q_d['subject'] = request.form["question-subject"]
            q_d['answer_type'] = request.form["question-answer-type"]
            q_d['question_type'] = request.form["question-type"]
            q_d['text'] = request.form["question-text"]

            q_a = [request.form["question-answer"]]

            q_v = [request.form.get("question-variant" + str(i + 1)) for i in range(3)]

            add_question(q_d, q_a, q_v)

    return render_template("addq.html", cur_user=current_user)


@app.route('/test', methods=['POST', 'GET'])
@login_required
def test_ch():
    if not current_user.done_first_test:
        flash('Тест для определения начального уровня не пройден!', 'alert alert-danger')
        return redirect('/profile')

    if request.method == "POST":
        sub = str(request.form.get('subject'))
        if sub != 'all':
            return redirect('/test/' + str(request.form.get('subject')) + '/' + str(request.form['q-num']))
        else:
            return redirect('/test/all')
    else:
        return render_template('test_ch.html', cur_user=current_user,
                               r_rus=get_av_result_by_subject_and_user_id("rus"),
                               r_math=get_av_result_by_subject_and_user_id("math"),
                               r_inf=get_av_result_by_subject_and_user_id("inf"),
                               r_all=get_av_result_by_subject_and_user_id("all"))


@app.route('/test/<subj>/<num>', methods=['POST', 'GET'])
@login_required
def test(subj, num):
    global cur_test
    global done_test
    global start_time

    if not current_user.done_first_test:
        flash('Тест для определения начального уровня не пройден!', 'alert alert-danger')
        return redirect('/profile')

    if request.method == 'POST':
        ans_arr = []
        for i in range(10):
            try:
                if request.form['q' + str(i)]:
                    ans_arr.append(request.form.getlist('q' + str(i)))
                else:
                    ans_arr.append([])
            except:
                ans_arr.append([])

        done_test = TestDone(cur_test.questions, cur_test.subject, ans_arr)
        last_done_tests_id = get_tests_id_by_user_id_and_subject(current_user.id, done_test.subject)

        if len(done_test.questions):
            add_done_test(done_test)
        test_time = math.floor(datetime.datetime.now().timestamp() - start_time.timestamp())

        if len(last_done_tests_id) != 0:
            last_done_test_id = last_done_tests_id[-1]
            last_done_test = get_done_test_by_id(last_done_test_id)
            last_tests_id = get_tests_id_by_user_id_and_subject(current_user.id, done_test.subject)
            last_tests = [get_done_test_by_id(t_id) for t_id in last_tests_id]

            # last_results = [math.floor(sum(d_test.get_rw()) / len(d_test.get_rw())) for d_test in last_tests]
            last_results = []
            for d_test in last_tests_id:
                res = get_test_result_by_id(d_test)
                if len(res):
                    last_results.append(math.floor(100 * sum(res) / len(res)))

            av_res = math.floor(sum(last_results) / len(last_results))

            return render_template('test_res.html', ans_arr=done_test.userAnswers, q_arr=done_test.questions,
                                   rw_arr=done_test.get_rw(), rw_arr_res=sum(done_test.get_rw()),
                                   last_test_rw_arr=get_test_result_by_id(last_done_test_id),
                                   last_test_rw_arr_res=sum(get_test_result_by_id(last_done_test_id)), lt=True,
                                   t_time=test_time, l_reults=last_results, avres=av_res,
                                   cur_user=current_user)
        else:
            return render_template('test_res.html', ans_arr=done_test.userAnswers, q_arr=done_test.questions,
                                   rw_arr=done_test.get_rw(), rw_arr_res=sum(done_test.get_rw()), lt=False,
                                   t_time=test_time,
                                   cur_user=current_user)
    else:
        questions_r = random.sample(get_questions_test_subject(subj), int(num))

        # new_test = classes.Test(get_questions_test_subject(subj), subj)
        new_test = Test(questions_r, subj)
        cur_test = new_test

        start_time = datetime.datetime.now()
        return render_template("test.html", test_questions=new_test.questions, types_array=new_test.types_arr(),
                               cur_user=current_user, subj=subj, num=num)


@app.route('/test/all', methods=['POST', 'GET'])
@login_required
def comp():
    global cur_test
    global done_test
    global start_time

    if request.method == 'POST':
        ans_arr = []
        for i in range(12):
            try:
                if request.form['q' + str(i)]:
                    ans_arr.append(request.form.getlist('q' + str(i)))
                else:
                    ans_arr.append([])
            except:
                pass

        current_user.done_first_test = 1
        db.session.commit()

        done_test = TestDone(cur_test.questions, cur_test.subject, ans_arr)
        last_done_tests_id = get_tests_id_by_user_id_and_subject(current_user.id, done_test.subject)

        if len(done_test.questions):
            add_done_test(done_test)
        test_time = math.floor(datetime.datetime.now().timestamp() - start_time.timestamp())

        if len(last_done_tests_id) != 0:
            last_done_test_id = last_done_tests_id[-1]
            last_done_test = get_done_test_by_id(last_done_test_id)
            last_tests_id = get_tests_id_by_user_id_and_subject(current_user.id, done_test.subject)
            last_tests = [get_done_test_by_id(t_id) for t_id in last_tests_id]

            # last_results = [math.floor(sum(d_test.get_rw()) / len(d_test.get_rw())) for d_test in last_tests]
            last_results = []
            for d_test in last_tests_id:
                res = get_test_result_by_id(d_test)
                if len(res):
                    last_results.append(math.floor(100 * sum(res) / len(res)))

            av_res = math.floor(sum(last_results) / len(last_results))

            return render_template('test_res.html', ans_arr=done_test.userAnswers, q_arr=done_test.questions,
                                   rw_arr=done_test.get_rw(), rw_arr_res=sum(done_test.get_rw()),
                                   last_test_rw_arr=get_test_result_by_id(last_done_test_id),
                                   last_test_rw_arr_res=sum(get_test_result_by_id(last_done_test_id)), lt=True,
                                   t_time=test_time, l_reults=last_results, avres=av_res,
                                   cur_user=current_user)
        else:
            return render_template('test_res.html', ans_arr=done_test.userAnswers, q_arr=done_test.questions,
                                   rw_arr=done_test.get_rw(), rw_arr_res=sum(done_test.get_rw()), lt=False,
                                   t_time=test_time,
                                   cur_user=current_user)
    else:
        questions_r = random.sample(
            random.sample(get_questions_test_subject('rus'), 6) + random.sample(get_questions_test_subject('math'), 6),
            12)

        # new_test = classes.Test(get_questions_test_subject(subj), subj)
        new_test = Test(questions_r, 'all')
        cur_test = new_test
        start_time = datetime.datetime.now()

        return render_template("test.html", test_questions=new_test.questions, types_array=new_test.types_arr(),
                               cur_user=current_user, subj="comp", num="12")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        n_login = request.form.get('login')
        n_pass = request.form.get('password')
        n_pass2 = request.form.get('s_password')

        if n_login and n_pass:
            res = check_login_pass(n_login, n_pass)
            if res == "same_user":
                flash('This user already exists', 'alert alert-danger')
                return redirect('/register')
            if res == "wrong_pass_format":
                flash('Wrong password format. 8 to 30 symbols, should contain only letters and digits',
                      'alert alert-danger')
                return redirect('/register')
            if n_pass2 != n_pass:
                flash('Passwords are not equal', 'alert alert-warning')
                return redirect('/register')
            if res == "success":
                add_new_user(n_login, n_pass)
                # login_user(Users.query.filter(Users.user_login == n_login).first())
                flash('You were successfully registered!', 'alert alert-success')
                return redirect('/login')

    return render_template('register.html', cur_user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        u_login = request.form.get('login')
        u_pass = request.form.get('password')

        if not u_login:
            flash('Please enter your login', 'alert alert-warning')

        if u_login and not u_pass:
            flash('Please enter password', 'alert alert-warning')
        if u_login and u_pass:
            if check_user(u_login, u_pass):
                if check_user(u_login, u_pass) == "no_such_user":
                    flash("No such user", 'alert alert-danger')
                else:
                    login_user(Users.query.filter(Users.user_login == u_login).first())
                    flash('You were successfully logged in!', 'alert alert-success')
                    return redirect('/profile')
            else:
                flash("Wrong password", 'alert alert-danger')

    return render_template('login.html', cur_user=current_user)


@app.route('/profile')
@login_required
def profile():
    if current_user.new_u:
        return redirect('/new_user')
    return render_template('user_profile.html', cur_user=current_user, did_chance=get_user_chance(current_user.id))


@app.route('/new_user')
@login_required
def new_user():
    if not current_user.new_u:
        return redirect('/profile')
    return render_template('new_user.html', cur_user=current_user)


@app.route('/greet')
@login_required
def greet_close():
    current_user.new_u = 0
    db.session.commit()
    return redirect('new_user')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/profile/tests')
@login_required
def pr_tests():
    if not current_user.done_first_test:
        flash('Тест для определения начального уровня не пройден!', 'alert alert-danger')
        return redirect('/profile')
    ut_id = get_tests_id_by_user_id(current_user.id)
    return render_template('tests_all_results.html', cur_user=current_user,
                           r_rus=get_all_results_by_subj("rus"), rav_rus=get_av_result_by_subject_and_user_id("rus"),
                           r_math=get_all_results_by_subj("math"),
                           rav_math=get_av_result_by_subject_and_user_id("math"),
                           r_inf=get_all_results_by_subj("inf"), rav_inf=get_av_result_by_subject_and_user_id("inf"),
                           r_all=get_all_results_by_subj("all"), rav_all=get_av_result_by_subject_and_user_id("all"))


@app.route('/message/<q_id>', methods=['POST', 'GET'])
@login_required
def message(q_id):
    if not current_user.done_first_test:
        flash('Тест для определения начального уровня не пройден!', 'alert alert-danger')
        return redirect('/profile')
    if request.method == 'POST':
        if request.form['message']:
            new_m = Messages(q_id=q_id, message=request.form['message'])
            db.session.add(new_m)
            db.session.commit()
            flash('Спасибо за сообщение!', 'alert alert-success')
            return redirect('/')
    return render_template('message.html', cur_user=current_user)


@app.errorhandler(401)
def page_not_found(e):
    flash('Log in first!', 'alert alert-warning')
    return redirect('/login')
