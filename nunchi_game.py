import random

def get_player_count():
    while True:
        try:
            count = int(input("컴퓨터 참가자 수를 입력하세요 (1~4명): "))
            if 1 <= count <= 4:
                return count
            else:
                print("1~4 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")

def get_user_choice():
    while True:
        try:
            choice = int(input("\n1~5 중 숫자를 선택하세요: "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("1~5 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")

def play_game():
    print("=" * 40)
    print("        👀 눈치게임을 시작합니다!")
    print("=" * 40)

    computer_count = get_player_count()

    total_drinks = 0
    round_num = 1

    while True:
        print(f"\n--- 라운드 {round_num} ---")

        # 참가자 숫자 선택
        choices = {}
        choices["나"] = get_user_choice()

        for i in range(1, computer_count + 1):
            choices[f"컴퓨터{i}"] = random.randint(1, 5)

        # 결과 출력
        print("\n📋 선택 결과:")
        for name, num in choices.items():
            print(f"  {name}: {num}")

        # 중복 확인
        user_num = choices["나"]
        others = [v for k, v in choices.items() if k != "나"]

        if user_num in others:
            print("\n😵 다른 참가자와 숫자가 겹쳤습니다! 술 1잔 마시세요!")
            total_drinks += 1
        else:
            print("\n🎉 성공! 혼자 다른 숫자를 선택했습니다!")

        print(f"🍺 현재까지 마신 술: {total_drinks}잔")

        # 계속 여부
        again = input("\n계속 하시겠습니까? (y/n): ").strip().lower()
        if again != "y":
            break

        round_num += 1

    print("\n" + "=" * 40)
    print(f"  게임 종료! 총 {total_drinks}잔 마셨습니다.")
    if total_drinks == 0:
        print("  👑 완벽한 눈치왕입니다!")
    elif total_drinks <= 2:
        print("  😅 눈치가 아쉬웠네요...")
    else:
        print("  😵 오늘 많이 마셨네요...")
    print("=" * 40)

if __name__ == "__main__":

    play_game()
