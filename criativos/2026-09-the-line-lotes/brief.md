# Leva 1 — THE LINE · lançamento de lotes

**Data:** 2026-09-15
**Objetivo:** lançamento / captação de leads
**Formato:** 5 peças em 1080 × 1080 (feed quadrado)
**Canvas de aprovação:** https://claude.ai/artifact/KuzJMs1zbBSp5UeP8h8u94

## Empreendimento

| Campo | Valor |
|---|---|
| Nome | THE LINE |
| Tipo | Condomínio-clube de lotes (One, Square e Field) |
| Local | Gleba Cafezal, Zona Sul — Londrina/PR |
| Endereço | Estrada Alcides Turini, 1677 |
| Lote mínimo | 250 m² |
| Clube | THE LINE CLUB, 12.650 m² |
| Lazer | piscina 420 m² com raia de 25 m, SPA com piscina aquecida, academia 270 m², 2 quadras de tênis de saibro, padel, beach tennis, quadra esportiva, 3 salões de festas, coworking, gourmet com parrilla |
| Distâncias | 5 min do Muffato · 6 min do Shopping Catuaí |
| Pagamento | parcelamento direto com a loteadora em até 180x |
| Urbanismo | Paysage Corpal |

## Peças

| # | Arquivo | Copy | Render |
|---|---|---|---|
| 1 | `c1-regiao-desejada` | Região mais desejada de Londrina | aérea The Line Square + Club (pg. 35) |
| 2 | `c2-seis-minutos` | 6 minutos do Shopping Catuaí | aérea da região com Londrina ao fundo (pg. 7) |
| 3 | `c3-metragem-rara` | Metragem rara nessa região | família no campo ao pôr do sol (pg. 5) |
| 4 | `c4-clube-12mil` | Clube com mais de 12.000 m² | aérea das quadras + 4 tiles de lazer |
| 5 | `c5-noticia` | Versão notícia da copy 5 | piscina do The Line Club (pg. 19) |

## Direção visual

Sem design system fechado — a direção veio dos próprios materiais do
empreendimento: tipografia geométrica fina em caixa alta com entreletra larga,
branco sobre render escurecido, blocos de informação alinhados e régua fina
como separador.

**Paleta** (amostrada das páginas chapadas do caderno):

| Cor | HEX |
|---|---|
| Terracota | `#B27757` |
| Areia | `#EBDBCE` |
| Musgo | `#868F79` |
| Terra rosé | `#96625D` |
| Fundo escuro | `#121614` / `#1B211D` |

**Tipografia:** Jost (display e texto, substitui a geométrica da marca) ·
Newsreader (manchete da peça 5).

**Marca THE LINE:** o wordmark é o original extraído do caderno. O traço
diagonal foi redesenhado em SVG (o do PDF tem ruído de compressão) e a
assinatura "Um jeito conectado de viver" foi recomposta em tipografia viva
pelo mesmo motivo.

## Pendências

- [ ] **Logo do Emerson** — a peça tem um slot pronto no canto inferior direito. Basta salvar `src/emerson-logo.png` (versão para fundo escuro) e `src/emerson-logo-dark.png` (versão para o fundo creme da peça 5) e rodar `make.py` + `render.py`
- [ ] CRECI e @ — ainda como placeholders entre `[colchetes]` nas 5 peças
- [ ] Logo da Barreto Negócios Imobiliários — não veio no caderno, só nas stories de referência
- [ ] Confirmar se pode usar os renders em peça pública: o caderno marca "uso exclusivo de treinamento / imagens preliminares"

## Checklist

- [x] Lote de 250 m² em todas as peças
- [x] Localização (Gleba Cafezal · Londrina/PR)
- [x] Parcelamento em 180x
- [x] Ressalva "imagens preliminares, meramente ilustrativas"
- [ ] CRECI visível — **bloqueado até receber o número**
- [ ] Valor conferido com o cliente

## Como regerar

```bash
python3 make.py     # monta src/*.html (render) e build/*.dc.html (canvas)
python3 render.py   # exporta entregas/*.png e *.jpg em 1080x1080
```
