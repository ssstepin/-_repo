from IVR_app import classes


class Question(object):
    def __init__(self, text: str, answer: list, q_id: int):
        self.questionText = text
        self.questionAnswer = answer
        self.id = q_id

    def debug_print(self):
        print("Text:", self.questionText)
        print("Answer", self.questionAnswer)

    def check_answer(self, user_answer):
        right_answer = []
        for ans in self.questionAnswer:
            right_answer.append(ans.lower())
        user_answers = []
        for ans in user_answer:
            user_answers.append(ans.lower())
        return sorted(right_answer) == sorted(user_answers)


class QuestionCheckbox(Question):
    def __init__(self, text: str, answer: list, variants: list, q_id: int):
        super(QuestionCheckbox, self).__init__(text, answer, q_id)
        variants_plus = variants + list(answer)
        self.questionAnswerVariants = variants_plus

    def debug_print(self):
        super(QuestionCheckbox, self).debug_print()
        print("Variants:", self.questionAnswerVariants)

    def check_answer(self, user_answer):
        return super(QuestionCheckbox, self).check_answer(user_answer)


class QuestionRadio(Question):
    def __init__(self, text: str, answer: list, variants: list, q_id: int):
        super(QuestionRadio, self).__init__(text, answer, q_id)
        variants_plus = variants + list(answer)
        self.questionAnswerVariants = variants_plus

    def debug_print(self):
        super(QuestionRadio, self).debug_print()
        print("Variants:", self.questionAnswerVariants)

    def check_answer(self, user_answer):
        return super(QuestionRadio, self).check_answer(user_answer)


class QuestionText(Question):
    def __init__(self, text: str, answer: list, ans_type: str, q_id: int):
        super(QuestionText, self).__init__(text, answer, q_id)
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

    def types_arr(self):
        arr = []
        for elem in self.questions:
            arr.append(get_question_type(elem))
        return arr


class TestDone(Test):
    def __init__(self, question_arr: list, subject: str, u_ans: list):
        #super(Test, self).__init__(question_arr, subject)
        self.questions = question_arr
        self.subject = subject
        self.userAnswers = u_ans

    def get_rw(self):
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
