import random
import time
import signal


TIME_LIMIT = 5
MISTAKE_RATE = 0.25


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException


def print_line():
    print("~" * 70)


def slow_print(text, delay=0.5):
    print(text)
    time.sleep(delay)


def timed_input(message, limit):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(limit)

    try:
        answer = input(message)
        signal.alarm(0)
        return answer
    except TimeoutException:
        signal.alarm(0)
        return None


def get_int_input_with_time(message, min_num, max_num, limit):
    answer = timed_input(message, limit)

    if answer is None:
        return None

    try:
        number = int(answer)

        if min_num <= number <= max_num:
            return number

        return "wrong"

    except ValueError:
        return "wrong"


def show_intro():
    print_line()
    print("🌸 두부두부게임 🌸")
    print("(두부두부두부 으쌰으쌰으쌰으쌰) x2")
    print_line()
    print("게임 방법")
    print("1. 현재 기준인 사람은 항상 두부 3모입니다.")
    print("2. 현재 3모 기준으로 1모, 2모, 4모, 5모가 정해집니다.")
    print("3. 지목당한 사람이 새로운 두부 3모가 됩니다.")
    print("4. 자기 자신인 3모를 외치면 벌칙입니다.")
    print("5. 제한 시간 안에 말하지 못하면 벌칙입니다.")
    print("6. 컴퓨터 플레이어는 일정 확률로 박자를 놓칩니다.")
    print("7. 누군가 벌칙을 받으면 두부게임 한 판이 종료됩니다.")
    print_line()


def make_seat_order(players):
    seat_order = players[:]
    random.shuffle(seat_order)
    return seat_order


def show_seat_order(seat_order):
    print("🪑 오늘의 자리 순서")
    for index, player in enumerate(seat_order, start=1):
        print(f"{index}. {player['name']}")
    print_line()


def get_tofu_family(seat_order, current_index):
    total = len(seat_order)

    return [
        (current_index - 2) % total,
        (current_index - 1) % total,
        current_index,
        (current_index + 1) % total,
        (current_index + 2) % total
    ]


def find_player_index(players, target_name):
    for index, player in enumerate(players):
        if player["name"] == target_name:
            return index

    return -1


def choose_tofu_number(current_player):
    if current_player["is_user"]:
        print()
        print(f"{current_player['name']}님의 차례입니다.")
        print(f"{TIME_LIMIT}초 안에 두부 몇 모를 외쳐야 합니다!")

        return get_int_input_with_time("1~5 중 선택 : ", 1, 5, TIME_LIMIT)

    number = random.randint(1, 5)
    slow_print(f"\n{current_player['name']} : 두부 {number}모!")

    return number


def computer_makes_mistake(current_player):
    if current_player["is_user"]:
        return False

    if random.random() < MISTAKE_RATE:
        slow_print(f"\n{current_player['name']}이(가) 박자를 놓쳤습니다!")
        return True

    return False


def give_penalty(player, reason):
    player["drink"] += 1

    print()
    print(f"🍺 {player['name']} 벌칙! 술 1잔!")
    print(f"이유 : {reason}")
    print("두부는 네모! 두부는 네모!")


def play_tofu_game(players, start_player):
    show_intro()

    if len(players) < 4:
        print("두부두부게임은 본인 포함 4명이 필요합니다.")
        print("친구를 3명 초대한 경우에만 플레이할 수 있습니다.")
        return

    seat_order = make_seat_order(players)
    show_seat_order(seat_order)

    current_index = find_player_index(seat_order, start_player["name"])

    if current_index == -1:
        current_index = random.randint(0, len(seat_order) - 1)

    round_num = 1

    print("첫 번째 두부 3모가 정해졌습니다!")
    print("누군가 벌칙을 받을 때까지 두부게임을 진행합니다.")

    while True:
        print_line()
        print(f"🌸 두부게임 라운드 {round_num} 🌸")

        current_player = seat_order[current_index]
        family = get_tofu_family(seat_order, current_index)

        if computer_makes_mistake(current_player):
            give_penalty(current_player, "박자를 놓침")
            print_line()
            print("두부두부게임 한 판이 종료되었습니다.")
            return

        tofu_number = choose_tofu_number(current_player)

        if tofu_number is None:
            give_penalty(current_player, f"{TIME_LIMIT}초 안에 말하지 못함")
            print_line()
            print("두부두부게임 한 판이 종료되었습니다.")
            return

        elif tofu_number == "wrong":
            give_penalty(current_player, "1~5가 아닌 값을 입력함")
            print_line()
            print("두부두부게임 한 판이 종료되었습니다.")
            return

        elif tofu_number == 3:
            print(f"\n{current_player['name']} : 두부 3모!")
            give_penalty(current_player, "자기 자신인 3모를 외침")
            print_line()
            print("두부두부게임 한 판이 종료되었습니다.")
            return

        else:
            if current_player["is_user"]:
                print(f"\n{current_player['name']} : 두부 {tofu_number}모!")

            next_index = family[tofu_number - 1]
            print("다음 차례로 넘어갑니다.")
            current_index = next_index

        round_num += 1


if __name__ == "__main__":
    test_players = [
        {"name": "민서", "capacity": 6, "drink": 0, "is_user": True},
        {"name": "예지", "capacity": 8, "drink": 0, "is_user": False},
        {"name": "아린", "capacity": 6, "drink": 0, "is_user": False},
        {"name": "다희", "capacity": 7, "drink": 0, "is_user": False},
    ]

    play_tofu_game(test_players, test_players[0])