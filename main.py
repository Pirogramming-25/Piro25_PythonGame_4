import random
from tofu_game import play_tofu_game

try:
    from nunchi_game import play_game as play_nunchi_game
except ImportError:
    play_nunchi_game = None

try:
    from subway_game import play_game as play_subway_game
except ImportError:
    play_subway_game = None

try:
    from baskin_game import play_baskin_game
except ImportError:
    play_baskin_game = None


PLAYER_POOL = ["민서", "예지", "아린", "다희", "피로"]


def print_line():
    print("~" * 70)


def get_yes_or_no(message):
    while True:
        answer = input(message).strip().lower()

        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("y 또는 n으로 입력해주세요.")


def get_int_input(message, min_num, max_num):
    while True:
        try:
            number = int(input(message))

            if min_num <= number <= max_num:
                return number
            else:
                print(f"{min_num}부터 {max_num} 사이의 숫자를 입력해주세요.")

        except ValueError:
            print("숫자로 입력해주세요.")


def show_intro():
    print_line()
    print("🍺 ALCOHOL GAME 🍺")
    print("안주 먹을 시간이 없어요 ❌ 마시면서 배우는 술게임 🍻")
    print_line()


def get_user_name():
    print("오늘 거하게 취해볼 당신은 누구인가요?")
    print(", ".join(PLAYER_POOL))

    while True:
        name = input("이름 입력 : ").strip()

        if name in PLAYER_POOL:
            print_line()
            print(f"{name}님으로 시작합니다.")
            print_line()
            return name

        print("목록에 있는 이름을 입력해주세요.")


def get_user_capacity():
    print_line()
    print("🍺 소주 기준 당신의 주량은? 🍺")
    print("1. 소주 반 병 (2잔)")
    print("2. 소주 반 병에서 한 병 (4잔)")
    print("3. 소주 한 병에서 한 병 반 (6잔)")
    print("4. 소주 한 병 반에서 두 병 (8잔)")
    print("5. 소주 두 병 이상 (10잔)")
    print_line()

    choice = get_int_input("당신의 치사량은 얼마인가요? 1~5 : ", 1, 5)
    return choice * 2


def invite_friends(user_name, user_capacity):
    players = [
        {
            "name": user_name,
            "capacity": user_capacity,
            "drink": 0,
            "is_user": True
        }
    ]

    print_line()
    friend_count = get_int_input(
        "같이 대결할 사람은 몇 명 초대할까요? 최대 3명 : ",
        1,
        3
    )

    friend_candidates = []

    for name in PLAYER_POOL:
        if name != user_name:
            friend_candidates.append(name)

    selected_names = random.sample(friend_candidates, friend_count)

    print_line()
    print("오늘 함께 취할 친구들입니다!")

    for name in selected_names:
        capacity = random.randint(2, 10)

        friend = {
            "name": name,
            "capacity": capacity,
            "drink": 0,
            "is_user": False
        }

        players.append(friend)
        print(f"{name}님이 참가합니다! 치사량 : {capacity}잔")

    print_line()
    return players


def show_status(players):
    print_line()

    for player in players:
        remain = player["capacity"] - player["drink"]

        if remain < 0:
            remain = 0

        print(
            f"{player['name']}은(는) 지금까지 {player['drink']}🍺! "
            f"치사량까지 {remain}"
        )

    print_line()


def show_game_list():
    print_line()
    print("🍺 오늘의 Alcohol GAME 🍺")
    print("1. 두부두부게임")
    print("2. 눈치게임")
    print("3. 지하철게임")
    print("4. 베스킨라빈스31게임")
    print("0. 종료")
    print_line()


def select_game(player):
    if player["is_user"]:
        choice = get_int_input(
            f"{player['name']}(이)가 좋아하는 랜덤 게임~ 랜덤 게임~ 무슨 게임? : ",
            0,
            4
        )

        if choice != 0:
            print_line()
            print(f"{player['name']}님이 게임을 선택하셨습니다! 😄")
            print_line()

        return choice

    print("술게임 진행 중! 다른 사람의 턴입니다.")
    print('그만하고 싶으면 "exit", 계속하고 싶으면 아무키나 입력해 주세요!')

    command = input("입력 : ").strip().lower()

    if command == "exit":
        return 0

    choice = random.randint(1, 4)

    print(
        f"{player['name']}(이)가 좋아하는 랜덤 게임~ "
        f"랜덤 게임~ 무슨 게임? : {choice}"
    )
    print_line()
    print(f"{player['name']}님이 게임을 선택하셨습니다! 😄")
    print_line()

    return choice


def run_game(choice, players, current_player):
    user_player = next((player for player in players if player["is_user"]), current_player)

    if choice == 1:
        if len(players) < 4:
            print_line()
            print("두부두부게임은 본인 포함 4명이 필요합니다.")
            print("친구를 3명 초대한 경우에만 플레이할 수 있습니다.")
            print("이번 턴은 넘어갑니다.")
            print_line()
        else:
            play_tofu_game(players, current_player)

    elif choice == 2:
        if play_nunchi_game is None:
            print("눈치게임 파일을 찾을 수 없습니다.")
        else:
            play_nunchi_game()

    elif choice == 3:
        if play_subway_game is None:
            print("지하철게임 파일을 찾을 수 없습니다.")
        else:
            play_subway_game(user_player["name"], current_player["name"])

    elif choice == 4:
        if play_baskin_game is None:
            print("베스킨라빈스31게임 파일을 찾을 수 없습니다.")
        else:
            play_baskin_game()


def check_game_over(players):
    for player in players:
        if player["drink"] >= player["capacity"]:
            print_line()
            print("GAME OVER!")
            print(f"{player['name']}이(가) 전사했습니다... 꿈나라에서는 편히 쉬시길... zzz")
            print_line()

            print("지금까지의 play 상황")
            for p in players:
                remain = p["capacity"] - p["drink"]
                if remain < 0:
                    remain = 0

                print(
                    f"{p['name']}은(는) 지금까지 {p['drink']}🍺! "
                    f"치사량까지 {remain}"
                )

            print_line()
            return True

    return False


def main():
    show_intro()

    start = get_yes_or_no("게임을 진행할까요? (y/n) : ")

    if not start:
        print("게임을 종료합니다.")
        return

    user_name = get_user_name()
    user_capacity = get_user_capacity()
    players = invite_friends(user_name, user_capacity)

    current_turn = 0

    while True:
        show_status(players)
        show_game_list()

        current_player = players[current_turn]
        choice = select_game(current_player)

        if choice == 0:
            print_line()
            print("게임을 종료합니다.")
            print_line()
            break

        run_game(choice, players, current_player)

        if check_game_over(players):
            break

        current_turn = (current_turn + 1) % len(players)


if __name__ == "__main__":
    main()
