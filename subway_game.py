# 지하철 게임 

import random
import select
import sys
import time

LINES = {
    "1호선": ["소요산","동두천","보산","동두천중앙","지행","덕정","덕계","양주","녹양","가능","의정부","회룡",
             "망월사","도봉산","도봉","방학","창동","녹천","월계","광운대","석계","신이문","외대앞","회기",
             "청량리","제기동","신설동","동묘앞","동대문","종로5가","종로3가","종각","시청","서울역","남영",
             "용산","노량진","대방","신길","영등포","신도림","구로","구일","개봉","오류동","온수","역곡",
             "소사","부천","중동","송내","부개","부평","백운","동암","간석","주안","도화","제물포","도원",
             "동인천","인천"],
    "2호선": ["시청","을지로입구","을지로3가","을지로4가","동대문역사문화공원","신당","상왕십리","왕십리",
             "한양대","뚝섬","성수","건대입구","구의","강변","잠실나루","잠실","잠실새내","종합운동장",
             "삼성","선릉","역삼","강남","교대","서초","방배","사당","낙성대","서울대입구","봉천","신림",
             "신대방","구로디지털단지","대림","신도림","문래","영등포구청","당산","합정","홍대입구","신촌",
             "이대","아현","충정로"],
    "3호선": ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발",
             "연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로",
             "동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재",
             "매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"],
    "4호선": ["진접","오남","별내별가람","당고개","상계","노원","창동","쌍문","수유","미아","미아사거리",
             "길음","성신여대입구","한성대입구","혜화","동대문","동대문역사문화공원","충무로","서울역",
             "숙대입구","삼각지","신용산","이촌","동작","총신대입구","사당","남태령","선바위","경마공원",
             "대공원","과천","정부과천청사","인덕원","평촌","범계","금정","산본","수리산","대야미","반월",
             "상록수","한대앞","중앙","고잔","초지","안산","신길온천","정왕","오이도"],
    "5호선": ["방화","개화산","김포공항","송정","마곡","발산","우장산","화곡","까치산","신정","목동","오목교",
             "양평","영등포구청","영등포시장","신길","여의도","여의나루","마포","공덕","애오개","충정로",
             "서대문","광화문","종로3가","을지로4가","동대문역사문화공원","청구","신금호","행당","왕십리",
             "마장","답십리","장한평","군자","아차산","광나루","천호","강동","길동","굽은다리","명일","고덕",
             "상일동","강일","미사","하남풍산","하남시청","하남검단산"],
    "6호선": ["응암","역촌","불광","독바위","연신내","구산","새절","증산","디지털미디어시티","월드컵경기장",
             "마포구청","망원","합정","상수","광흥창","대흥","공덕","효창공원앞","삼각지","녹사평","이태원",
             "한강진","버티고개","약수","청구","신당","동묘앞","창신","보문","안암","고려대","월곡","상월곡",
             "돌곶이","석계","태릉입구","화랑대","봉화산","신내"],
    "7호선": ["장암","도봉산","수락산","마들","노원","중계","하계","공릉","태릉입구","먹골","중화","상봉",
             "면목","사가정","용마산","중곡","군자","어린이대공원","건대입구","뚝섬유원지","청담","강남구청",
             "학동","논현","반포","고속터미널","내방","이수","남성","숭실대입구","상도","장승배기","신대방삼거리",
             "보라매","신풍","대림","남구로","가산디지털단지","철산","광명사거리","천왕","온수","까치울",
             "부천종합운동장","춘의","신중동","부천시청","상동","삼산체육관","굴포천","부평구청"],
    "8호선": ["암사","천호","강동구청","몽촌토성","잠실","석촌","송파","가락시장","문정","장지","복정","산성",
             "남한산성입구","단대오거리","신흥","수진","모란"],
    "9호선": ["개화","김포공항","공항시장","신방화","마곡나루","양천향교","가양","증미","등촌","염창","신목동",
             "선유도","당산","국회의사당","여의도","샛강","노량진","노들","흑석","동작","구반포","신반포",
             "고속터미널","사평","신논현","언주","선정릉","삼성중앙","봉은사","종합운동장","삼전","석촌고분",
             "석촌","송파나루","한성백제","올림픽공원","둔촌오륜","중앙보훈병원"],
    "경의중앙선": ["문산","파주","월롱","금촌","금릉","운정","야당","탄현","일산","풍산","백마","곡산",
             "대곡","능곡","행신","강매","화전","수색","디지털미디어시티","가좌","신촌","서울역","이촌",
             "서빙고","한남","옥수","응봉","왕십리","청량리","회기","중랑","상봉","망우","양원","구리",
             "도농","양정","덕소","도심","팔당","운길산","양수","신원","국수","아신","오빈","양평","원덕",
             "용문"],
    "신분당선": ["신사","논현","신논현","강남","양재","양재시민의숲","청계산입구","판교","정자","미금",
             "동천","수지구청","성복","상현","광교중앙","광교"],
    "공항철도": ["서울역","공덕","홍대입구","디지털미디어시티","마곡나루","김포공항","계양","검암",
             "청라국제도시","영종","운서","공항화물청사","인천공항1터미널","인천공항2터미널"],
}

