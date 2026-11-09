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
        self.load_state()

    def load_state(self):
        """파일에서 고득점과 퀴즈 목록을 불러옵니다."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.high_score = data.get('high_score', 0)
                # JSON 데이터를 Quiz 객체 리스트로 변환
                self.quizzes = [Quiz(q['question'], q['answer']) for q in data.get('quizzes', [])]
        
        # 만약 불러온 퀴즈가 없다면 기본 문제 5개를 추가합니다 (평가 기준 충족)
        if not self.quizzes:
            default_quizzes = [
                {"question": "파이썬에서 리스트에 요소를 추가하는 함수는?", "answer": "append"},
                {"question": "파이썬 파일의 확장자는?", "answer": ".py"},
                {"question": "출력할 때 사용하는 함수는?", "answer": "print"},
                {"question": "정수형 데이터 타입을 무엇이라 하나요?", "answer": "int"},
                {"question": "리스트의 길이를 구하는 함수는?", "answer": "len"}
            ]
            self.quizzes = [Quiz(q['question'], q['answer']) for q in default_quizzes]