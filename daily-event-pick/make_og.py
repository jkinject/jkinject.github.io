#!/usr/bin/env python3
# 줍줍노트 OG 이미지 (1200x630) — 미니멀 화이트 리스트 톤
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (255, 255, 255)
INK = (25, 27, 31)
MID = (95, 100, 105)
DIM = (162, 167, 173)
LINE = (236, 238, 241)
HOT = (211, 58, 44)

FONT = "/usr/share/fonts/pickle-hwp/NotoSansCJKkr-Regular.otf"

def f(size):
    return ImageFont.truetype(FONT, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text(xy, s, font, fill, bold=0):
    d.text(xy, s, font=font, fill=fill, stroke_width=bold, stroke_fill=fill)

# 상단 브랜드
text((88, 66), "줍줍노트", f(28), INK, bold=1)
text((226, 70), "경품 이벤트", f(23), DIM)

# 헤드라인
text((88, 146), "지금 응모할 수 있는", f(58), INK, bold=1)
text((88, 216), "경품 이벤트", f(58), INK, bold=1)

# 샘플 리스트 (한 줄에 하나)
rows = [
    ("D-1", "모두가 도시농부 만족도 설문  농림수산식품교육문화원", "스타벅스 세트 30명 · ~11.25(화)", True),
    ("D-3", "2026 홈페이지 이용자 만족도 조사  금융감독원", "모바일 상품권 1만원 500명 · ~11.27(금)", True),
    ("D-19", "2026 정부혁신 우수사례 국민투표  행안부", "갤럭시 버즈4 외 882명 · ~12.13(일)", False),
]
y = 330
d.line([(88, y), (1112, y)], fill=LINE, width=1)
for dd, title, meta, hot in rows:
    text((92, y + 22), dd, f(20), HOT if hot else DIM)
    text((172, y + 16), title, f(22), INK)
    text((172, y + 46), meta, f(19), DIM)
    text((1036, y + 22), "응모 →", f(19), MID)
    y += 74
    d.line([(88, y), (1112, y)], fill=LINE, width=1)

text((88, 580), "매일 오전 8시 업데이트 · @daily.event.pick", f(20), DIM)

img.save("assets/og.png", "PNG", optimize=True)
print("saved assets/og.png", img.size)
