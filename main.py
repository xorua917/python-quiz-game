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
                self.quizzes = [Quiz(q['question'], q['answer']) for q in data.get('quizzes', [])]
        
        if not self.quizzes:
            default_quizzes = [
                {"question": "파이썬에서 리스트에 요소를 추가하는 함수는?", "answer": "append"},
                {"question": "파이썬 파일의 확장자는?", "answer": ".py"},
                {"question": "출력할 때 사용하는 함수는?", "answer": "print"},
                {"question": "정수형 데이터 타입을 무엇이라 하나요?", "answer": "int"},
                {"question": "리스트의 길이를 구하는 함수는?", "answer": "len"}
            ]
            self.quizzes = [Quiz(q['question'], q['answer']) for q in default_quizzes]

    def save_state(self):
        """현재 고득점과 퀴즈 목록을 파일에 저장합니다."""
        data = {
            'high_score': self.high_score,
            'quizzes': [{'question': q.question, 'answer': q.answer} for q in self.quizzes]
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        """게임을 시작합니다."""
        print(f"\n=== 퀴즈 게임을 시작합니다! (현재 최고 점수: {self.high_score}) ===")
        score = 0
        
        for i, q in enumerate(self.quizzes, 1):
            print(f"\n문제 {i}: {q.question}")
            user_answer = input("답변: ").strip().lower()
            
            if user_answer == q.answer.lower():
                print("정답입니다! ✨")
                score += 1
            else:
                print(f"오답입니다. 정답은 [{q.answer}]입니다.")
        
        print(f"\n게임 종료! 당신의 점수는 {score}/{len(self.quizzes)}입니다.")
        
        if score > self.high_score:
            print(f"🎊 축하합니다! 새로운 최고 기록입니다! ({score}점)")
            self.high_score = score
            self.save_state()

if __name__ == "__main__":
    game = QuizGame()
    game.run()