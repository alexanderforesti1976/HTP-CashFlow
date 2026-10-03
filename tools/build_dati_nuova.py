#!/usr/bin/env python3
"""Genera nuova/dati.json: H1 dalla bozza 30/06/2026 (params.json H1_2026_reale, verificato al centesimo)
e luglio/agosto dai mastrini 2026 (xlsx di Alex, NON nel repo), con la stessa riclassifica della bozza.
Uso: python3 tools/build_dati_nuova.py /percorso/MASTRINI_2026.xlsx /percorso/OrdiniVenditaAperti.pdf /percorso/Condizioni_pagamento_clienti_fornitori.xlsx"""
import json, sys, collections, openpyxl, re, subprocess, datetime as dt
xlsx = sys.argv[1]; pdf_ordini = sys.argv[2]; xlsx_cond = sys.argv[3]
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
reg_h1 = collections.defaultdict(float)  # conti personale gen-giu dai mastrini (INAIL 6041101, TFR 6041200/6041201)
nomi = {}
wb = openpyxl.load_workbook(xlsx, data_only=True)
for r in wb['Movimenti'].iter_rows(min_row=2, values_only=True):
    if r[14] == 'Sì' or not r[3]: continue
    g = gruppo(int(r[1]))
    if int(r[1]) in (6041101, 6041200, 6041201) and r[3].month <= 6: reg_h1[int(r[1])] += (r[8] or 0) - (r[9] or 0)
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
# --- ordini aperti Pegaso (PDF, non nel repo): mese = periodo di conferma; righe 2099 (in attesa c/lavoro) e 2100 (programmi) al mese della
# data richiesta consegna; esclusi i mesi gia passati rispetto alla stampa e, oltre la finestra Ott26-Mag27, i contratti con data lontana.
def parse_ordini(path):
    txt = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout
    stampa = dt.datetime.strptime(re.search(r'Stampa del (\d\d/\d\d/\d{4})', txt).group(1), '%d/%m/%Y').date()
    giorno = lambda x: dt.datetime.strptime(x, '%d/%m/%Y').date()
    rows = []
    for ln in txt.split('\n'):
        m = re.match(r'^(2\d{3})\s+(\d{1,2})\s+(\d{5,6})\s', ln)
        if not m: continue
        date = re.findall(r'\d\d/\d\d/\d{4}', ln); nums = re.findall(r'\d{1,3}(?:\.\d{3})*,\d+', ln)
        cli = re.sub(r'^\d\d/\d\d/\d{4}\s+', '', re.sub(r'\s+', ' ', ln[m.end():m.end() + 60]).strip()).upper()
        rows.append({'anno': m.group(1), 'mese': int(m.group(2)), 'date': date, 'cli': cli, 'res': float(nums[-1].replace('.', '').replace(',', '.'))})
    totale = round(sum(r['res'] for r in rows), 2)
    mesi_o = collections.defaultdict(lambda: {'tot': 0.0, 'nc': 0.0, 'imp': 0.0, 'cli': collections.defaultdict(float)})
    for r in rows:
        if r['anno'] in ('2099', '2100'):
            d = giorno(r['date'][1]); nc = True
            if d <= stampa: continue
        else:
            d = dt.date(int(r['anno']), r['mese'], 1); nc = False
        ym = d.strftime('%Y-%m')
        if not ('2026-10' <= ym <= '2027-05'): continue
        mesi_o[ym]['tot'] += r['res']; mesi_o[ym]['cli'][re.sub(r'\s+(V0\\d|V11|PRV).*$', '', r['cli'])] += r['res']
        if nc: mesi_o[ym]['nc'] += r['res']
        if any(n.upper() in r['cli'] for n in P['taxClients']): mesi_o[ym]['imp'] += r['res']
    return stampa, totale, mesi_o
stampa_o, totale_o, ORD = parse_ordini(pdf_ordini)

