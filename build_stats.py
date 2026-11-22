#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""끄투 단어 통계 페이지 생성 (실측치 고정 입력, 2026-11-22 집계)"""
import html, json, urllib.parse

LEN = {1:1418,2:81096,3:138485,4:139119,5:91661,6:73275,7:55131,8:42670,9:29331,
       10:20728,11:14711,12:10361,13:7219,14:5083,15:3481,16:2449,17:1591,18:1089,
       19:746,20:574,21:371,22:284,23:187,24:167,25:122,26:99,27:80,28:65,29:55,
       30:28,31:36,32:25,33:26,34:21,35:15,36:16,37:9,38:7,39:11,40:8,41:8,42:4,
       43:5,44:3,45:2,46:2,47:4,48:1,49:1,50:2,51:1,52:2,53:2,55:1,56:1,57:1,58:2,61:1,76:1}
TOTAL_KO = 721894
TOTAL_ALL = 814025
FIRST_TOP = [("아",10265),("이",9751),("사",8978),("고",7478),("오",7403),("마",6761),
             ("가",6514),("대",6492),("수",5932),("전",5871),("스",5819),("자",5656),
             ("기",5322),("유",5314),("지",5288)]
END_TOP = [("기",17982),("이",16583),("리",16567),("원",15441),("스",14851),("교",13106),
           ("자",11098),("지",10515),("트",10012),("사",9725)]
START_LOW = [("촏",1),("탓",1),("뙁",1),("봋",1),("쑝",1),("픗",1),("왇",1),("돓",1),
             ("옦",1),("슻",1),("돤",1),("뒙",1)]
DEADEND = 2335
GE10 = 69708
GE20 = 2250
THEMES = [("주제없음",314029),("의학",26327),("주제 없음",23558),("소설/시/희곡",20202),
          ("동물의 숲",19688),("역사",19280),("국내 관광지/축제",18401),("쿠키런",17983),
          ("유희왕",17746),("동물",17271),("식물",16195),("직업",16096)]
THEME_DISTINCT = 123
LONGEST = [("추방당한치트부여마술사는자유로운세컨드라이프를구가한다나는무기만이아니라모든것에강화포인트를부여할수있고내마음대로효과를해제할수있는데남은사람들괜찮겠어",76),
 ("약혼파기를노리고기억상실인척했더니냉담하던약혼자가기억을잃기전의넌나에게완전히푹빠져있었다는말도안되는거짓말을하기시작했다",61),
 ("땅거미질때샌디에이고에서로스앤젤레스로운전하며소형디지털녹음기에구술한막연히엘에이운전시들이라고생각하는작품들의모음",58),
 ("티타임을위하여착한사람문성현열린사회와그적들눈사람속의검은항아리씨앗불목마른계절술먹고담배피는엄마목련꽃그늘아래서",58),
 ("인도네시아페칼롱간의바틱박물관과공동수행하는초중고등학교직업학교기술전문학교학생들에대한바틱무형문화유산교육및훈련",57),
 ("최고난이도미궁에서파티에게버려진에스랭크검사정말로헤매다가아무도모르는최심부로내감이맞다면아마도이쪽이출구일거야",56),
 ("이제일하고싶지않습니다모험가따위그만두겠습니다이제와서잘해줄테니돌아오라고해도거절합니다저는절대일하지않습니다",55),
 ("우리다투게돼도이것만기억해줄래눈을맞추고서로가서로의손잡아주며낮은목소리와예쁜말투로상처주지않게노력을하고",53),
 ("산티아고데콤포스텔라성당의칼릭스티누스고사본및리베르상티야콥의중세사본들이베리아에서기원한유럽의야고보전통",53),
 ("광문자전김신선전우상전열녀함양박씨전마장전예덕선생전민옹전은애전유우춘전출동문오대검협전부목한전상사동기",52)]

def kf(n): return f"{n:,}"

def texturl(w): return "https://kkutu.lightstudio.kr/text/" + urllib.parse.quote(w)

# 길이 분포: 1~14 개별, 15 이상 묶음
rows = []
maxn = max(LEN.values())
for L in range(1, 15):
    n = LEN[L]
    rows.append((f"{L}글자", n, n / maxn * 100))
rest = sum(v for k, v in LEN.items() if k >= 15)
rest_cnt = len([k for k in LEN if k >= 15])
rows.append((f"15글자 이상({rest_cnt}종 길이)", rest, rest / maxn * 100))

