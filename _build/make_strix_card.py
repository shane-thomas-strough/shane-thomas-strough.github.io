"""Generate the field study's share image from local text and simple geometry."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images/strix-workflow-report.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

im = Image.new("RGB", (1200, 630), "#080A0C")
d = ImageDraw.Draw(im)

for x in range(0, 1201, 60):
    d.line((x, 0, x, 630), fill="#10202A", width=1)
for y in range(0, 631, 60):
    d.line((0, y, 1200, y), fill="#10202A", width=1)

d.rectangle((55, 54, 1145, 576), fill="#0D1117", outline="#1E2D3D", width=2)
d.rectangle((55, 54, 63, 576), fill="#00E5FF")
d.text((98, 92), "SHANE THOMAS STROUGH  /  ELEVARE FIELD STUDY", font=ImageFont.truetype(BOLD, 23), fill="#C8A96E")
d.text((95, 178), "THE FINDING IS", font=ImageFont.truetype(BOLD, 72), fill="#F0F4F8")
d.text((95, 270), "NOT THE REPORT", font=ImageFont.truetype(BOLD, 72), fill="#00E5FF")
d.line((98, 391, 1095, 391), fill="#1E2D3D", width=2)
d.text((98, 424), "24 LOCAL ATTEMPTS", font=ImageFont.truetype(BOLD, 24), fill="#F0F4F8")
d.text((468, 424), "4 MODELS", font=ImageFont.truetype(BOLD, 24), fill="#F0F4F8")
d.text((731, 424), "2 INVENTED TARGETS", font=ImageFont.truetype(BOLD, 24), fill="#F0F4F8")
d.text((98, 514), "shanestrough.com", font=ImageFont.truetype(FONT, 20), fill="#6B8099")
im.save(OUT, optimize=True)
print(OUT)