# --- matrice incassi per ott-dic 2026 dal mix clienti del PDF x condizioni di pagamento (xlsx): mesi di ritardo dall'emissione
def ritardo(cond):
    c = cond.lower()
    if any(x in c for x in ('prepayment', 'anticipato', 'vista', 'c.a.d')): return 0
    m = re.search(r'(\d+)\s*(gg|days)', c)
    return int(round(int(m.group(1)) / 30)) if m else 1
wbc = openpyxl.load_workbook(xlsx_cond, data_only=True).active
CL = [(r[2].upper(), ritardo(r[4] or ''), r[7]) for r in wbc.iter_rows(min_row=2, values_only=True) if r[0] == 'CLIENTE' and r[2] and str(r[10]).lower() != 'true']
def ritardo_cliente(nome):
    k = ' '.join(nome.upper().split()[:2])
    m = [c for c in CL if k in c[0]] or [c for c in CL if nome.upper().split()[0][:7] in c[0]]
    m = sorted(m, key=lambda c: c[2] != 'R')  # prima RiBa italiana
    return m[0][1] if m else 2
REC = {}
for ym in ('2026-10', '2026-11', '2026-12'):
    v = [0.0] * 7
    for nome, tot in ORD[ym]['cli'].items(): v[min(6, ritardo_cliente(nome))] += tot
    REC[ym] = [round(x / ORD[ym]['tot'], 4) for x in v]
ricavi_previsti = []
ricavi_previsti.append({'mese': 'Settembre', 'totale': round(P['OBACKLOG'][2]['t'] * 1000, 2), 'non_confermato': 0})
for ym, lab in (('2026-10', 'Ottobre'), ('2026-11', 'Novembre'), ('2026-12', 'Dicembre')):
    ricavi_previsti.append({'mese': lab, 'totale': round(ORD[ym]['tot'], 2), 'non_confermato': round(ORD[ym]['nc'], 2)})
out = {'_fonte': 'H1: bozza bilancio 30/06/2026 del 13/07/2026 (riconciliata al centesimo, R058); luglio e agosto: mastrini 2026 estratti il 02/10/2026 16:02 (settembre incompleto, non usato). Importi in euro. Lo storno 41.502,04 (07011300) e dentro altri_costi del H1 per convenzione aziendale.',
       'bozza_totali': {'costi': 1215491.60, 'ricavi': 1257026.72, 'utile': 41535.12},
       'h1': h1, 'mesi': mesi, 'altri_conti': altri_conti, 'ricavi_previsti': ricavi_previsti,
       '_nota_ricavi': 'Ordini aperti Pegaso stampa 02/10/2026 17:50 (OBACKLOG di params.json); settembre = 142,5k emessi + 77,5k da emettere (provvisorio); non_confermato = programmi 2100 + righe 2099'}

# --- dati per il cash flow (passo 3): ereditati da params.json (R005, R009: verificati su scadenzari e condizioni di pagamento)
ob = {x['m']: x for x in P['OBACKLOG']}
def quota_iva(lab):
    r = ob.get(lab)
    if not r or r['t'] <= 0: return P['vendTaxShareDef'] / 100
    return round(sum(c[1] for c in r['c'] if any(n in c[0] for n in P['taxClients'])) / r['t'], 4)
ym_lab = {'2026-09': 'Set 26', '2026-10': 'Ott 26', '2026-11': 'Nov 26', '2026-12': 'Dic 26'}
fin = collections.defaultdict(float)
for l in P['loans']:
    for ym, v in l['sched'].items():
        if '2026-10' <= ym <= '2027-12': fin[ym] += v * 1000
