from IVR_app import classes  # Чтобы реализовать get_question_type


class Question(object):
    def __init__(self, text: str, answer: list, q_id: int, subject: str):
        self.questionText = text
        self.questionAnswer = answer
        self.id = q_id
        self.subject = subject

    def debug_print(self):
        print("Text:", self.questionText)
        print("Answer", self.questionAnswer)

    def check_answer(self, user_answer):
        right_answer = []
        for ans in self.questionAnswer:
            right_answer.append(ans.lower())
        user_answers = []
        for ans in set(user_answer):  # set, чтобы дополнительно исключить повторения
            user_answers.append(ans.lower())
        return sorted(right_answer) == sorted(user_answers)  # упорядочивание обоих списков


class QuestionCheckbox(Question):
    def __init__(self, text: str, answer: list, variants: list, q_id: int, subject: str):
        super(QuestionCheckbox, self).__init__(text, answer, q_id, subject)
        variants_plus = variants
        self.questionAnswerVariants = variants_plus

    def debug_print(self):
        super(QuestionCheckbox, self).debug_print()
        print("Variants:", self.questionAnswerVariants)

    def check_answer(self, user_answer):
        return super(QuestionCheckbox, self).check_answer(user_answer)


class QuestionRadio(Question):
    def __init__(self, text: str, answer: list, variants: list, q_id: int, subject: str):
        super(QuestionRadio, self).__init__(text, answer, q_id, subject)
        variants_plus = variants
        self.questionAnswerVariants = variants_plus

    def debug_print(self):
        super(QuestionRadio, self).debug_print()
        print("Variants:", self.questionAnswerVariants)

    def check_answer(self, user_answer):
        return super(QuestionRadio, self).check_answer(user_answer)


class QuestionText(Question):
    def __init__(self, text: str, answer: list, ans_type: str, q_id: int, subject: str):
        super(QuestionText, self).__init__(text, answer, q_id, subject)
        self.questionAnswerType = ans_type

    def debug_print(self):
        super(QuestionText, self).debug_print()
        print("Type", self.questionAnswerType)

    def check_answer(self, user_answer):
        return super(QuestionText, self).check_answer(user_answer)


class Test(object):
    def __init__(self, question_arr: list, subject: str):
        self.questions = question_arr
        self.subject = subject

    def types_arr(self):  # типы вопросов
        arr = []
        for elem in self.questions:
            arr.append(get_question_type(elem))
        return arr


class TestDone(Test):
    def __init__(self, question_arr: list, subject: str, u_ans: list):
        self.questions = question_arr
        self.subject = subject
        self.userAnswers = u_ans

    def types_arr(self):
        return super(TestDone, self).types_arr()

    def get_rw(
            self):  # rw = "right/wrong"; получить список результатов - 0, если на вопрос ответ неправильный, 1 - если правильный
        arr = []
        for i in range(len(self.questions)):
            if self.questions[i].check_answer(list(self.userAnswers[i])):
                arr.append(1)
            else:
                arr.append(0)
        return arr


def get_question_type(question):
    if type(question) == classes.Question:
        return "Question"
    if type(question) == classes.QuestionText:
        return "QuestionText"
    if type(question) == classes.QuestionCheckbox:
        return "QuestionCheckbox"
    if type(question) == classes.QuestionRadio:
        return "QuestionRadio"

    return "Not question"

# type == classes.Question
