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


def make_default_players(computer_count):
    players = [{"name": "나", "drink": 0, "is_user": True}]

    for i in range(1, computer_count + 1):
        players.append({
            "name": f"컴퓨터{i}",
            "drink": 0,
            "is_user": False
        })

    return players


def play_game(players=None, current_player=None):
    print("=" * 40)
    print("        👀 눈치게임을 시작합니다!")
    print("=" * 40)

    if players is None:
        computer_count = get_player_count()
        players = make_default_players(computer_count)

    if current_player is None:
        current_player = players[0]

    ordered_players = [current_player]
    for player in players:
        if player["name"] != current_player["name"]:
            ordered_players.append(player)

    print("참가자:", ", ".join(player["name"] for player in ordered_players))

    total_drinks = 0
    round_num = 1

    while True:
        print(f"\n--- 라운드 {round_num} ---")

        # 참가자 숫자 선택
        choices = {}
        for player in ordered_players:
            if player.get("is_user"):
                choices[player["name"]] = get_user_choice()
            else:
                choices[player["name"]] = random.randint(1, 5)

        # 결과 출력
        print("\n📋 선택 결과:")
        for name, num in choices.items():
            print(f"  {name}: {num}")

        # 중복 확인
        duplicated_numbers = {
            num for num in choices.values()
            if list(choices.values()).count(num) > 1
        }

        if duplicated_numbers:
            loser_names = [
                name for name, num in choices.items()
                if num in duplicated_numbers
            ]
            print("\n😵 숫자가 겹쳤습니다! 겹친 사람은 술 1잔!")
            print("벌칙:", ", ".join(loser_names))

            for player in players:
                if player["name"] in loser_names:
                    player["drink"] += 1
                    if player.get("is_user"):
                        total_drinks += 1
        else:
            print("\n🎉 성공! 아무도 숫자가 겹치지 않았습니다!")

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
