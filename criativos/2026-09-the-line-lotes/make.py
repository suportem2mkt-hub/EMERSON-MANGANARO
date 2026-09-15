#!/usr/bin/env python3
"""Gera os 5 criativos THE LINE em duas saidas a partir de uma unica fonte:
   src/*.html      pagina isolada 1080x1080, imagens em alta -> render PNG
   build/*.dc.html artboard do canvas, imagens comprimidas    -> edicao visual
"""
import os, re, shutil, html

W = 1080

# ---------------------------------------------------------------- paleta
# amostrada das paginas chapadas do caderno do corretor
TERRA  = "#B27757"   # terracota
AREIA  = "#EBDBCE"   # creme
MUSGO  = "#868F79"   # verde
ROSE   = "#96625D"   # terra rose
NOITE  = "#121614"   # fundo escuro
CARVAO = "#1B211D"   # bloco escuro

# ---------------------------------------------------------------- pecas
PIN = ('<svg class="pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M12 21.5s6.8-5.7 6.8-11.1a6.8 6.8 0 1 0-13.6 0C5.2 15.8 12 21.5 12 21.5Z"/>'
       '<circle cx="12" cy="10.2" r="2.5"/></svg>')

MARK = ('<svg class="mark" viewBox="0 0 475 104" fill="none" '
        'stroke="currentColor" stroke-width="4.5" stroke-linecap="square">'
        '<path d="M3 98 L295 6 L472 6"/></svg>')


def lockup(w, cls="", tagline=True):
    """marca THE LINE: traco em SVG + wordmark original + assinatura em tipo vivo
    (a assinatura do caderno esta degradada pelo JPEG e nao aguenta ampliacao)"""
    tag = (f'<p class="tagline" style="font-size:{round(w * 0.060, 1)}px">'
           f'Um jeito conectado de viver</p>') if tagline else ""
    return (f'<div class="lockup {cls}" style="width:{w}px">{MARK}'
            f'<img src="theline-only.png" alt="THE LINE">{tag}</div>')


def sig(dark_bg=True):
    s = "" if dark_bg else "-dark"
    return f'''<footer class="sig">
  <div class="sig-brands">
    <img class="sig-tl" src="theline-only{s}.png" alt="THE LINE">
    <span class="sig-div"></span>
    <img class="sig-py" src="paysage{s}.png" alt="Paysage Corpal">
  </div>
  <div class="sig-cor">
    <div class="sig-name">[NOME DO CORRETOR]</div>
    <div class="sig-meta">CRECI [000000-F] &middot; [@INSTAGRAM]</div>
  </div>
</footer>
<p class="legal">Imagens preliminares, meramente ilustrativas.</p>'''


def pin_line(txt):
    return f'<p class="pin-line">{PIN}<span>{txt}</span></p>'


# ---------------------------------------------------------------- css base
BASE = f'''
*,*::before,*::after{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{font-family:'Jost',"Century Gothic","Futura",system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}}
a{{color:{TERRA};text-decoration:none}} a:hover{{color:{ROSE}}}
.frame{{position:relative;width:{W}px;height:{W}px;overflow:hidden;
  background:{NOITE};color:#fff;isolation:isolate}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}}
.scrim{{position:absolute;inset:0;z-index:1}}

.lockup{{display:block}}
.lockup .mark{{display:block;width:100%;height:auto;color:currentColor;
  margin:0 0 4.8%}}
.lockup img{{display:block;width:100%;height:auto}}
.lockup .tagline{{margin:7.4% 0 0;font-weight:400;letter-spacing:.015em;
  line-height:1;text-align:center;white-space:nowrap}}

.eyebrow{{font-size:21px;font-weight:400;letter-spacing:.34em;
  text-transform:uppercase;opacity:.82;margin:0}}
.figure{{font-size:146px;font-weight:200;letter-spacing:-.005em;line-height:.92;
  margin:10px 0 0}}
.figure sup{{font-size:.44em;font-weight:300;top:-.52em;position:relative;
  letter-spacing:0}}
h1{{font-size:53px;font-weight:300;letter-spacing:.155em;line-height:1.32;
  text-transform:uppercase;margin:0;text-wrap:balance}}
.sub{{font-size:27px;font-weight:300;letter-spacing:.05em;line-height:1.5;
  margin:0;opacity:.93;text-wrap:pretty}}
.rule{{width:104px;height:1px;background:currentColor;opacity:.55;border:0;margin:0}}

.pin-line{{display:flex;align-items:center;gap:11px;margin:0;
  font-size:23px;font-weight:400;letter-spacing:.2em;text-transform:uppercase}}
.pin{{width:23px;height:23px;flex:none;opacity:.9}}
.pay{{font-size:25px;font-weight:300;letter-spacing:.045em;margin:0;opacity:.92}}

.sig{{display:flex;align-items:flex-end;justify-content:space-between;gap:24px}}
.sig-brands{{display:flex;align-items:center;gap:22px}}
.sig-tl{{height:25px;width:auto;display:block}}
.sig-py{{height:40px;width:auto;display:block}}
.sig-div{{width:1px;height:34px;background:currentColor;opacity:.3;display:block}}
.sig-cor{{text-align:right}}
.sig-name{{font-size:23px;font-weight:400;letter-spacing:.13em;text-transform:uppercase}}
.sig-meta{{font-size:18px;font-weight:300;letter-spacing:.1em;opacity:.72;margin-top:4px}}
.legal{{font-size:15px;font-weight:300;letter-spacing:.055em;opacity:.55;margin:14px 0 0}}
'''

