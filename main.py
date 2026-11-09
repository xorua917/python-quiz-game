
import json
import os
import shutil
from datetime import datetime


class Quiz:
    """개별 퀴즈의 문제, 선택지, 정답을 관리합니다."""

    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")

        if (
            not isinstance(choices, list)
            or len(choices) != 4
            or any(
                not isinstance(choice, str) or not choice.strip()
                for choice in choices
            )
        ):
            raise ValueError("퀴즈에는 비어 있지 않은 선택지 4개가 필요합니다.")

        if type(answer) is not int or answer not in range(1, 5):
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

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
    """퀴즈 진행, 문제 관리, 점수 및 JSON 저장을 담당합니다."""

    def __init__(self, filename="state.json"):
        self.filename = filename
        self.quizzes = []
        self.high_score = 0
        self.storage_writable = True
        self.load_state()

    def default_quizzes(self):
        """기본 퀴즈 5개를 생성합니다."""
        return [
            Quiz(
                "파이썬에서 리스트에 요소를 추가하는 함수는?",
                ["append", "pop", "sort", "clear"],
                1
            ),
            Quiz(
                "파이썬 파일의 확장자는?",
                [".txt", ".py", ".json", ".exe"],
                2
            ),
            Quiz(
                "출력할 때 사용하는 함수는?",
                ["input", "len", "print", "type"],
                3
            ),
            Quiz(
                "정수형 데이터 타입을 무엇이라 하나요?",
                ["str", "bool", "float", "int"],
                4
            ),
            Quiz(
                "리스트의 길이를 구하는 함수는?",
                ["len", "list", "max", "sum"],
                1
            ),
        ]

    def load_state(self):
        """JSON 파일을 불러오고 손상 시 백업 후 복구합니다."""
        defaults = self.default_quizzes()
        default_map = {quiz.question: quiz for quiz in defaults}

        if not os.path.exists(self.filename):
            self.quizzes = defaults
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("JSON 최상위 구조가 올바르지 않습니다.")

            saved_score = data.get("high_score", 0)

            if type(saved_score) is not int or saved_score < 0:
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")

            saved_quizzes = data["quizzes"]

            if not isinstance(saved_quizzes, list):
                raise ValueError("퀴즈 목록이 올바르지 않습니다.")

            loaded = []
            converted = False

            for item in saved_quizzes:
                if not isinstance(item, dict):
                    raise ValueError("퀴즈 데이터가 올바르지 않습니다.")

                if "choices" in item:
                    loaded.append(
                        Quiz(
                            item["question"],
                            item["choices"],
                            item["answer"]
                        )
                    )

                elif item.get("question") in default_map:
                    loaded.append(default_map[item["question"]])
                    converted = True

                else:
                    raise ValueError(
                        "변환할 수 없는 기존 퀴즈 데이터입니다."
                    )

            self.quizzes = loaded if loaded else defaults
            self.high_score = saved_score

            if converted:
                print("기존 주관식 퀴즈를 4지선다형으로 변환했습니다.")

        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError
        ) as error:
            print(f"\n데이터 불러오기 실패: {error}")

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            backup_name = f"{self.filename}.corrupt-{timestamp}.bak"

            try:
                shutil.copy2(self.filename, backup_name)
                print(f"손상된 원본을 백업했습니다: {backup_name}")

            except OSError as backup_error:
                print(f"백업에 실패했습니다: {backup_error}")
                print("기존 파일 보호를 위해 저장을 차단합니다.")
                self.storage_writable = False

            self.quizzes = defaults
            self.high_score = 0

            print("기본 퀴즈 5개로 복구하여 시작합니다.")

    def save_state(self):
        """퀴즈와 최고 점수를 JSON 파일에 저장합니다."""
        if not self.storage_writable:
            print("원본 파일 보호를 위해 저장이 차단되어 있습니다.")
            return False

        data = {
            "high_score": self.high_score,
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ]
        }

        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except OSError as error:
            print(f"데이터 저장에 실패했습니다: {error}")
            return False

    def run(self):
        """퀴즈를 출제하고 정답을 판정합니다."""
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

                print(
                    f"오답입니다. 정답은 "
                    f"{quiz.answer}번 ({correct})입니다."
                )

        print(f"\n게임 종료! 점수: {score}/{len(self.quizzes)}")

        if score > self.high_score:
            self.high_score = score
            print("새로운 최고 점수입니다!")

        self.save_state()

    def add_quiz(self):
        """사용자가 새로운 4지선다 퀴즈를 등록합니다."""
        print("\n=== 새 퀴즈 추가 ===")

        while True:
            question = input("문제 입력: ").strip()

            if question:
                break

            print("문제는 비워둘 수 없습니다.")

        choices = []

        for i in range(1, 5):
            while True:
                choice = input(f"{i}번 선택지: ").strip()

                if choice:
                    choices.append(choice)
                    break

                print("선택지는 비워둘 수 없습니다.")

        while True:
            answer = input("정답 번호 (1~4): ").strip()

            if answer in ("1", "2", "3", "4"):
                break

            print("1~4 사이의 숫자를 입력해주세요.")

        new_quiz = Quiz(question, choices, int(answer))
        self.quizzes.append(new_quiz)

        if self.save_state():
            print("퀴즈가 추가되고 저장되었습니다!")
        else:
            print("퀴즈가 현재 실행에만 추가되었습니다.")

    def list_quizzes(self):
        """등록된 퀴즈 목록을 출력합니다."""
        print("\n=== 등록된 퀴즈 목록 ===")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes, 1):
            print(f"\n[퀴즈 {i}]")
            quiz.display()
            print(f"정답: {quiz.answer}번")

    def show_menu(self):
        """메인 메뉴를 표시하고 선택한 기능을 실행합니다."""
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
                    self.add_quiz()

                elif choice == "3":
                    self.list_quizzes()

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
