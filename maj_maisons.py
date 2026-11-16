#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys

p = 'index.html'
s = open(p, encoding='utf-8').read()
orig_len = len(s)

def rep(old, new, label):
    global s
    assert s.count(old) == 1, f"ÉCHEC {label}: trouvé {s.count(old)} fois"
    s = s.replace(old, new)
    print(f"OK  {label}")

HEART = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg><span class="lk-n">0</span>'
HEART_CELL = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg><span>0</span>'

# ============ 1. Suppression de la topbar ============
rep('''<div class="topbar"><div class="topbar-in">
  <div class="logo">Maison <em>pour Chabatt</em></div>
  <div class="filters">
    <button class="fbtn active" data-f="all">Tout</button>
    <button class="fbtn" data-f="landes">Landes</button>
    <button class="fbtn" data-f="bearn">Béarn & Pyrénées</button>
    <button class="fbtn" data-f="gers">Gers</button>
    <button class="fbtn" data-f="dordogne">Dordogne & Sud</button>
  </div>
  <span class="userchip" id="userchip"></span>
</div></div>

''', '', 'HTML topbar')

rep('''/* ===== Topbar ===== */
.topbar{position:sticky;top:12px;z-index:50;max-width:1160px;margin:12px auto 0;padding:0 24px}
.topbar-in{display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:rgba(255,255,255,.72);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid rgba(0,0,0,.04);border-radius:999px;padding:10px 12px 10px 22px;box-shadow:0 4px 20px rgba(0,0,0,.05)}
.logo{font-weight:700;font-size:.95rem;letter-spacing:-.01em}
.logo em{font-style:normal;color:var(--green2)}
.filters{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
.fbtn{border:none;background:transparent;color:var(--muted);padding:8px 15px;border-radius:999px;font-size:.8rem;font-weight:600;cursor:pointer;transition:all .2s;font-family:'Onest',sans-serif}
.fbtn:hover{background:#EFEFEA;color:var(--ink)}
.fbtn.active{background:#111;color:#fff}
.userchip{display:none;align-items:center;gap:6px;background:#111;color:#fff;font-size:.78rem;font-weight:600;padding:8px 14px;border-radius:999px}
''', '', 'CSS topbar')

rep('''  .topbar{padding:0 10px;top:8px}
  .topbar-in{gap:8px;padding:8px 8px 8px 16px}
  .logo{font-size:.88rem}
  .filters{gap:4px}
  .fbtn{padding:7px 11px;font-size:.73rem}
''', '', 'CSS topbar mobile')

rep('  .userchip{padding:7px 10px;font-size:.72rem}\n', '', 'CSS userchip mobile')

rep('''document.querySelectorAll('.fbtn').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.fbtn').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  const f=b.dataset.f;
  document.querySelectorAll('article.card').forEach(c=>{c.classList.toggle('hidden', f!=='all' && c.dataset.zone!==f);});
}));

''', '', 'JS filtres')

rep('''  const u=document.getElementById('userchip');
  if(user){u.textContent='♥ '+user;u.style.display='inline-flex';}''',
'''  const u=document.getElementById('userchip');
  if(u&&user){u.textContent='♥ '+user;u.style.display='inline-flex';}''', 'garde userchip')

# ============ 2. Carte #4 → Ithurrondoa ============
old4 = '''<article class="card" data-zone="bearn" id="g4">
  <button class="like" data-id="4" title="Liker cette maison"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg><span class="lk-n">0</span></button>
  <div class="card-top">
    <div class="rank">04</div>
    <div class="title-wrap">
      <h2>Gîte des Mousquetaires <span class="pill pill-blue">Aux pieds des Pyrénées</span></h2>
      <div class="meta"><span class="meta-item"><i class="dot d-black"></i>Lanne-en-Barétous — vallée de Barétous</span><span class="meta-item"><i class="dot d-gray"></i>≈ 1h55 de Biscarrosse</span><span class="meta-item"><i class="dot d-blue"></i>Dans les contreforts</span><span class="meta-item"><i class="dot d-gray"></i>15 couchages ⚠️</span></div>
    </div>
    <div class="price"><div class="per">60 €<span>/pers</span></div><div class="tot">≈ 970 € · 2 nuits</div></div>
  </div>
  <div class="mosaic"><img src="img/des-mousquetaires1.webp" alt="Gîte des Mousquetaires — photo 1" onclick="zoom(this.src)" loading="lazy"><img src="img/des-mousquetaires2.webp" alt="Gîte des Mousquetaires — photo 2" onclick="zoom(this.src)" loading="lazy"><img src="img/des-mousquetaires3.webp" alt="Gîte des Mousquetaires — photo 3" onclick="zoom(this.src)" loading="lazy"><img src="img/des-mousquetaires4.webp" alt="Gîte des Mousquetaires — photo 4" onclick="zoom(this.src)" loading="lazy"></div>
  <div class="card-body">
    <div class="features"><h4>Le bien</h4><ul><li>Joli chalet de 230 m² · 7 chambres · 5 salles d'eau</li><li>Grande cheminée à foyer ouvert + comptoir bar</li><li>Au bord d'un ruisseau, terrain arboré de 3 200 m²</li><li>Classé 3 étoiles · 1 chambre PMR</li></ul></div>
    <div class="invoice"><h4>Prix · 2 nuits · 31/12 → 02/01</h4><table><tr><td>Week-end (haute saison)</td><td>650 €</td></tr><tr><td>Ménage fin de séjour</td><td>120 €</td></tr><tr><td>Draps (option, 16 × 10 €)</td><td>≈ 160 €</td></tr><tr><td>Taxe de séjour</td><td>≈ 37 €</td></tr><tr class="total"><td>Total ÷ 16 pers</td><td>≈ 970 € → <b>60 €/pers</b></td></tr></table></div>
  </div>
  <div class="card-foot">
    <div class="party ask"><span class="pdot"></span><div><b>Soirée à confirmer</b> — Maison isolée dans la vallée, parfaite pour la fête — mais 15 couchages : prévoir l'appoint pour la 16ᵉ personne.</div></div>
    <div class="actions"><a class="btn primary" href="https://www.grandsgites.com/gite-64-des-mousquetaires-6712.htm" target="_blank">Voir la fiche &amp; contacter ↗</a></div>
  </div>
</article>'''

