#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

p = 'index.html'
s = open(p, encoding='utf-8').read()

REMOVE = ['g1', 'g5', 'g6', 'g12', 'g15', 'g17', 'g19', 'g102']

# 1. Supprimer les articles
for gid in REMOVE:
    pat = re.compile(r'<article class="card[^"]*" data-zone="[^"]*" id="' + gid + r'">.*?</article>\n?', re.S)
    s2 = pat.sub('', s, count=1)
    assert s2 != s, f'article {gid} non trouvé'
    s = s2
    print(f'OK article {gid} supprimé')

# 2. Rennuméroter les .rank des cartes principales restantes (laisser le bonus « 101 »)
def rerank(m):
    v = int(m.group(1))
    if v > 20:
        return m.group(0)
    rerank.i += 1
    return f'<div class="rank">{rerank.i:02d}</div>'
rerank.i = 0
s = re.sub(r'<div class="rank">(\d+)</div>', rerank, s)

# 3. Pill « Meilleur prix » sur Ithurrondoa (moins cher restant)
old = '<h2>Ithurrondoa <span class="pill pill-blue">Grand salon</span></h2>'
new = '<h2>Ithurrondoa <span class="pill pill-gold">Meilleur prix</span></h2>'
assert s.count(old) == 1
s = s.replace(old, new)
print('OK pill Meilleur prix → Ithurrondoa')

# 4. Stat orange Meilleur prix
old = '<div class="s-label">Meilleur prix</div><div class="s-num">47 €</div><div class="s-pills"><span>Lou Cazalet</span><span>Orthez · 64</span></div>'
new = '<div class="s-label">Meilleur prix</div><div class="s-num">52 €</div><div class="s-pills"><span>Ithurrondoa</span><span>Masparraute · 64</span></div>'
assert s.count(old) == 1
s = s.replace(old, new)
print('OK stat meilleur prix → 52 € Ithurrondoa')

# 5. Stat Sélection 20 → 13
old = '<div class="s-num dark">20</div><div class="s-sub">maisons · 4 zones · loueurs en direct</div>'
new = '<div class="s-num dark">13</div><div class="s-sub">maisons · 4 zones · loueurs en direct</div>'
assert s.count(old) == 1
s = s.replace(old, new)
print('OK stat sélection → 13')

# 6. Sous-titre
old = '<p class="sub">20 maisons chaleureuses à moins de 2h20 de route'
new = '<p class="sub">13 maisons chaleureuses à moins de 2h20 de route'
assert s.count(old) == 1
s = s.replace(old, new)
print('OK sous-titre → 13 maisons')

# 7. Tableau récap : supprimer les lignes des maisons retirées puis renuméroter
for gid in [g for g in REMOVE if g != 'g102']:  # g102 n'a pas de ligne récap
    pat = re.compile(r"<tr onclick=\"location\.hash='" + gid + r"'\">.*?</tr>\n?", re.S)
    s2 = pat.sub('', s, count=1)
    assert s2 != s, f'ligne récap {gid} non trouvée'
    s = s2
    print(f'OK récap {gid} supprimé')
def renum(m):
    renum.i += 1
    return f'<td class="tname">{renum.i:02d} · '
renum.i = 0
s = re.sub(r'<td class="tname">\d+ · ', renum, s)
print('OK récap renuméroté')

# 8. Note montagne : retirer Sagardian
old = 'les options Béarn/Pays Basque (Ithurrondoa, Sagardian, Zazpiak-Bat, Mendipea)'
new = 'les options Béarn/Pays Basque (Ithurrondoa, Zazpiak-Bat, Mendipea)'
assert s.count(old) == 1
s = s.replace(old, new)
print('OK note montagne')

open(p, 'w', encoding='utf-8').write(s)

# Vérifs finales
for kw in ['Cazalet', 'Sagardian', 'Lacampagne', "d'Orx", 'Plagnette', 'Brocq', 'Bonheur', 'Benquet', 'garaibie']:
    assert kw not in s, f'mention restante : {kw}'
cards = re.findall(r'<article class="card[^"]*" data-zone="([^"]*)" id="(g\d+)">', s)
print('\nCartes finales :', len(cards))
for z, gid in cards:
    print(f'  {gid} ({z})')
likes = re.findall(r'class="like" data-id="(\d+)"', s)
print('likes :', len(likes), sorted(set(likes), key=int))
cells = re.findall(r'lk-cell" data-id="(\d+)"', s)
print('lk-cell :', len(cells), sorted(set(cells), key=int))
ranks = re.findall(r'<div class="rank">(\d+)</div>', s)
print('rangs :', ranks)
tn = re.findall(r'<td class="tname">(\d+) · ', s)
print('tname :', tn)