m7r = mesi['7']['ricavi_operativi']; m8r = mesi['8']['ricavi_operativi']
cf = {
 'cassa_30_09': 1870460.00,
 'ricavi': dict([('2026-09', round(ob['Set 26']['t'] * 1000, 2))] + [(ym, round(ORD[ym]['tot'], 2)) for ym in ('2026-10', '2026-11', '2026-12')]),
 'quota_iva_vendite': dict([('2026-09', quota_iva('Set 26'))] + [(ym, round(ORD[ym]['imp'] / ORD[ym]['tot'], 4)) for ym in ('2026-10', '2026-11', '2026-12')]),
 'rec_matrix': dict(list({k: v for k, v in P['recMatrix'].items()}.items()) + list(REC.items())),
 'pay_matrix': P['payMatrix'],
 'aperti_clienti': {k: round(v * 1000, 2) for k, v in P['openRecSched'].items()},
 'aperti_fornitori': {k: round(v * 1000, 2) for k, v in P['openPaySched'].items()},
 'acquisti_settembre_registrati': round(P['purchPartial']['2026-09'] * 1000, 2),
 'ricavi_2026_mensili': {'2026-01': 136970, '2026-02': 228310, '2026-03': 198160, '2026-04': 202780, '2026-05': 197600, '2026-06': 238150, '2026-07': round(m7r,2), '2026-08': round(m8r,2)},
 'ordini_2027': {ym: round(ORD[ym]['tot'], 2) for ym in sorted(ORD) if ym >= '2027-01'},
 'ordini_fonte': {'stampa': str(stampa_o), 'residuo_totale_pdf': totale_o},
 'finanziamenti_mensili': {k: round(v, 2) for k, v in sorted(fin.items())},
 'iva': {'aliquota': P['ivaRate'], 'energia': P['ivaEnergia'], 'quota_plafond_acquisti': P['matPlafondShare'], 'quota_vendite_default': P['vendTaxShareDef']},
 '_fonti': 'recMatrix, payMatrix, aperti clienti/fornitori, finanziamenti e quote IVA ereditati da params.json (derivati da scadenzari Pegaso 02/10, condizioni di pagamento, piani di ammortamento; R005, R007, R009); cassa 30/09 dal file situazione banche (R045)'}

# --- valori di partenza dei parametri modificabili (solo dati futuri; i dati passati restano bloccati)
def gsum(k): return h1.get(k, 0) + mesi['7'].get(k, 0) + mesi['8'].get(k, 0)
ric_ga = gsum('ricavi_operativi')
pub = sum(c['tot_gen_ago'] for c in altri_conti if c['conto'] == 6021808)
rec = sum(c['tot_gen_ago'] for c in altri_conti if c['ricorrente'])
irr = sum(c['tot_gen_ago'] for c in altri_conti if not c['ricorrente'])
cf['defaults'] = {
 'pers_mese': round(h1['personale'] / 6, 2),
 'pct_materie': round(gsum('materie') / ric_ga * 100, 3),
 'pct_lavorazioni': round(gsum('lavorazioni_terzi') / ric_ga * 100, 3),
 'pct_provvigioni': round(gsum('provvigioni') / ric_ga * 100, 3),
 'affitti_mese': mesi['8']['affitti'],
 'energia_mese': round(gsum('energia') / 8, 2),
 'altri_ricorrenti_mese': round(rec / 8, 2),
 'costi_irregolari_mese': round((irr - pub) / 8, 2),
 'pubblicita_gen_ago': round(pub, 2),
 '_nota': 'Rapporti reali gen-ago 2026 (bozza 30/06 + mastrini lug-ago); altri costi dai conti dei mastrini (ricorrenti = presenti in almeno 6 mesi su 8; irregolari senza pubblicità/fiere)'}
cf['non_confermato'] = {r['mese']: r['non_confermato'] for r in ricavi_previsti}

