import random


def play_turn(name, cur, is_human):
    limit = min(3, 31 - cur)  # 이번 턴에 부를 수 있는 최대 개수
    if is_human:
        while True:
            raw = input(
                f"{name}님, 부를 숫자를 입력하세요 "
                f"(예: {' '.join(map(str, range(cur + 1, cur + 1 + limit)))}): "
            ).strip()
            nums = raw.split()
            if not all(n.isdigit() for n in nums):
                print("⚠️  숫자만 공백으로 구분해서 입력해주세요!")
                continue
            nums = [int(n) for n in nums]
            if not (1 <= len(nums) <= limit):
                print(f"⚠️  1 ~ {limit}개만 부를 수 있어요!")
                continue
            if nums != list(range(cur + 1, cur + 1 + len(nums))):
                print(f"⚠️  {cur + 1}부터 순서대로 연속된 숫자여야 해요!")
                continue
            called = nums
            break
    else:  # 컴퓨터는 랜덤
        count = random.randint(1, limit)
        called = list(range(cur + 1, cur + 1 + count))

    print(f"🔢 {name}: {' '.join(map(str, called))}")
    return called, called[-1]


def play_game():
    """main.py의 run_game에서 인자 없이 호출됨.
    나 vs 컴퓨터 1:1로 베스킨라빈스31 진행."""
    print("=" * 40)
    print("      🍦 베스킨라빈스31 게임 시작! 🍦")
    print("31을 부르는 사람이 원샷! 1~3개씩 이어서 세요.")
    print("=" * 40)

    players = [("나", True), ("컴퓨터", False)]
    cur, idx = 0, 0

    while cur < 31:
        name, is_human = players[idx]
        called, cur = play_turn(name, cur, is_human)
        if 31 in called:
            print("-" * 40)
            print(f"💀 {name}(이)가 31을 불렀습니다! → {name} 원샷! 🍺")
            print("-" * 40)
            return name  # main은 리턴값을 안 쓰지만, 있어도 무방
        idx = (idx + 1) % len(players)  # 다음 사람으로


# 단독 테스트용
if __name__ == "__main__":
    play_game()