len_rows = "\n".join(
    f'      <tr><td>{lab}</td><td class="num">{kf(n)}</td>'
    f'<td><span class="bar" style="width:{w:.1f}%"></span></td>'
    f'<td class="num pct">{n / TOTAL_KO * 100:.1f}%</td></tr>'
    for lab, n, w in rows)

def chip_list(items, param="start"):
    return "".join(
        f'<a class="chip" href="https://kkutu.lightstudio.kr/?{param}={urllib.parse.quote(w)}">{w} <b>{kf(n)}</b></a>'
        for w, n in items)

first_chips = chip_list(FIRST_TOP, "start")
end_chips = chip_list(END_TOP, "end")
low_chips = "".join(f'<span class="chip muted">{w} <b>{kf(n)}</b></span>' for w, n in START_LOW)
theme_chips = "".join(f'<span class="chip">{html.escape(t)} <b>{kf(n)}</b></span>' for t, n in THEMES)
long_rows = "\n".join(
    f'      <li><span class="len">{L}</span><a href="{texturl(w)}">{html.escape(w)}</a></li>'
    for w, L in LONGEST)

HTML = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>끄투 단어 통계 — 글자 길이 분포·시작 글자 순위</title>
<meta name="description" content="끄투코리아 단어사전에 등록된 한글 단어 {kf(TOTAL_KO)}개의 실제 통계입니다. 글자 길이 분포, 시작 글자·끝 글자 순위, 이어갈 단어가 없는 단어 수, 가장 긴 단어 목록을 한 페이지에 정리했습니다.">
<link rel="canonical" href="https://ha-am-dev.github.io/kkutu-dict-docs/stats.html">
<style>
  :root{{--ink:#171a1f;--muted:#5c6470;--line:#e6e8ec;--accent:#c9821a;--bg:#fffdf8}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.75 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}}
  main{{max-width:780px;margin:0 auto;padding:56px 22px 96px}}
  h1{{font-size:1.8rem;line-height:1.3;margin:0 0 10px;letter-spacing:-0.02em}}
  p.lead{{color:var(--muted);margin:0 0 26px}}
  h2{{font-size:1.15rem;margin:40px 0 6px}}
  h2 + p.sub{{color:var(--muted);font-size:.93rem;margin:0 0 14px}}
  p{{margin:0 0 14px}}
  a{{color:var(--accent)}}
  code{{background:#f1efe9;padding:2px 5px;border-radius:4px;font-size:.92em}}
  .kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:24px 0 8px}}
  .kpi div{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
  .kpi b{{display:block;font-size:1.45rem;line-height:1.2;letter-spacing:-0.01em}}
  .kpi span{{color:var(--muted);font-size:.86rem}}
  table{{width:100%;border-collapse:collapse;font-size:.94rem;margin:6px 0 4px}}
  th,td{{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:middle}}
  th{{color:var(--muted);font-weight:600;font-size:.86rem}}
  td.num{{white-space:nowrap;font-variant-numeric:tabular-nums}}
  td.pct{{color:var(--muted)}}
  .bar{{display:block;height:8px;border-radius:4px;background:linear-gradient(90deg,#e8b871,#c9821a);min-width:2px}}
  .chips{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px}}
  .chip{{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:.94rem;text-decoration:none;color:var(--ink)}}
  .chip b{{color:var(--accent);font-weight:600;font-size:.86rem}}
  .chip.muted{{color:var(--muted)}}
  .chip:hover{{border-color:#d9c6a8}}
  ol.long{{padding-left:22px}}
  ol.long li{{margin:10px 0;word-break:break-all}}
  ol.long a{{text-decoration:none}}
  .len{{display:inline-block;min-width:34px;margin-right:8px;color:var(--muted);font-size:.85rem;font-variant-numeric:tabular-nums}}
  .note{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:26px 0;font-size:.93rem;color:#3d444e}}
  footer{{margin-top:52px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}}
  @media(max-width:520px){{ td.pct, th.pct{{display:none}} }}
</style>
</head>
<body>
<main>
  <h1>끄투 단어 통계</h1>
  <p class="lead">끝말잇기를 하다 보면 "이 글자로 시작하는 단어가 몇 개나 되나"가 곧 전략이 됩니다. <a href="https://kkutu.lightstudio.kr/">끄투코리아 단어사전</a>에 실제로 등록된 단어를 세어 정리했습니다.</p>

  <div class="kpi">
    <div><b>{kf(TOTAL_KO)}</b><span>한글 단어</span></div>
    <div><b>{kf(TOTAL_ALL)}</b><span>전체 등록 단어</span></div>
    <div><b>{kf(GE10)}</b><span>10글자 이상</span></div>
    <div><b>{kf(DEADEND)}</b><span>이어갈 단어 없음</span></div>
  </div>

  <h2>글자 길이 분포</h2>
  <p class="sub">한글 단어 {kf(TOTAL_KO)}개를 길이별로 센 결과입니다. 3~4글자가 전체의 {((LEN[3]+LEN[4])/TOTAL_KO*100):.0f}%를 차지합니다.</p>
  <table>
    <thead><tr><th>길이</th><th>단어 수</th><th>비중</th><th class="pct">점유율</th></tr></thead>
    <tbody>
{len_rows}
    </tbody>
  </table>
  <p class="sub">20글자 이상도 {kf(GE20)}개 있습니다. <a href="https://kkutu.lightstudio.kr/?min=20">최소 길이를 20으로 두고 검색</a>하면 바로 볼 수 있습니다.</p>

  <h2>시작 글자 순위</h2>
  <p class="sub">그 글자로 시작하는 단어가 많은 순서입니다. 내 차례에 이어가기 쉬운 글자이기도 합니다.</p>
  <div class="chips">{first_chips}</div>

  <h2>끝 글자 순위</h2>
  <p class="sub">그 글자로 끝나는 단어가 많은 순서입니다. 반대로 상대를 막으려면 이 목록에 없는 글자로 끝내는 편이 낫습니다.</p>
  <div class="chips">{end_chips}</div>

  <h2>이어가기 어려운 글자</h2>
  <p class="sub">사전 전체에서 그 글자로 시작하는 단어가 한 개뿐인 글자입니다. 이런 글자로 끝내면 다음 사람은 사실상 선택지가 하나입니다.</p>
  <div class="chips">{low_chips}</div>

  <h2>이어갈 단어가 없는 단어 {kf(DEADEND)}개</h2>
  <p>끝 글자로 시작하는 단어가 사전에 하나도 없는 단어입니다(예: <a href="{texturl('호른')}">호른</a>은 '른'으로 시작하는 단어가 없습니다). 이런 단어를 내면 상대는 그 글자로 이어갈 수 없습니다. 단, 게임 설정에 따라 두음법칙이 적용되면 '려·뇨·류·리' 같은 끝 글자가 '여·요·유·이'로 이어질 수 있으니 실제 판에서는 규칙을 확인하세요.</p>

  <h2>가장 긴 단어</h2>
  <p class="sub">사전에 등록된 순수 한글 단어 중 긴 순서입니다. 길이 제한이 없는 판에서만 쓸 수 있습니다.</p>
  <ol class="long">
{long_rows}
  </ol>

  <h2>주제 분포</h2>
  <p class="sub">주제는 {THEME_DISTINCT}종이 등록되어 있습니다. 단어 수가 많은 주제부터 보면 어느 주제에서 단어를 찾기 쉬운지 감이 옵니다.</p>
  <div class="chips">{theme_chips}</div>

  <div class="note">
    <strong>집계 기준</strong> — 2026년 11월 22일 기준 사전 등록 데이터 전체를 직접 세었습니다.
    '한글 단어'는 한글 음절로만 이루어진 단어이며, 라틴 문자·숫자가 섞인 항목은 제외했습니다.
    이어가기 판정은 사전 원문의 첫 글자·끝 글자를 그대로 비교한 값이라 두음법칙 변형은 반영하지 않았습니다.
  </div>

  <h2>같이 보기</h2>
  <ul>
    <li><a href="https://ha-am-dev.github.io/kkutu-dict-docs/">끄투 사전 조건 검색 사용법</a></li>
    <li><a href="https://ha-am-dev.github.io/kkutu-dict-docs/guide.html">상황별 조건 조합 치트시트</a></li>
    <li><a href="https://kkutu.lightstudio.kr/">끄투코리아 단어사전 열기</a></li>
  </ul>

  <footer>끄투 사전 사용법을 정리한 비공식 안내 문서입니다. · <a href="https://ha-am-dev.github.io/kkutu-dict-docs/">사용법으로</a></footer>
</main>
</body>
</html>
"""

open("stats.html", "w", encoding="utf-8").write(HTML)
print("written", len(HTML), "chars")
print("rest", rest, "rest_cnt", rest_cnt)
