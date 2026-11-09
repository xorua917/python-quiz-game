def run_quiz():
    questions = [
        {"question": "파이썬에서 리스트에 요소를 추가하는 함수는?", "answer": "append"},
        {"question": "파이썬 파일의 확장자는?", "answer": ".py"},
        {"question": "출력할 때 사용하는 함수는?", "answer": "print"}
    ]
    score = 0
    print("\n--- 퀴즈 시작! ---")
    for i, q in enumerate(questions, 1):
        print(f"문제 {i}: {q['question']}")
        user_answer = input("답변: ").strip().lower()
        if user_answer == q['answer'].lower():
            print("정답입니다! ✨")
            score += 1
        else:
            print(f"오답입니다. 정답은 {q['answer']}입니다.")
    print(f"\n결과: {score}/{len(questions)}점을 맞혔습니다!")

def main():
    while True:
        print("\n=== 파이썬 퀴즈 게임 메뉴 ===")
        print("1. 퀴즈 시작")
        print("2. 게임 종료")
        choice = input("선택 (1/2): ").strip()

        if choice == "1":
            run_quiz()
        elif choice == "2":
            print("게임을 종료합니다. 다음에 또 봐요! 👋")
            break
        else:
            print("잘못된 입력입니다. 1 또는 2를 입력해주세요.")

if __name__ == "__main__":
    main()