# ================================================================ C1
C1_CSS = f'''
.c1 .scrim{{background:
  linear-gradient(to right,rgba(8,12,10,.60) 0%,rgba(8,12,10,.18) 46%,rgba(8,12,10,0) 72%),
  linear-gradient(to top,rgba(8,12,10,.96) 0%,rgba(8,12,10,.92) 30%,
  rgba(8,12,10,.70) 47%,rgba(8,12,10,.30) 63%,rgba(8,12,10,.08) 76%,
  rgba(8,12,10,.52) 100%)}}
.c1 .wrap{{position:relative;z-index:2;height:100%;padding:62px 74px 54px;
  display:flex;flex-direction:column}}
.c1 .top{{display:flex;justify-content:center}}
.c1 .body{{margin-top:auto;display:flex;flex-direction:column;gap:26px}}
.c1 .meta{{display:flex;flex-direction:column;gap:12px;margin-top:4px}}
.c1 .sig{{margin-top:40px}}
.c1 .figure{{font-size:132px}}
.c1 h1{{font-size:50px}}
'''
C1 = f'''<div class="frame c1">
<img class="bg" src="c1-aerea.jpg" alt="">
<div class="scrim"></div>
<div class="wrap">
  <div class="top">{lockup(300)}</div>
  <div class="body">
    <div>
      <p class="eyebrow">Lotes de</p>
      <p class="figure">250<sup>m²</sup></p>
    </div>
    <hr class="rule">
    <h1>Em uma das regiões<br>mais desejadas<br>de Londrina</h1>
    <div class="meta">
      {pin_line("Gleba Cafezal &middot; Londrina/PR")}
      <p class="pay">Parcelamento direto com a loteadora em até 180x</p>
    </div>
  </div>
  {sig()}
</div>
</div>'''

# ================================================================ C2
C2_CSS = f'''
.c2{{display:flex;flex-direction:column;background:{CARVAO}}}
.c2 .photo{{position:relative;height:600px;flex:none;overflow:hidden}}
.c2 .photo .scrim{{background:
  linear-gradient(to top,rgba(18,22,20,.80) 0%,rgba(18,22,20,.06) 42%,
  rgba(18,22,20,.42) 100%)}}
.c2 .photo .top{{position:absolute;z-index:2;top:52px;left:0;right:0;
  display:flex;justify-content:center}}
.c2 .chip{{position:absolute;z-index:2;left:74px;bottom:38px;
  display:flex;align-items:center;gap:11px;
  font-size:21px;font-weight:400;letter-spacing:.24em;text-transform:uppercase}}
.c2 .panel{{flex:1;padding:52px 74px 50px;display:flex;flex-direction:column;
  background:{CARVAO}}}
.c2 h1{{font-size:50px}}
.c2 .panel .rule{{margin:30px 0 26px}}
.c2 .meta{{display:flex;flex-direction:column;gap:12px}}
.c2 .sig{{margin-top:auto;padding-top:34px}}
'''
C2 = f'''<div class="frame c2">
<div class="photo">
  <img class="bg" src="c2-londrina.jpg" alt="">
  <div class="scrim"></div>
  <div class="top">{lockup(276)}</div>
  <div class="chip">{PIN}<span>Zona Sul &middot; Londrina/PR</span></div>
</div>
<div class="panel">
  <h1>More a 6 minutos do<br>Shopping Catuaí</h1>
  <hr class="rule">
  <div class="meta">
    <p class="sub">Lotes a partir de 250 m² em condomínio<br>fechado estilo clube, na Gleba Cafezal.</p>
    <p class="pay">Parcelamento direto com a loteadora em até 180x</p>
  </div>
  {sig()}
</div>
</div>'''