def mosaic(slug, alt):
    return '<div class="mosaic">' + ''.join(
        f'<img src="img/{slug}{i}.webp" alt="{alt} — photo {i}" onclick="zoom(this.src)" loading="lazy">'
        for i in (1,2,3,4)) + '</div>'

new4 = f'''<article class="card" data-zone="bearn" id="g4">
  <button class="like" data-id="21" title="Liker cette maison">{HEART}</button>
  <div class="card-top">
    <div class="rank">04</div>
    <div class="title-wrap">
      <h2>Ithurrondoa <span class="pill pill-blue">Grand salon</span></h2>
      <div class="meta"><span class="meta-item"><i class="dot d-black"></i>Masparraute — Pays Basque intérieur</span><span class="meta-item"><i class="dot d-gray"></i>≈ 1h40 de Biscarrosse</span><span class="meta-item"><i class="dot d-blue"></i>Pyrénées à ~45 min</span><span class="meta-item"><i class="dot d-gray"></i>15 couchages*</span></div>
    </div>
    <div class="price"><div class="per">52 €<span>/pers</span></div><div class="tot">≈ 780 € · 2 nuits</div></div>
  </div>
  {mosaic('ithurrondoa','Ithurrondoa')}
  <div class="card-body">
    <div class="features"><h4>Le bien</h4><ul><li>Maison basque rénovée · <b>grand salon</b> avec canapé panoramique + salle à manger sous poutres</li><li>Terrasse couverte : ping-pong et longue table de banquet</li><li>Piscine privée · draps fournis · ouvert jusqu'en décembre</li><li>Au calme, entre coteaux et forêts du Pays Basque intérieur</li></ul></div>
    <div class="invoice"><h4>Prix · 2 nuits · 31/12 → 02/01</h4><table><tr><td>Week-end fin d'année (à partir de)</td><td>620 €</td></tr><tr><td>Ménage fin de séjour</td><td>120 €</td></tr><tr><td>Taxe de séjour</td><td>≈ 40 €</td></tr><tr class="total"><td>Total ÷ 15 pers</td><td>≈ 780 € → <b>52 €/pers</b></td></tr></table></div>
  </div>
  <div class="card-foot">
    <div class="party ask"><span class="pdot"></span><div><b>Soirée à confirmer</b> — Gîte familial au calme, ouvert jusqu'en décembre — confirmez simplement la soirée du 31 avec la propriétaire.</div></div>
    <div class="actions"><a class="btn primary" href="https://www.grandsgites.com/gite-64-ithurrondoa-1876.htm" target="_blank">Voir la fiche &amp; contacter ↗</a><span class="btn ghost">📞 06 85 14 48 46</span></div>
  </div>
</article>'''

rep(old4, new4, 'carte #4 → Ithurrondoa')

