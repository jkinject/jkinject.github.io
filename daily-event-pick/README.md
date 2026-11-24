# 줍줍노트 · daily-event-pick

인스타그램 `@daily.event.pick` 카드뉴스와 짝을 이루는 **경품 이벤트 링크 모음**입니다.
프로필 링크(`https://jkinject.github.io/daily-event-pick/`)로 들어와 목록 한 줄을 누르면 기관 응모 페이지가 새 창으로 열립니다.

- 주소: <https://jkinject.github.io/daily-event-pick/>
- 톤: 화이트 미니멀 리스트 (`#FFFFFF` 배경 / `#191B1F` 본문 / `#EAECEF` 1px 라인 / Pretendard)
- 한 이벤트 = 한 줄. D-day·이벤트명(기관명)·핵심 경품·마감일·`응모 →` 만 표시합니다.
- 수십 건이 쌓여도 한 화면에 8~10건이 들어갑니다.

## 구조

```
index.html        # 화면 전부 (CSS·JS 인라인, 외부 라이브러리 없음)
data/events.json  # 이벤트 데이터 — 매일 이 파일만 고치면 됩니다
assets/og.png     # 공유 미리보기 이미지 (make_og.py로 재생성)
make_og.py        # OG 이미지 생성 스크립트 (선택)
```

## 화면 기능

- **필터 탭**: `진행중` / `마감임박`(오늘·내일 마감, D-1 이하) / `신규`(가장 최근 업데이트 날짜로 등록된 건) / `마감`(오늘 기준 마감 1~30일 지난 건). 탭 옆 건수는 모바일에서도 보입니다.
- **`신규` 기준**: 오늘 날짜가 아니라 `days[].date` 중 오늘 이전의 **가장 최근 날짜**입니다. 자정부터 그날 업데이트 전까지도 탭이 비지 않습니다.
- **탭별 제목·설명**: 탭을 누르면 상단 제목·설명이 바뀝니다. (진행중 `지금 응모할 수 있는 경품` / 마감임박 `곧 마감되는 경품` / 신규 `새로 올라온 경품` / 마감 `최근 30일 마감된 경품`)
- **상단 고정 순서**: ① `오늘픽` → ② 나머지, 각 묶음 안에서는 선택한 정렬순(기본 마감임박순). `오늘픽`은 오늘 마감(`D-DAY`) 건보다도 위에 둡니다. (`마감` 탭은 고정하지 않음)
- **오늘픽 배지**: `featured_date`가 가장 최근인 이벤트(=그날 인스타 카드뉴스에서 소개한 건)에 `오늘픽` 배지가 붙습니다. (`신규` 탭과 헷갈리지 않도록 예전 `NEW`에서 이름을 바꿨습니다. CSS 클래스는 `.pick`)
- **AI 비서에게 맡기기**: 제목 아래 상자의 `문장 복사`를 누르면 AI 비서(피클 등)에게 보낼 문장이 복사됩니다. AI 가 읽는 목록은 `https://event.lalatap.kr/llms.txt`(텍스트)·`/ai.json`(JSON) — Worker 가 `events.json` 에서 진행 중인 건만 뽑아 그때그때 만듭니다. 이벤트에 `how`(참여 방법 한 줄)·`needs`(필요한 것) 필드가 있으면 거기에 함께 나갑니다.
- **TIP 줄**: `tip` 필드가 있으면 경품 줄 아래에 `TIP` 라벨과 함께 한 줄로 보여 줍니다. (예: `모두의 광장 로그인 필요`)
- **오류 제보**: 각 행의 `제보`를 누르면 제보 창이 열립니다(사유 5가지 + 선택 메모). 하단의 `제보해 주세요`는 특정 이벤트 없이 누락·사이트 오류를 받는 창입니다. 제보한 이벤트는 `localStorage` `reported_events_v1`에 기록되어 `제보됨`으로 바뀝니다. 접수는 `https://event.lalatap.kr/api/report`(Cloudflare Worker `event-lalatap`, KV 90일 보관)로 보냅니다. → 아래 「커스텀 도메인·Worker」 참고.
- **경품 아이콘**: 각 행의 경품 앞에 18×18 인라인 SVG 아이콘(커피·상품권·치킨·버거·배달·디지털·기타)이 붙습니다. 이모지는 쓰지 않습니다. `icon` 필드가 있으면 그것을, 없으면 `prize` 문구에서 먼저 나오는 키워드로 자동 판별합니다.
- **행 구조**: 행은 `<div class="row">`이고 제목(`a.t.go`)이 `::after`로 행 전체를 덮는 링크입니다. `제보` 버튼만 그 위(z-index)에 올라옵니다.
- **방문 표시**: 행(또는 `결과보기` 링크)을 누르면 그 이벤트를 `localStorage` `visited_events_v1`에 기록하고, 행 배경과 글자 톤만 은은하게 바뀝니다(체크·라벨 표시 없음). 새로고침해도 유지됩니다.
- **마감 탭 행 우측**: `result_url`이 있으면 `결과보기 →`(새 창), 없으면 링크 없는 `개별발표`(행 클릭 반응 없음)로 표시합니다.
- **정렬 토글**: `마감임박순`(기본, 마감 30일 탭에서는 `최근 마감순`) ↔ `최신순`(등록일 기준)
- **D-day 자동 계산**: `deadline`과 오늘(KST)을 비교해 `D-5` / `D-DAY` / `마감`을 계산합니다. D-3 이하만 은은한 레드.
- **마감 처리**: 마감일이 지난 건은 `진행중` 목록에서 빠지고, `마감 30일` 탭에서 최근 마감순으로 보입니다. **마감 후 30일이 지난 건은 어느 탭에도 나오지 않습니다.**
- **전체 노출**: 선택한 탭의 항목을 페이지 나눔 없이 처음부터 끝까지 한 번에 보여줍니다.
- **링크가 두 개인 이벤트**: 한 행에 버튼을 우겨넣지 않고 제목에 구분을 붙인 **두 개의 행**으로 나눠 넣습니다(예: `2026 정부혁신 우수사례 국민투표 (차관급)` / `(장관급)`). 방문 표시도 행마다 따로 붙습니다.