# ================================================================ C3
C3_CSS = f'''
.c3 .scrim{{background:
  linear-gradient(to bottom,rgba(26,16,10,.88) 0%,rgba(26,16,10,.84) 40%,
  rgba(26,16,10,.40) 57%,rgba(26,16,10,.16) 70%,rgba(20,12,7,.62) 83%,
  rgba(16,10,6,.93) 92%,rgba(14,9,5,.96) 100%)}}
.c3 .wrap{{position:relative;z-index:2;height:100%;padding:60px 74px 54px;
  display:flex;flex-direction:column;align-items:center;text-align:center}}
.c3 .body{{margin-top:40px;display:flex;flex-direction:column;align-items:center;
  gap:26px;width:100%}}
.c3 h1{{font-size:56px;letter-spacing:.17em}}
.c3 .sub{{max-width:760px}}
.c3 .meta{{display:flex;flex-direction:column;align-items:center;gap:12px}}
.c3 .sig{{margin-top:auto;width:100%}}
.c3 .legal{{width:100%;text-align:left}}
'''
C3 = f'''<div class="frame c3">
<img class="bg" src="c3-campo.jpg" alt="">
<div class="scrim"></div>
<div class="wrap">
  {lockup(272)}
  <div class="body">
    <h1>Uma metragem rara<br>nessa região</h1>
    <hr class="rule">
    <div class="meta">
      <p class="sub">Lotes a partir de <strong style="font-weight:400">250 m²</strong><br>em condomínio fechado estilo clube</p>
      {pin_line("Gleba Cafezal &middot; Londrina/PR")}
      <p class="pay">Parcelamento direto com a loteadora em até 180x</p>
    </div>
  </div>
  {sig()}
</div>
</div>'''

# ================================================================ C4
C4_CSS = f'''
.c4{{display:flex;flex-direction:column;background:{CARVAO}}}
.c4 .head{{flex:none;padding:46px 74px 30px;display:flex;
  align-items:flex-end;justify-content:space-between;gap:30px}}
.c4 .head h1{{font-size:44px;letter-spacing:.14em;line-height:1.3}}
.c4 .head-tl{{width:206px;height:auto;display:block;margin-bottom:6px;flex:none}}
.c4 .hero{{position:relative;height:396px;flex:none;overflow:hidden}}
.c4 .hero .scrim{{background:linear-gradient(to top,rgba(18,22,20,.55),rgba(18,22,20,0) 45%)}}
.c4 .tiles{{flex:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;
  padding:6px 0 0}}
.c4 .tile{{position:relative;height:172px;overflow:hidden}}
.c4 .tile img{{width:100%;height:100%;object-fit:cover;display:block}}
.c4 .tile span{{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 13px;
  font-size:17px;font-weight:400;letter-spacing:.2em;text-transform:uppercase;
  text-align:center;background:linear-gradient(to top,rgba(14,18,16,.88),rgba(14,18,16,0))}}
.c4 .foot{{flex:1;padding:34px 74px 50px;display:flex;flex-direction:column}}
.c4 .amen{{font-size:25px;font-weight:300;letter-spacing:.075em;margin:0 0 16px;
  color:{AREIA}}}
.c4 .meta{{display:flex;align-items:center;justify-content:space-between;gap:24px;
  padding-bottom:26px;border-bottom:1px solid rgba(255,255,255,.18)}}
.c4 .sig{{margin-top:26px}}
'''
C4_TILES = [("c4-piscina.jpg", "Piscinas"), ("c4-academia.jpg", "Academia"),
            ("c4-tenis.jpg", "Tênis"), ("c4-beach.jpg", "Beach tennis")]
C4 = f'''<div class="frame c4">
<div class="head">
  <h1>Lote de 250 m²<br>em clube com mais<br>de 12.000 m²</h1>
  <img class="head-tl" src="theline-only.png" alt="THE LINE">
</div>
<div class="hero">
  <img class="bg" src="c4-aerea-clube.jpg" alt="">
  <div class="scrim"></div>
</div>
<div class="tiles">
  {"".join(f'<div class="tile"><img src="{f}" alt=""><span>{t}</span></div>' for f, t in C4_TILES)}
</div>
<div class="foot">
  <p class="amen">Piscinas &middot; SPA &middot; Academia &middot; Tênis &middot; Padel &middot; Beach tennis e mais</p>
  <div class="meta">
    {pin_line("Gleba Cafezal &middot; Londrina/PR")}
    <p class="pay" style="margin:0">Em até 180x direto com a loteadora</p>
  </div>
  {sig()}
</div>
</div>'''