# ============ 3. Carte #5 → Maison Sagardian ============
old5 = '''<article class="card" data-zone="bearn" id="g5">
  <button class="like" data-id="5" title="Liker cette maison"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg><span class="lk-n">0</span></button>
  <div class="card-top">
    <div class="rank">05</div>
    <div class="title-wrap">
      <h2>Le Garaïbie <span class="pill pill-blue">Aux pieds des Pyrénées</span></h2>
      <div class="meta"><span class="meta-item"><i class="dot d-black"></i>Ordiarp — Soule, forêt des Arbailles</span><span class="meta-item"><i class="dot d-gray"></i>≈ 2h05 de Biscarrosse</span><span class="meta-item"><i class="dot d-blue"></i>En montagne (col de Napal)</span><span class="meta-item"><i class="dot d-gray"></i>32 couchages</span></div>
    </div>
    <div class="price"><div class="per">62 €<span>/pers</span></div><div class="tot">≈ 1 000 € · 2 nuits</div></div>
  </div>
  <div class="mosaic"><img src="img/garaibie1.webp" alt="Le Garaïbie — photo 1" onclick="zoom(this.src)" loading="lazy"><img src="img/garaibie2.webp" alt="Le Garaïbie — photo 2" onclick="zoom(this.src)" loading="lazy"><img src="img/garaibie3.webp" alt="Le Garaïbie — photo 3" onclick="zoom(this.src)" loading="lazy"><img src="img/garaibie4.webp" alt="Le Garaïbie — photo 4" onclick="zoom(this.src)" loading="lazy"></div>
  <div class="card-body">
    <div class="features"><h4>Le bien</h4><ul><li>600 m² · 14 chambres avec salle d'eau + WC <b>privés</b></li><li>Grand salon avec poêle à bois, bar, baby-foot</li><li>2 cuisines dont une professionnelle</li><li>Un seul groupe à la fois : privatisation totale</li></ul></div>
    <div class="invoice"><h4>Prix · 2 nuits · 31/12 → 02/01</h4><table><tr><td>16 pers × 2 nuits × 30 €/pers/nuit</td><td>960 €</td></tr><tr><td>Électricité</td><td>au réel (relevé)</td></tr><tr><td>Caution</td><td>500 € (rendue)</td></tr><tr class="total"><td>Total ÷ 16 pers</td><td>≈ 1 000 € → <b>62 €/pers</b></td></tr></table></div>
  </div>
  <div class="card-foot">
    <div class="party ok"><span class="pdot"></span><div><b>Soirée friendly</b> — Le gîte n'accueille qu'un seul groupe — vous êtes seuls en pleine nature, zéro problème de bruit.</div></div>
    <div class="actions"><a class="btn primary" href="https://www.grandsgites.com/gite-64-groupe-le-garaibie-42.htm" target="_blank">Voir la fiche &amp; contacter ↗</a></div>
  </div>
</article>'''

new5 = f'''<article class="card" data-zone="bearn" id="g5">
  <button class="like" data-id="22" title="Liker cette maison">{HEART}</button>
  <div class="card-top">
    <div class="rank">05</div>
    <div class="title-wrap">
      <h2>Maison Sagardian <span class="pill pill-blue">Pays Basque</span></h2>
      <div class="meta"><span class="meta-item"><i class="dot d-black"></i>Ascain — au pied de la Rhune</span><span class="meta-item"><i class="dot d-gray"></i>≈ 1h45 de Biscarrosse</span><span class="meta-item"><i class="dot d-blue"></i>Montagne à 200 m</span><span class="meta-item"><i class="dot d-gray"></i>15 couchages*</span></div>
    </div>
    <div class="price"><div class="per">65 €<span>/pers</span></div><div class="tot">≈ 975 € · 2 nuits</div></div>
  </div>
  {mosaic('sagardian','Maison Sagardian')}
  <div class="card-body">
    <div class="features"><h4>Le bien</h4><ul><li>2 gîtes communicants = <b>2 pièces à vivre</b> pour le groupe</li><li>Grande cuisine/salle à manger — 15 couverts à table</li><li>Baby-foot, ping-pong, fléchettes · vue sur la Rhune</li><li>Ouvert toute l'année · sentiers de montagne au départ de la maison</li></ul></div>
    <div class="invoice"><h4>Prix · 2 nuits · 31/12 → 02/01</h4><table><tr><td>Week-end moyenne saison</td><td>750 €</td></tr><tr><td>Taxe de séjour (≈ 2,50 €/nuit/adulte)</td><td>≈ 75 €</td></tr><tr><td>Ménage fin de séjour</td><td>150 €</td></tr><tr class="total"><td>Total ÷ 15 pers</td><td>≈ 975 € → <b>65 €/pers</b></td></tr></table></div>
  </div>
  <div class="card-foot">
    <div class="party ask"><span class="pdot"></span><div><b>Soirée à confirmer</b> — 2 salons + jeux de bar, maison faite pour les groupes — confirmez simplement le 31 avec la propriétaire.</div></div>
    <div class="actions"><a class="btn primary" href="https://www.grandsgites.com/gite-64-maison-sagardian-5246.htm" target="_blank">Voir la fiche &amp; contacter ↗</a><span class="btn ghost">📞 06 82 03 48 91</span></div>
  </div>
</article>'''

rep(old5, new5, 'carte #5 → Maison Sagardian')

# ============ 4-5. Récap + note déjà appliqués par script regex précédent ============

open(p, 'w', encoding='utf-8').write(s)
print(f"\nTerminé. {orig_len} → {len(s)} caractères.")
