
import json
import os


class Quiz:
    """개별 퀴즈의 문제, 선택지, 정답을 관리합니다."""

    def __init__(self, question, choices, answer):
        if len(choices) != 4 or not isinstance(answer, int) or answer not in range(1, 5):
            raise ValueError("퀴즈는 선택지 4개와 정답 번호 1~4가 필요합니다.")
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(f"\n{self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def check_answer(self, answer):
        return answer == self.answer


class QuizGame:
    """퀴즈 진행, 최고 점수 및 데이터 저장을 관리합니다."""

    def __init__(self, filename="state.json"):
        self.filename = filename
        self.quizzes = []
        self.high_score = 0
        self.load_state()

    def default_quizzes(self):
        return [
            Quiz("파이썬에서 리스트에 요소를 추가하는 함수는?",
                 ["append", "pop", "sort", "clear"], 1),
            Quiz("파이썬 파일의 확장자는?",
                 [".txt", ".py", ".json", ".exe"], 2),
            Quiz("출력할 때 사용하는 함수는?",
                 ["input", "len", "print", "type"], 3),
            Quiz("정수형 데이터 타입을 무엇이라 하나요?",
                 ["str", "bool", "float", "int"], 4),
            Quiz("리스트의 길이를 구하는 함수는?",
                 ["len", "list", "max", "sum"], 1),
        ]

    def load_state(self):
        defaults = self.default_quizzes()
        default_map = {q.question: q for q in defaults}

        if not os.path.exists(self.filename):
            self.quizzes = defaults
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            saved_score = data.get("high_score", 0)
            if not isinstance(saved_score, int) or saved_score < 0:
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")

            loaded = []
            converted = False

            for item in data["quizzes"]:
                if "choices" in item:
                    loaded.append(
                        Quiz(item["question"], item["choices"], item["answer"])
                    )
                elif item["question"] in default_map:
                    loaded.append(default_map[item["question"]])
                    converted = True
                else:
                    raise ValueError("변환할 수 없는 기존 퀴즈 데이터입니다.")

            self.quizzes = loaded if loaded else defaults
            self.high_score = saved_score

            if converted:
                print("기존 주관식 퀴즈를 4지선다형으로 변환했습니다.")

        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"데이터를 불러오지 못했습니다: {error}")
            print("기본 퀴즈 데이터로 시작합니다.")
            self.quizzes = defaults
            self.high_score = 0

    def save_state(self):
        data = {
            "high_score": self.high_score,
            "quizzes": [
                {
                    "question": q.question,
                    "choices": q.choices,
                    "answer": q.answer
                }
                for q in self.quizzes
            ]
        }

        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"데이터 저장에 실패했습니다: {error}")

    def run(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        print(f"\n=== 퀴즈 시작! 총 {len(self.quizzes)}문제 ===")

        for i, quiz in enumerate(self.quizzes, 1):
            print(f"\n[문제 {i}]")
            quiz.display()

            while True:
                answer = input("정답 번호 (1~4): ").strip()

                if not answer:
                    print("빈 입력입니다. 다시 입력해주세요.")
                    continue

                try:
                    answer_number = int(answer)
                except ValueError:
                    print("숫자를 입력해주세요.")
                    continue

                if answer_number not in range(1, 5):
                    print("1~4 사이의 숫자를 입력해주세요.")
                    continue

                break

            if quiz.check_answer(answer_number):
                print("정답입니다!")
                score += 1
            else:
                correct = quiz.choices[quiz.answer - 1]
                print(f"오답입니다. 정답은 {quiz.answer}번 ({correct})입니다.")

        print(f"\n게임 종료! 점수: {score}/{len(self.quizzes)}")

        if score > self.high_score:
            self.high_score = score
            print("새로운 최고 점수입니다!")

        self.save_state()

    def show_menu(self):
        while True:
            print("\n=== 파이썬 퀴즈 게임 메뉴 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 최고 점수 확인")
            print("5. 종료")

            try:
                choice = input("메뉴 선택 (1~5): ").strip()

                if choice == "1":
                    self.run()
                elif choice == "2":
                    print("퀴즈 추가 기능은 다음 단계에서 구현합니다.")
                elif choice == "3":
                    print("퀴즈 목록 기능은 다음 단계에서 구현합니다.")
                elif choice == "4":
                    print(f"현재 최고 점수: {self.high_score}")
                elif choice == "5":
                    self.save_state()
                    print("게임을 종료합니다.")
                    return
                else:
                    print("잘못된 입력입니다. 1~5 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다. 안전하게 종료합니다.")
                self.save_state()
                return


if __name__ == "__main__":
    game = QuizGame()
    game.show_menu()