# ================================================================ C5  (noticia)
C5_CSS = f'''
.c5{{display:flex;flex-direction:column;background:{AREIA};color:#20241f}}
.c5 .tag{{flex:none;display:flex;align-items:center;justify-content:space-between;
  gap:20px;padding:20px 74px;background:{TERRA};color:#fff}}
.c5 .tag .kind{{display:flex;align-items:center;gap:13px;
  font-size:22px;font-weight:500;letter-spacing:.3em;text-transform:uppercase}}
.c5 .dot{{width:11px;height:11px;border-radius:50%;background:#fff;flex:none}}
.c5 .tag .where{{font-size:19px;font-weight:300;letter-spacing:.22em;
  text-transform:uppercase;opacity:.92}}
.c5 .head{{flex:none;padding:44px 74px 34px}}
.c5 .head h2{{font-family:'Newsreader',"Georgia",serif;font-size:63px;font-weight:600;
  letter-spacing:-.012em;line-height:1.1;margin:0;text-wrap:balance;color:#191d18}}
.c5 .lead{{font-size:26px;font-weight:300;letter-spacing:.012em;line-height:1.52;
  margin:22px 0 0;color:#3c433a;text-wrap:pretty}}
.c5 .lead strong{{font-weight:500;color:#20241f}}
.c5 .photo{{position:relative;height:352px;flex:none;overflow:hidden}}
.c5 .photo img{{width:100%;height:100%;object-fit:cover;display:block}}
.c5 .cap{{position:absolute;left:0;right:0;bottom:0;padding:44px 74px 14px;color:#fff;
  font-size:17px;font-weight:300;letter-spacing:.08em;
  background:linear-gradient(to top,rgba(14,18,16,.8),rgba(14,18,16,0))}}
.c5 .foot{{flex:1;padding:30px 74px 46px;display:flex;flex-direction:column}}
.c5 .facts{{display:flex;align-items:center;gap:0;margin:0 0 auto;
  border-top:1px solid rgba(32,36,31,.22);border-bottom:1px solid rgba(32,36,31,.22)}}
.c5 .fact{{flex:1;padding:18px 0}}
.c5 .fact + .fact{{border-left:1px solid rgba(32,36,31,.16);padding-left:26px}}
.c5 .fact b{{display:block;font-size:31px;font-weight:300;letter-spacing:.01em}}
.c5 .fact span{{display:block;font-size:16px;font-weight:400;letter-spacing:.16em;
  text-transform:uppercase;opacity:.62;margin-top:3px}}
.c5 .sig{{margin-top:26px}}
.c5 .sig-div{{opacity:.28}}
.c5 .legal{{opacity:.5}}
'''
C5 = f'''<div class="frame c5">
<div class="tag">
  <span class="kind"><span class="dot"></span>Notícia</span>
  <span class="where">Londrina &middot; Zona Sul</span>
</div>
<div class="head">
  <h2>Gleba Cafezal vai receber lotes de 250 m² em condomínio estilo clube</h2>
  <p class="lead">A 5 minutos do Muffato e a 6 minutos do Shopping Catuaí, a região
  passa a ter uma metragem que até agora não estava disponível por lá.
  <strong>Parcelamento direto com a loteadora em até 180x.</strong></p>
</div>
<div class="photo">
  <img src="c5-piscina.jpg" alt="">
  <div class="cap">THE LINE CLUB &middot; piscina de 420 m² com raia de 25 metros</div>
</div>
<div class="foot">
  <div class="facts">
    <div class="fact"><b>250 m²</b><span>Lote mínimo</span></div>
    <div class="fact"><b>12.000 m²</b><span>De clube</span></div>
    <div class="fact"><b>180x</b><span>Direto com a loteadora</span></div>
  </div>
  {sig(dark_bg=False)}
</div>
</div>'''

# ---------------------------------------------------------------- build
CREATIVES = [
    ("Main",     "c1-regiao-desejada",  C1, C1_CSS),
    ("Catuai",   "c2-seis-minutos",     C2, C2_CSS),
    ("Metragem", "c3-metragem-rara",    C3, C3_CSS),
    ("Clube",    "c4-clube-12mil",      C4, C4_CSS),
    ("Noticia",  "c5-noticia",          C5, C5_CSS),
]

GF = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
      'family=Jost:wght@200;300;400;500&'
      'family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap">')

os.makedirs("build", exist_ok=True)

for board, slug, body, extra in CREATIVES:
    css = BASE + extra
    # 1) pagina isolada para render PNG (fontes locais)
    open(f"src/{slug}.html", "w").write(
        f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        f'<title>THE LINE &mdash; {slug}</title>'
        f'<link rel="stylesheet" href="fonts.css">'
        f'<style>{css}</style></head><body>{body}</body></html>')
    # 2) artboard do canvas
    open(f"build/{board}.dc.html", "w").write(
        f'<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n'
        f'<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n'
        f'<helmet>\n{GF}\n<style>{css}</style>\n</helmet>\n{body}\n</x-dc>\n'
        f'</body>\n</html>\n')

print("gerados:", ", ".join(s for _, s, _, _ in CREATIVES))
