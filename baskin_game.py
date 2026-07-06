import random

# 배스킨라빈스
def play_turn(name, cur, is_human):
    limit = min(3, 31 - cur)  # 이번 턴에 부를 수 있는 최대 개수
    if is_human:
        while True:
            raw = input(f"{name}님, 부를 숫자를 입력하세요 (예: {' '.join(map(str, range(cur+1, cur+1+limit)))}): ").strip()
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
 
 
def play_game(players):
    """players = [(이름, is_human), ...] 여러 명이 순서대로 참여.
    31을 부른 사람(패자)의 이름을 반환."""
    print("=" * 40)
    print("        🍦 배스킨라빈스31 시작! (다 같이)")
    print("=" * 40)
 
    cur, idx = 0, 0
    while cur < 31:
        name, is_human = players[idx]
        called, cur = play_turn(name, cur, is_human)
        if 31 in called:
            print("─" * 42)
            print(f"💀 {name}(이)가 31을 불렀습니다! → {name} 원샷! 🍺")
            print("─" * 42)
            return name
        idx = (idx + 1) % len(players)  # 다음 사람으로 (원형으로 순환)
 

# 게임 진행 관련 (main.py)
def get_player_name():
    name = input('사용자의 이름을 입력해주세요: ')
    return name

def get_capacity():
    menu = {1: 2, 2: 4, 3: 6, 4: 8, 5: 10}  
    print("\n🍶 소주 기준 당신의 주량은?")
    print("  1. 소주 반병 (2잔)")
    print("  2. 소주 반병~한병 (4잔)")
    print("  3. 소주 한병~한병반 (6잔)")
    print("  4. 소주 한병반~두병 (8잔)")
    print("  5. 소주 두병 이상 (10잔)")
    while True:
        try:
            choice = int(input("당신의 치사량(주량)은? (1~5): "))
            if choice in menu:
                return menu[choice]
            print("⚠️  1~5 사이로 선택해주세요.")
        except ValueError:
            print("⚠️  숫자를 입력해주세요.")

FRIENDS = ["은서", "하연", "연서", "예진", "헌도"]

def invite_friends():
    while True:
        try:
            n = int(input("\n몇 명을 술게임에 초대할까요? (최대 3명): "))
            if 1 <= n <= 3:
                break
            print("⚠️  1~3명만 초대할 수 있어요.")
        except ValueError:
            print("⚠️  숫자를 입력해주세요.")

    names = random.sample(FRIENDS, n)  # 중복 없이 n명 랜덤 선택
    friends = {}
    for nm in names:
        cap = random.choice([2, 4, 6, 8, 10])  # 주량 랜덤 배정
        friends[nm] = cap
        print(f"오늘 함께 취할 친구는 {nm}입니다! (치사량: {cap})")
    return friends

def print_status(limits, drinks):
    print("~" * 42)
    for name in limits:
        left = limits[name] - drinks[name]
        print(f"{name}은(는) 지금까지 {drinks[name]}🍺! 치사량까지 {left}")
    print("~" * 42)
 
 
def game_over(loser, limits, drinks):
    print_status(limits, drinks)      # 최종 상황 출력
    print("-" * 42)
    print("        💀  G A M E   O V E R !  💀")
    print("-" * 42)
    print(f"{loser}이(가) 전사했습니다... 꿈나라에서는 편히 쉬시길 ..zzz")
    print("🍺 다음에 술 마시면 또 불러주세요~ 안녕! 🍺")

if __name__ == "__main__":
    my_capacity = get_capacity()      # 내 주량 선택
    my_name = get_player_name()       # 내 이름
    friends = invite_friends()        # 친구 초대 (랜덤 이름+주량)
 
    # 참가자 전원: 나 + 초대한 친구들
    limits = {my_name: my_capacity, **friends}
    drinks = {name: 0 for name in limits}
 
    # 게임에 참여할 순서 리스트 (나는 사람, 친구는 컴퓨터)
    players = [(my_name, True)] + [(nm, False) for nm in friends]
 
    while True:
        loser = play_game(players)     # 전원이 한 판 진행
        drinks[loser] += 1
 
        # 치사량 도달 → 게임오버 후 종료
        if drinks[loser] >= limits[loser]:
            game_over(loser, limits, drinks)
            break
 
        print_status(limits, drinks)
