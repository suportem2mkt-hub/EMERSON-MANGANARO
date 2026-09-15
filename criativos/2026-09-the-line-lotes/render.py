#!/usr/bin/env python3
"""Renderiza cada src/*.html em PNG 1080x1080 (captura em 2x e reduz)."""
import os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SRC = os.path.abspath("src")
OUT = os.path.abspath("entregas")
SIZE = 1080
os.makedirs(OUT, exist_ok=True)

pages = sorted(f for f in os.listdir(SRC) if f.endswith(".html"))
if len(sys.argv) > 1:
    pages = [p for p in pages if any(a in p for a in sys.argv[1:])]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--font-render-hinting=none"])
    ctx = b.new_context(viewport={"width": SIZE, "height": SIZE}, device_scale_factor=2)
    pg = ctx.new_page()
    for f in pages:
        pg.goto(f"file://{SRC}/{f}")
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(350)
        tmp = f"/tmp/claude-0/{f}.png"
        pg.locator(".frame").screenshot(path=tmp)
        im = Image.open(tmp).convert("RGB")
        if im.size != (SIZE, SIZE):
            im = im.resize((SIZE, SIZE), Image.LANCZOS)
        name = f.replace(".html", "")
        im.save(f"{OUT}/{name}.png")
        im.save(f"{OUT}/{name}.jpg", quality=92, subsampling=0, progressive=True)
        print(f"{name}  {os.path.getsize(f'{OUT}/{name}.png')//1024}KB png")
    b.close()
