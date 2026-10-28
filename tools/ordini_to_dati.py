#!/usr/bin/env python3
"""Ricalcola da una stampa ordini aperti Pegaso (PDF) i dati di ricavo/incasso di ott-26..mag-27 in nuova/dati.json,
senza bisogno dei mastrini xlsx né del file condizioni (i ritardi di incasso per cliente sono in RITARDI, da CLAUDE.md).
Regole (R108, R187): ordini normali nel mese di conferma; righe 2099 e programmi 2100 al mese della data richiesta, solo se > data di stampa;
programmi 2100 di T.Erre 110002E OV 260125-260130 ANNULLATI (R187) esclusi con --escludi-terre; finestra ott-26 / mag-27.
Uso: python3 tools/ordini_to_dati.py OrdiniVenditaAperti.pdf [--arretrati] [--bolle-ott] [--scrivi]
 senza --scrivi stampa solo il confronto con i valori attuali di dati.json."""
import re, sys, json, subprocess, datetime as dt, collections
pdf = sys.argv[1]; ARRETRATI = '--arretrati' in sys.argv; ESCL = '--escludi-terre' in sys.argv; BOLLE = '--bolle-ott' in sys.argv; SCRIVI = '--scrivi' in sys.argv
RITARDI = [('ENEXTRAS', 0), ('TERRA VERDE', 0), ('SEROTTI', 1), ('ELRING', 1), ('EDSCHA', 1), ('T.ERRE', 2), ('ARGOMM', 2), ('WATTS', 2), ('EUROGOMMA', 2), ('DICHTUNG', 2),
           ('LAV.EL', 3), ('OMECA', 3), ('CAVAGNA', 3), ('OMR', 3)]  # altri clienti: 2 mesi (default dello script di build)
TAX = ['T.ERRE', 'WATTS', 'SAGOM', 'OMR', 'DUBHE', 'SCALIGERA', 'E.B.', 'BREKA', 'ELLEDI']
BOLLE_OTT = [('LAV.EL. GOMMA', 17678.39), ('EUROGOMMA', 18200.00), ('OMECA', 6932.49), ('WATTS', 5384.25),
             ('EUROGOMMA', 4244.00), ('OMECA', 4378.00),
             ('SEROTTI', 8536.20), ('ARKIMAT', 4800.00), ('LAV.EL. GOMMA', 8242.01), ('OMECA', 6076.45), ('OMR', 2945.25), ('WATTS', 2152.80), ('EUROGOMMA', 356.00), ('MCM', 3925.00), ('T.ERRE', 840.00)]  # R213: spedito tra le stampe del 16/10 (10:37) e del 28/10 (15:06), dal calo dei residui per OV (righe del periodo ott-dic uscite o ridotte); esclusi 260231 T.Erre 46.662,14 (riga di novembre sparita, da verificare) e gli spostamenti (260150/260235 OMECA, righe T.Erre 2027)  # bolle + fatture emesse fino al 13/10 (R190, R192) + spedito tra le stampe del 13/10 e del 15/10 (calo dei residui: Eurgomma 4.244, OMECA 4.378; R201)
PIANO_110002E = {'2026-10': 19000.0, '2026-11': 19000.0, '2026-12': 19000.0, '2027-02': 19000.0, '2027-04': 19000.0}  # piano T.Erre 110002E di Alex 15/10: 80.000 pz (ott+nov) + 40.000 dicembre, febbraio, aprile, a 0,475 (R205)
TERRE_ANNULLATI = {'260125', '260126', '260127', '260128', '260129', '260130'}
def ritardo(nome):
    n = nome.upper()
    for k, d in RITARDI:
        if k in n: return d
    return 2
txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
stampa = dt.datetime.strptime(re.search(r'Stampa del (\d\d/\d\d/\d{4})', txt).group(1), '%d/%m/%Y').date()
giorno = lambda x: dt.datetime.strptime(x, '%d/%m/%Y').date()
M = collections.defaultdict(lambda: {'tot': 0.0, 'nc': 0.0, 'imp': 0.0, 'v': [0.0] * 7})
for ln in txt.split('\n'):
    m = re.match(r'^(2\d{3})\s+(\d{1,2})\s+(\d{5,6})\s', ln)
    if not m: continue
    date = re.findall(r'\d\d/\d\d/\d{4}', ln); nums = re.findall(r'\d{1,3}(?:\.\d{3})*,\d+', ln)
    cli = re.sub(r'^\d\d/\d\d/\d{4}\s+', '', re.sub(r'\s+', ' ', ln[m.end():m.end() + 60]).strip()).upper()
    res = float(nums[-1].replace('.', '').replace(',', '.')); anno = m.group(1)
    if anno in ('2099', '2100'):
        d = giorno(date[1]); nc = True
        if d <= stampa: continue
        if ESCL and anno == '2100' and m.group(3) in TERRE_ANNULLATI and 'T.ERRE' in cli: continue
    else:
        d = dt.date(int(anno), int(m.group(2)), 1); nc = False
        if ARRETRATI and d < dt.date(2026, 10, 1): d = dt.date(2026, 10, 1)  # R207: righe ancora aperte di periodi passati = da spedire, contate a ottobre
    ym = d.strftime('%Y-%m')
    if not ('2026-10' <= ym <= '2027-05'): continue
    e = M[ym]; e['tot'] += res; e['v'][min(6, ritardo(cli))] += res
    if nc: e['nc'] += res
    if any(t in cli for t in TAX): e['imp'] += res
if BOLLE:
    e = M['2026-10']
    for n, v in BOLLE_OTT:
        e['tot'] += v; e['v'][ritardo(n)] += v
        if any(t in n for t in TAX): e['imp'] += v
D = json.load(open('nuova/dati.json', encoding='utf-8')); cf = D['cf']
nuovo = {'ricavi': {}, 'non_conf': {}, 'quota_iva': {}, 'rec': {}, 'ord27': {}, 'rec27': {}}
for ym in ('2026-10', '2026-11', '2026-12'):
    e = M[ym]; nuovo['ricavi'][ym] = round(e['tot'], 2); nuovo['quota_iva'][ym] = round(e['imp'] / e['tot'], 4)
    nuovo['rec'][ym] = [round(x / e['tot'], 4) for x in e['v']]
for ym in ('2027-01', '2027-02', '2027-03', '2027-04', '2027-05'):
    e = M[ym]; nuovo['ord27'][ym] = round(e['tot'], 2); nuovo['rec27'][ym] = [round(x, 2) for x in e['v']]
nc = {'Ottobre': round(M['2026-10']['nc'], 2), 'Novembre': round(M['2026-11']['nc'], 2), 'Dicembre': round(M['2026-12']['nc'], 2)}
print('stampa', stampa, '| escludi T.Erre annullate:', ESCL, '| bolle ottobre:', BOLLE)
for ym in ('2026-10', '2026-11', '2026-12'):
    print(ym, 'ricavi', nuovo['ricavi'][ym], '(attuale', cf['ricavi'].get(ym), ') quota IVA', nuovo['quota_iva'][ym], '(', cf['quota_iva_vendite'].get(ym), ') rec', nuovo['rec'][ym], '(', cf['rec_matrix'].get(ym), ')')
print('non confermato', nc, '(attuale', cf['non_confermato'], ')')
for ym in nuovo['ord27']:
    print(ym, 'ordini', nuovo['ord27'][ym], '(attuale', cf['ordini_2027'].get(ym), ') per ritardo', nuovo['rec27'][ym], '(', cf['rec_ordini_2027'].get(ym), ')')
if SCRIVI:
    for ym in ('2026-10', '2026-11', '2026-12'):
        cf['ricavi'][ym] = nuovo['ricavi'][ym]; cf['quota_iva_vendite'][ym] = nuovo['quota_iva'][ym]; cf['rec_matrix'][ym] = nuovo['rec'][ym]
    cf['non_confermato'].update(nc)
    for ym in nuovo['ord27']:
        cf['ordini_2027'][ym] = nuovo['ord27'][ym]; cf['rec_ordini_2027'][ym] = nuovo['rec27'][ym]
    json.dump(D, open('nuova/dati.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('dati.json aggiornato')
