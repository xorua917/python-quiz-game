def run_quiz():
    questions = [
        {"question": "파이썬에서 리스트에 요소를 추가하는 함수는?", "answer": "append"},
        {"question": "파이썬 파일의 확장자는?", "answer": ".py"},
        {"question": "출력할 때 사용하는 함수는?", "answer": "print"}
    ]
    score = 0
    print("\n=== 파이썬 기초 퀴즈 게임 ===\n")
    for i, q in enumerate(questions, 1):
        print(f"문제 {i}: {q['question']}")
        user_answer = input("답변: ").strip().lower()
        if user_answer == q['answer'].lower():
            print("정답입니다! ✨")
            score += 1
        else:
            print(f"오답입니다. 정답은 {q['answer']}입니다.")
    print(f"\n최종 점수: {score}/{len(questions)}")

if __name__ == "__main__":
    run_quiz()
