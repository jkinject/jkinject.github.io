# 줍줍노트 · daily-event-pick

인스타그램 `@daily.event.pick` 카드뉴스와 짝을 이루는 **모바일 바로 응모 페이지**입니다.
프로필 링크(`https://jkinject.github.io/daily-event-pick/`)로 들어와 카드에서 바로 기관 응모 페이지로 이동합니다.

- 주소: <https://jkinject.github.io/daily-event-pick/>
- 톤: 다크 에디토리얼 (`#0D1017` 배경 / `#4A8BFF` 포인트 / Pretendard)

## 구조

```
index.html        # 화면 전부 (CSS·JS 인라인, 외부 라이브러리 없음)
data/events.json  # 이벤트 데이터 — 매일 이 파일만 고치면 됩니다
assets/og.jpg     # 공유 미리보기 이미지
```

## 매일 업데이트하는 법

`data/events.json`에서 `days` 배열 맨 앞에 오늘 날짜를 추가합니다. (최신 날짜가 자동으로 첫 탭)

```json
{
  "date": "2026-11-25",
  "label": "오늘",
  "headline": "오늘 마감 임박 경품 이벤트",
  "sub": "5분이면 끝나는 경품 3건 · 마감 빠른 순",
  "events": [
    {
      "id": "org-event-2026",
      "org": "기관명",
      "title": "이벤트명",
      "prize": "경품 (예: 스타벅스 아메리카노 100명)",
      "winners": "100명 추첨",
      "deadline": "2026-11-30",
      "url": "https://...응모페이지...",
      "tip": "참여 팁 한 줄",
      "tag": "설문"
    }
  ]
}
```

- `deadline`만 있으면 **D-day 배지가 자동 계산**됩니다 (D-2 이하 빨강, D-5 이하 주황).
- 투표처럼 페이지가 두 개면 `url2` / `url2_label`을 추가하면 두 번째 버튼이 생깁니다.
- `site.updated_at`을 갱신하면 화면 상단의 업데이트 시각이 바뀝니다.
- 카드 순서는 `deadline` 오름차순으로 자동 정렬됩니다.

## 배포

`main` 브랜치 `/` 루트를 GitHub Pages(legacy)로 서빙합니다. push하면 1분 안에 반영됩니다.

```bash
git add -A && git commit -m "events: 2026-11-25" && git push
```
