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
