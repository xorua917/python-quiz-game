import json
import os

class Quiz:
    """퀴즈 문제 하나에 대한 정보를 담는 클래스"""
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class QuizGame:
    def __init__(self, filename='state.json'):
        self.filename = filename
        self.quizzes = []
        self.high_score = 0