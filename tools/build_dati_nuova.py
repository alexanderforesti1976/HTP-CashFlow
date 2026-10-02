#!/usr/bin/env python3
"""Genera nuova/dati.json: H1 dalla bozza 30/06/2026 (params.json H1_2026_reale, verificato al centesimo)
e luglio/agosto dai mastrini 2026 (xlsx di Alex, NON nel repo), con la stessa riclassifica della bozza.
Uso: python3 tools/build_dati_nuova.py /percorso/MASTRINI_2026.xlsx"""
import json, sys, collections, openpyxl
xlsx = sys.argv[1]
h = json.load(open('params.json'))['H1_2026_reale']
GRUPPI = {
 'materie':   lambda c: 6011000 <= c <= 6011008 and c != 6011004,
 'lavorazioni_terzi': lambda c: c == 6021003,
 'energia':   lambda c: c in (6021000, 6021001, 6021002),
 'affitti':   lambda c: c == 6031000,
 'provvigioni': lambda c: c in (6021402, 6021403),
 'royalties': lambda c: c == 6023010,
 'personale': lambda c: 6041000 <= c <= 6041500,
 'interessi_passivi': lambda c: 6091000 <= c <= 6091999,
}
def gruppo(c):
    for g, f in GRUPPI.items():
        if f(c): return g
    if 6060000 <= c <= 6069999: return 'esistenze_iniziali'
    if 6000000 <= c < 6100000: return 'altri_costi'
    if c in (7011000, 7011200, 7011400, 7051001, 7051002): return 'ricavi_operativi'
    if c == 7051004: return 'ricavi_titoli'
    if c == 7051901: return 'interessi_attivi'
    if c == 7011300: return 'storno_ricavi'
    return None
mov = collections.defaultdict(lambda: collections.defaultdict(float))
conti = collections.defaultdict(lambda: [0.0]*8)
nomi = {}
wb = openpyxl.load_workbook(xlsx, data_only=True)
for r in wb['Movimenti'].iter_rows(min_row=2, values_only=True):
    if r[14] == 'Sì' or not r[3]: continue
    g = gruppo(int(r[1]))
    if g == 'altri_costi' and r[3].month <= 8:
        conti[int(r[1])][r[3].month-1] += (r[8] or 0) - (r[9] or 0); nomi[int(r[1])] = r[2]
    if g and r[3].month in (7, 8):
        v = (r[8] or 0) - (r[9] or 0)
        if g in ('ricavi_operativi', 'ricavi_titoli', 'interessi_attivi'): v = -v
        mov[r[3].month][g] += v
mesi = {str(m): {g: round(v, 2) for g, v in mov[m].items()} for m in (7, 8)}
h1 = {
 'ricavi_operativi': round(h['ricavi'] + h['ricaviDiversi'] + h['ricaviStampi'], 2),
 'ricavi_titoli': h['ricaviTitoli'], 'interessi_attivi': h['intAttiviCC'],
 'materie': round(h['mpAcquisti'] + h['materialiConsumo'] + h['imballi'] + h['pfAcquistati'], 2),
 'lavorazioni_terzi': h['lavCTerzi'],
 'personale': round(h['salari'] + h['interinale'] + h['contributi'] + h['tfr'] + h['welfare'], 2),
 'energia': h['energia'], 'affitti': h['affitti'], 'provvigioni': h['provvigioni'], 'royalties': h['royalties'],
 'altri_costi': round(h['leasing'] + h['noleggi'] + h['manutenzioni'] + h['pubblicita'] + h['svariComm'] + h['consulAmm'] + h['consulTec'] + h['compensoAmm'] + h['revisore'] + h['speseBancarie'] + h['altriGA'], 2),
 'interessi_passivi': h['interessi'], 'esistenze_iniziali': h['esistenzeIniziali2026'],
}
altri_conti = []
for c, mm in sorted(conti.items()):
    ric = sum(1 for v in mm if abs(v) > 1) >= 6
    altri_conti.append({'conto': c, 'nome': nomi[c], 'mesi': [round(v, 2) for v in mm], 'tot_gen_ago': round(sum(mm), 2), 'ricorrente': ric})
P = json.load(open('params.json'))
ricavi_previsti = []
for i, lab in enumerate(['Settembre', 'Ottobre', 'Novembre', 'Dicembre']):
    ob = P['OBACKLOG'][2 + i]
    nc = round(sum(x[1] for x in ob.get('nc', [])), 2)
    ricavi_previsti.append({'mese': lab, 'totale': round(ob['t'] * 1000, 2), 'non_confermato': round(nc * 1000, 2)})
out = {'_fonte': 'H1: bozza bilancio 30/06/2026 del 13/07/2026 (riconciliata al centesimo, R058); luglio e agosto: mastrini 2026 estratti il 02/10/2026 16:02 (settembre incompleto, non usato). Importi in euro. Lo storno 41.502,04 (07011300) e dentro altri_costi del H1 per convenzione aziendale.',
       'bozza_totali': {'costi': 1215491.60, 'ricavi': 1257026.72, 'utile': 41535.12},
       'h1': h1, 'mesi': mesi, 'altri_conti': altri_conti, 'ricavi_previsti': ricavi_previsti,
       '_nota_ricavi': 'Ordini aperti Pegaso stampa 02/10/2026 17:50 (OBACKLOG di params.json); settembre = 142,5k emessi + 77,5k da emettere (provvisorio); non_confermato = programmi 2100 + righe 2099'}
json.dump(out, open('nuova/dati.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