# --- dati per il CE 2026 e le imposte (passo 6)
# TFR e 13a per legge (art. 2120 c.c.; CCNL gomma-plastica industria: 13 mensilita, niente 14a): stipendi 12 mesi = H1 x 2 (metodo Alex);
# 13a = stipendi 12 mesi / 12 + contributi (INPS + INAIL, rapporto reale 2026); TFR = (stipendi 12 mesi + 13a) / 13,5 - 0,50% dell'imponibile INPS;
# da aggiungere = quota annua - TFR gia registrato in H1 (6041200 + 6041201).
sal12 = h['salari'] * 2
inail = reg_h1[6041101]; contr_anno = (h['contributi'] - inail) * 2 + inail
r_contr = contr_anno / sal12
tred_lordo = sal12 / 12
tred = tred_lordo * (1 + r_contr)
tfr_annuo = (sal12 + tred_lordo) / 13.5 - 0.005 * (sal12 + tred_lordo)
tfr_reg = reg_h1[6041200] + reg_h1[6041201]
integ = {'tfr_da_aggiungere': round(tfr_annuo - tfr_reg, 2), 'tredicesima_con_contributi': round(tred, 2),
         '_calcolo': {'stipendi_12_mesi': round(sal12, 2), 'rapporto_contributi_su_stipendi': round(r_contr, 4), 'tredicesima_lorda': round(tred_lordo, 2),
                      'tfr_quota_annua': round(tfr_annuo, 2), 'tfr_gia_registrato_h1': round(tfr_reg, 2)}}
int_sd = sum(v * 1000 for l in P['loans'] for ym, v in l.get('int', {}).items() if '2026-09' <= ym <= '2026-12')
int_27 = sum(v * 1000 for l in P['loans'] for ym, v in l.get('int', {}).items() if '2027-01' <= ym <= '2027-12')
senza_int = [l['name'] for l in P['loans'] if 'int' not in l]
cf['giacenze_30_06'] = {'prodotto_finito': 20437, 'semilavorato': 42170, 'materia_prima': 96348, 'imballi': 5784, 'totale_valore_finale': 164739, '_nota': 'Alex 03/10/2026 (seconda tabella, sostituisce la prima del 155.548): valore pieno 281.730, azzerato -110.609, svalutato 30% -6.382, valore finale 164.739 al 30/06/2026'}
cf['ce2026'] = {
 'interessi_passivi_2027_piani': round(int_27, 2), 'prestiti_senza_piano_interessi': senza_int,
 'interessi_passivi_gen_ago': round(13432.12 + mesi['7']['interessi_passivi'] + mesi['8']['interessi_passivi'], 2),
 'interessi_attivi_gen_ago': 3821.36,
 'ricavi_titoli_gen_giu': h1['ricavi_titoli'],
 'esistenze_iniziali': h1['esistenze_iniziali'],
 'esistenze_iniziali_categorie': {'materie_prime': 118997.02, 'materiali_consumo_imballi': 3487.84, 'semilavorati': 23678.86, 'prodotti_finiti': 22195.61, '_fonte': 'bilancio 2025: rimanenze finali al 31/12/2025 (conti 00041000/41100/41200/41300), somma 168.359,33; materiali di consumo assimilati agli imballi (ipotesi)'},
 'royalties_registrate_gen_ago': round(h1['royalties'] + mesi['7']['royalties'], 2),
 'interessi_passivi_set_dic_piani': round(int_sd, 2),
 'multe_e_costi_indeducibili_2025_ricorrenti': 46600,
 'addback_irap_2025_senza_interinale': 107400,
 'integrazioni': integ,
 '_note': 'Integrazioni di competenza: TFR e 13a calcolati con il metodo standard (DATI_RICEVUTI/R025). Variazioni fiscali IRES e addebiti IRAP stimati dal 2025: IRES 2025 imponibile 426,2k contro utile ante imposte 296,1k (variazioni +130,1k di cui multe 83,5k non ricorrenti: restano 46,6k); IRAP 2025 imponibile 563,3k contro risultato operativo 365k (+198,3k, di cui interinale circa 90,9k: restano 107,4k). Entrambi DA CONFERMARE con Verusca/Luca'}
cf['defaults'].update({'ammortamenti_2026': 110000, 'ammortamenti_2027': 100000, 'giacenza_30_06': 164739, 'rimanenze_finali_2026': 153400})
out['cf'] = cf
json.dump(out, open('nuova/dati.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
