from IVR_app import *


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
    answer_type = db.Column(db.String(100), nullable=False)  # Qtext -> string/int | else "None"
    question_type = db.Column(db.String(100), nullable=False)


class QuestionsAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.Text(), nullable=False)


class QuestionsVariants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    variant = db.Column(db.Text(), nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    new_u = db.Column(db.Integer)
    done_first_test = db.Column(db.Integer)

    # Методы, нужные для класса, используемого для действий, связанных с пользователем (из документации flask_login)
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class DoneQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    test_id = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer)


class DoneTests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100), nullable=False)


class UserChance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    chance = db.Column(db.Integer, nullable=False)
    same = db.Column(db.Integer)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String)