PLAYER_POOL = ["민서", "예지", "아린", "다희", "피로"]
TIMEOUT = 10          # 내 차례 제한 시간(초)
MISTAKE_PROB = 0.1    # NPC가 일부러 틀린 역을 말할 확률


class SubwayGame:
    def __init__(self, name, players):
        self.name = name
        self.players = players  # 이름 포함 전체 참가자 리스트 (main에서 랜덤으로 정해서 넘겨줌)
        self.line = ""
        self.used = set()

    def wait_for_input(self, prompt):
        # TIMEOUT초 안에 입력이 없으면 None 반환
        print(prompt, end="", flush=True)
        ready, _, _ = select.select([sys.stdin], [], [], TIMEOUT)
        if not ready:
            print()
            return None
        return sys.stdin.readline().strip()

    def try_answer(self, raw):
        # 역 이름(또는 환승)을 검사. 맞으면 상태 갱신 후 True, 틀리면 이유 출력 후 False
        if "환승" in raw:
            parts = raw.replace(",", " ").split()
            if len(parts) >= 2:
                station, target = parts[0], parts[-1]
                if (target in LINES and target != self.line
                        and station not in self.used
                        and station in LINES[self.line] and station in LINES[target]):
                    self.used.add(station)
                    self.line = target
                    print(f"🔀 '{station}'에서 {target}(으)로 환승!")
                    return True
            print(f"❌ 환승할 수 없는 입력이에요: '{raw}'")
            return False

        station = raw.strip()
        if not station or station not in LINES[self.line]:
            print(f"❌ '{station}'은(는) {self.line}에 없는 역이에요!")
            return False
        if station in self.used:
            print(f"❌ '{station}'은(는) 이미 나온 역이에요!")
            return False

        self.used.add(station)
        return True

    def npc_move(self):
        # NPC의 턴
        options = [s for s in LINES[self.line] if s not in self.used]

        if random.random() < MISTAKE_PROB or not options:
            if self.used and random.random() < 0.5:
                return random.choice(list(self.used)), False  # 이미 나온 역 재사용
            other_line = random.choice([l for l in LINES if l != self.line])
            return random.choice(LINES[other_line]), False    # 다른 노선 역

        station = random.choice(options)
        self.used.add(station)
        return station, True

    def run(self):
        print("=" * 40)
        print("  지~하철! 지하철 지~하철! 지하철! 🚇")
        print("=" * 40)

        players = self.players
        print(f"\n🎲 참가자: {', '.join(players)}")
        time.sleep(2)

        caller = random.choice(players)
        print(f"🎤 호선/역을 정할 사람: {caller}")

        if caller == self.name:
            while self.line not in LINES:
                self.line = input("호선 입력 (예: 2호선): ").strip()
            start = ""
            while start not in LINES[self.line]:
                start = input(f"{self.line} 시작역 입력: ").strip()
        else:
            time.sleep(2)
            self.line = random.choice(list(LINES.keys()))
            start = random.choice(LINES[self.line])
            print(f"📣 {caller}님이 [{self.line}] '{start}' 역을 선택했습니다!")

        self.used = {start}
        time.sleep(2)

        others = [p for p in players if p != caller]
        random.shuffle(others)
        order = [caller] + others
        print("🎲 진행 순서: " + " → ".join(order))
        time.sleep(2)
        print(f"\n게임 시작! [{self.line}] '{start}'에서 출발합니다.\n")

        turn = 1  # 0번(caller)은 이미 호선/역을 정하며 턴을 사용함
        while True:
            player = order[turn % len(order)]

            if player == self.name:
                raw = self.wait_for_input(f"[{self.line}] {player}(나)님의 차례 (10초!) ▶ ")
                if raw is None:
                    print(f"\n💥 시간 초과! {player}님, 술 한 잔 원샷! 🍺")
                    return
                if raw in ("종료", "quit", "exit"):
                    print("게임을 종료합니다.")
                    return
                if not self.try_answer(raw):
                    print(f"💥 GAME OVER! {player}님, 술 한 잔 원샷! 🍺")
                    return
            else:
                time.sleep(random.uniform(1, TIMEOUT))
                station, correct = self.npc_move()
                print(f"🗣️ {player}: \"{station}\"")
                if not correct:
                    print(f"💥 GAME OVER! {player}님, 술 한 잔 원샷! 🍺")
                    return

            turn += 1


# main 실행을 위한 함수
def play_game(name):
    npcs = random.sample(PLAYER_POOL, random.randint(1, 3))
    players = [name] + npcs
    SubwayGame(name, players).run()
 
 
# 테스트 용 
if __name__ == "__main__":
    name = input("당신의 이름을 입력해주세요: ").strip() or "나"
    try:
        play_game(name)
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 중단했습니다.")
        sys.exit(0)