## 데이터 형식

`data/events.json`에서 `days` 배열 맨 앞에 오늘 날짜를 추가합니다.

```json
{
  "date": "2026-11-25",
  "events": [
    {
      "id": "org-event-2026",
      "org": "기관명",
      "title": "이벤트명",
      "prize": "스타벅스 아메리카노 세트",
      "winners": "30명 추첨",
      "deadline": "2026-11-30",
      "url": "https://...응모페이지...",
      "tag": "설문",
      "tip": "참여 팁 (선택)"
    }
  ]
}
```

| 필드 | 필요 | 설명 |
| --- | --- | --- |
| `org` | ✔ | 기관명 — 이벤트명 뒤에 회색으로 붙습니다 |
| `title` | ✔ | 이벤트명 |
| `prize` | ✔ | 핵심 경품 한 줄 |
| `winners` | | 당첨 인원 — 경품 뒤에 이어 붙습니다 |
| `deadline` | ✔ | `YYYY-MM-DD` — D-day·마감일·정렬에 사용 |
| `url` | ✔ | 응모 링크 |
| `id` | | 중복 제거 키 (없으면 `url` 사용) |
| `featured_date` | | `YYYY-MM-DD` — 이 날짜로 소개한 건은 `오늘픽` 배지와 함께 맨 위에 고정됩니다 (인스타 카드뉴스 발행 회차) |
| `icon` | | 경품 아이콘 강제 지정: `coffee` / `giftcard` / `chicken` / `burger` / `delivery` / `tech` / `gift` (없으면 `prize` 문구로 자동 판별) |
| `result_url` | | 마감 후 결과·당첨자 공개 페이지 주소. 있으면 `마감` 탭 행 우측이 `결과보기 →` 링크가 되고, 없으면 `개별발표`로 표시 |
| `tip` | | 참여 팁 한 줄 — 경품 줄 아래 `TIP`으로 표시 (로그인 필요 여부, 문항 수, 소요 시간 등) |
| `tag` | | 저장만 되고 목록에는 표시하지 않음 |

- `days[]` 대신 최상위 `events[]` 평면 배열도 읽습니다.
- 같은 `id`(또는 `url`)가 여러 날짜에 있으면 **가장 최근 날짜의 내용**만 남습니다.
- `site.updated_at`을 갱신하면 하단 업데이트 시각이 바뀝니다.

## 배포

`main` 브랜치 `/` 루트를 GitHub Pages(legacy)로 서빙합니다. push하면 1분 안에 반영됩니다.

```bash
git add -A && git commit -m "events: 2026-11-25" && git push
```

## 커스텀 도메인·Worker

- 공개 주소: <https://event.lalatap.kr/> — Cloudflare Worker `event-lalatap`이 이 폴더(`jkinject.github.io/daily-event-pick/*`)를 그대로 프록시합니다. GitHub Pages 설정(커스텀 도메인)은 건드리지 않습니다.
- **Web Analytics**: Worker가 HTML 응답 끝에 Cloudflare Web Analytics 비콘을 넣습니다. `index.html`에는 스크립트를 넣지 않습니다(집계는 `event.lalatap.kr` 접속분만).
- **오류 제보 API**: `POST https://event.lalatap.kr/api/report` (JSON: `id`, `title`, `org`, `url`, `deadline`, `reason`, `message`, `page`). KV `event-lalatap-reports`에 90일 보관, IP당 시간당 5건·하루 전체 200건 제한. 허용 Origin은 `event.lalatap.kr`, `jkinject.github.io`.
- **제보 확인**: `https://event.lalatap.kr/api/reports?token=<ADMIN_TOKEN>` (목록·삭제, `&format=json` 지원). 토큰과 Worker 소스는 저장소 밖(로컬 `event-lalatap-worker/`)에 있습니다.
