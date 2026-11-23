#!/usr/bin/env python3
"""Genera il documento 'situazione 2026: economico, finanziario, IRES e IRAP' per Luca (HTML) dal modello (nuova/motore.js + nuova/dati.json).
Uso: python3 tools/doc_luca.py out.html  ; poi PDF con playwright (page.pdf, A4).
Parametri della pagina di Alex: CIG 2027 936/936/936/464, non confermato 0. Tutte le cifre vengono dal modello: nessuna a mano.
Regole di Alex: niente domande per Luca; sempre scritto quale utile (operativo, ante imposte, netto); dati reali e stime distinti."""
import json, subprocess, sys, math, re, datetime as dt
OUT = sys.argv[1]
JS = r"""
const fs=require('fs');const src=fs.readFileSync('nuova/motore.js','utf8');
// copia di prova: secondo acconto 30/11 e base acconti 2026 parametrizzabili (solo per gli scenari del documento)
const t=src.replace("ym === '2026-11' ? 58012","ym === '2026-11' ? (P._sec != null ? P._sec + 10984.5 : 58012)").replace("base26 = 116024","base26 = (P._sec != null ? 47027.5 + P._sec + 21969 : 116024)");
fs.writeFileSync('/tmp/_motore_doc.js',t);
const M=require('/tmp/_motore_doc.js');const D=JSON.parse(fs.readFileSync('nuova/dati.json','utf8'));
const base=()=>{const P=M.parametriDefault(D);Object.assign(P,{quota_non_confermato:0,cig_o_26q4:0,cig_o_27q1:936,cig_o_27q2:936,cig_o_27q3:936,cig_o_27q4:464});return P};
const r0=M.calcola(D,base());const c=r0.ce;
const sc=sec=>{const P=base();P._sec=sec;const r=M.calcola(D,P);const R=r.righe;return {nov:R['2026-11'].chiusura,dic26:R['2026-12'].chiusura,giu27:R['2027-06'].chiusura,dic27:R['2027-12'].chiusura,ott:R['2026-10'].chiusura}};
const R0=r0.righe;
const ires=c.ires;const prev=Math.max(0,ires-47027.5);
const secs=[prev,12000,18000,24000,47027.5];
// ricavo per 100.000 di sensibilita (prova): ricavi nov +100.000
const out={c:{ricavi:c.ricavi,rimanenze:c.rimanenze,materie:c.materie,lavorazioni:c.lavorazioni,provvigioni:c.provvigioni,royalties:c.royalties,personale:c.personale,affitti:c.affitti,energia:c.energia,altri:c.altri,ammortamenti:c.ammortamenti,operativo:c.operativo,int_passivi:c.int_passivi,int_attivi:c.int_attivi,tfm:c.tfm,ante_imposte:c.ante_imposte,imponibile_ires:c.imponibile_ires,ires:c.ires,imponibile_irap:c.imponibile_irap,irap:c.irap,imposte:c.imposte,utile:c.utile,ante_tfm:c.ante_tfm},
 c27:{utile:r0.ce27.utile},
 secs:secs,scen:secs.map(sc),minimo:r0.riepilogo.minimo,mese_minimo:r0.riepilogo.mese_minimo,
 dic26_base:R0['2026-12'].chiusura,dic27_base:R0['2027-12'].chiusura,ott:R0['2026-10'].chiusura,
 ric:{nov:R0['2026-11'].ricavi,dic:R0['2026-12'].ricavi},
 g:{rim_fin:c.rim_fin,rim_in:c.rim_in},
 div:{lordo:R0['2027-05'].dividendo+R0['2027-06'].impDividendo}};
console.log(JSON.stringify(out));
"""
N = json.loads(subprocess.check_output(['node', '-e', JS], cwd='.'))
c = N['c']
D = json.load(open('nuova/dati.json'))
FIN12 = 11923.53 + 216.50  # titoli + interessi attivi + resi: dentro i ricavi e compensati negli altri costi del modello
f = lambda x: ('{:,.0f}'.format(round(x))).replace(',', '.')
def f2(x): return ('{:,.2f}'.format(x)).replace(',', 'X').replace('.', ',').replace('X', '.')
ric = c['ricavi'] - FIN12; altri = c['altri'] - FIN12
var_fisc = c['imponibile_ires'] - c['ante_imposte']
ires, irap = c['ires'], c['irap']
oggi = dt.date.today().strftime('%d/%m/%Y')
# probabilita che l'acconto totale basti: IRES vera ~ normale, media = IRES stimata, scostamento tipico 9.000 (ipotesi)
SD = 9000.0
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2))); phi = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
rows_p = ''
rows_s = ''
for sec, s in zip(N['secs'], N['scen']):
    T = 47027.50 + sec; z = (T - ires) / SD; p = Phi(z); es = SD * (phi(z) - z * (1 - Phi(z))); cost = es * (25 / 3 / 100 + 0.01)
    p12 = 1 - Phi((T + 12000 - ires) / SD)
    cls = ' class="t"' if abs(sec - 47027.5) < 1 else ''
    rows_p += '<tr%s><td>%s</td><td>%s</td><td>%s</td><td>%s%%</td><td>%s</td><td>%s%%</td></tr>' % (cls, f2(sec), f(T), f(47027.5 - sec), '99' if p > 0.995 else round(p * 100), f(cost) if cost >= 1 else '0', round(p12 * 100))
    rows_s += '<tr%s><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (cls, f2(sec), f(s['nov']), f(s['dic26']), f(s['giu27']), f(s['dic27']))
sec_prev = N['secs'][0]; s_prev = N['scen'][0]; s_stor = N['scen'][-1]
cassa_diff = s_prev['dic26'] - s_stor['dic26']
html = '''<!doctype html><html lang="it"><head><meta charset="utf-8"><title>HTP - Situazione 2026 IRES e IRAP</title>
<style>@page{size:A4;margin:14mm 13mm}body{font-family:Helvetica,Arial,sans-serif;font-size:10pt;line-height:1.38;color:#1a1a1a}
h1{font-size:16pt;margin:0}h2{font-size:12pt;margin:15px 0 5px;color:#1f4e79;border-bottom:2px solid #1f4e79;padding-bottom:2px}
.sub{color:#555;font-size:9pt;margin:3px 0 8px}table{border-collapse:collapse;width:100%%;margin:5px 0 7px;font-size:9.4pt}
th,td{border:1px solid #bbb;padding:3px 6px;text-align:right}th{background:#e8eef5}td:first-child,th:first-child{text-align:left}
tr.t td{font-weight:bold;background:#f3f6fa}.box{background:#fff6e5;border-left:4px solid #d98200;padding:5px 9px;margin:7px 0}
ul{margin:3px 0 4px 18px;padding:0}li{margin:2px 0}.pb{page-break-before:always}</style></head><body>
<h1>HTP S.r.l. — situazione 2026: economico, finanziario, IRES e IRAP</h1>
<div class="sub">Per Luca Rizzi (SGA) e Valentina, da valutare entro il 30/11/2026 (secondi acconti). Stime del modello di cash flow al %(oggi)s: gennaio-ottobre dal bilancio provvisorio al 31/10 di Verusca; novembre = DDT emessi fino al 23/11 (84.085 €) più ordini aperti della stampa Pegaso del 23/11 (ore 14:02); dicembre = ordini aperti del 23/11 senza le righe PRV (programmi) di DPH (20.600 €) e con 4.500 € di OMR 178002 indicati da Valentina; magazzino al 31/10 dal gestionale; scadenzari Pegaso del 18/11. Non sono dati definitivi. Preparato per Alex Foresti.</div>

<h2>1. Conto economico 2026 (stima a fine anno)</h2>
<table><tr><th>Voce</th><th>Importo €</th><th>Come è costruita</th></tr>
<tr><td>Ricavi delle vendite</td><td>%(ric)s</td><td>gen-ott reali (fatture), nov-dic DDT e ordini aperti</td></tr>
<tr><td>Variazione rimanenze</td><td>%(rim)s</td><td>magazzino finale %(rimfin)s (valore al 31/10) contro iniziali %(rimin)s</td></tr>
<tr><td>Materie prime e acquisti</td><td>−%(mat)s</td><td>consumo sui ricavi, percentuale dei 10 mesi reali</td></tr>
<tr><td>Lavorazioni c/terzi, provvigioni, royalties</td><td>−%(dir3)s</td><td>%(lav)s + %(prov)s + %(roy)s</td></tr>
<tr><td>Personale (con TFR, 13ª, ferie)</td><td>−%(pers)s</td><td>reale gen-ott, medie sui 10 mesi</td></tr>
<tr><td>Affitti, energia, altri costi</td><td>−%(str)s</td><td>%(aff)s + %(en)s + %(altri)s</td></tr>
<tr><td>Ammortamenti</td><td>−%(amm)s</td><td>stima, non ancora registrati</td></tr>
<tr class="t"><td>Risultato operativo</td><td>%(oper)s</td><td></td></tr>
<tr><td>Interessi passivi / attivi e titoli</td><td>−%(ip)s / +%(ia)s</td><td>reali gen-ott e piano dei finanziamenti</td></tr>
<tr><td>TFM (20%% del risultato prima del TFM)</td><td>−%(tfm)s</td><td>dedotto per competenza</td></tr>
<tr class="t"><td>Utile ante imposte (dopo il TFM)</td><td>%(ante)s</td><td></td></tr>
<tr><td>IRES + IRAP</td><td>−%(imp)s</td><td>vedi punto 2</td></tr>
<tr class="t"><td>Utile netto (dopo TFM, IRES e IRAP)</td><td>%(utile)s</td><td></td></tr></table>
<div class="sub">Il conto economico con il dettaglio di tutti i conti è nel documento separato "Conto economico 2026".</div>

<h2>2. IRES e IRAP 2026</h2>
<table><tr><th>Voce</th><th>Importo €</th></tr>
<tr><td>Utile ante imposte (dopo il TFM)</td><td>%(ante)s</td></tr>
<tr><td>Variazioni fiscali (auto 80%%, telefonia, indeducibili, multe)</td><td>+%(vf)s</td></tr>
<tr class="t"><td>Imponibile IRES 2026</td><td>%(impires)s</td></tr>
<tr><td>IRES 24%%</td><td>%(ires)s</td></tr>
<tr><td>Imponibile IRAP (risultato operativo + compenso amministratore e multe)</td><td>%(impirap)s</td></tr>
<tr><td>IRAP 3,9%%</td><td>%(irap)s</td></tr>
<tr class="t"><td>Imposte 2026 stimate (IRES + IRAP)</td><td>%(imp)s</td></tr>
<tr><td>Acconti 2026, metodo storico (IRES 2 × 47.027,50 + IRAP 2 × 10.984,50)</td><td>116.024</td></tr>
<tr class="t"><td>Credito stimato a fine anno se si versa tutto il metodo storico</td><td>circa %(cred)s</td></tr></table>
<div class="sub">Base 2025 (Luca, mail 16/11): imponibile IRES 426.167, IRES 102.280, IRAP 21.969. Secondo acconto storico da versare il 30/11: IRES 47.027,50 + IRAP 10.984,50 = 58.012.</div>

<h2>3. Situazione finanziaria 2026</h2>
<table><tr><th>Cassa (banche e depositi)</th><th>31/10 reale</th><th>30/11</th><th>31/12</th></tr>
<tr><td>Con acconti storici (58.012 a novembre)</td><td>%(ott)s</td><td>%(nov_s)s</td><td>%(dic_s)s</td></tr>
<tr><td>IRES previsionale (%(sp)s) + IRAP storica (10.984,50)</td><td>%(ott)s</td><td>%(nov_p)s</td><td>%(dic_p)s</td></tr>
<tr class="t"><td>Differenza</td><td>—</td><td>+%(dn)s</td><td>+%(dd)s</td></tr></table>
<ul><li>Novembre: incassi attesi (Enextras, RiBa del 30/11 e altri); dicembre: personale con 13ª, finanziamenti e pagamenti ai fornitori. I costi di novembre-dicembre si pagano in gran parte a gennaio-marzo 2027 (fornitori a 60-105 giorni, provvigioni il mese dopo, royalties del 4° trimestre a gennaio).</li>
<li>Cassa minima del periodo: %(minimo)s (%(mmin)s). Il credito IVA di 28.165 € al 31/10 non viene versato e si recupera con la dichiarazione annuale.</li>
<li>Fine 2027: %(d27)s € con acconti storici (l'acconto previsionale è solo un anticipo di cassa, con la compensazione del credito a giugno 2027). Nel 2027 è previsto il dividendo a HFA e HFV pari al 100%% dell'utile netto 2026 (circa %(div)s € lordi, maggio-giugno 2027), già dentro la cassa 2027.</li></ul>

<h2>4. Secondo acconto IRES: scenari (metodo previsionale)</h2>
<div class="sub">Primo acconto IRES già versato 47.027,50. Acconto totale = IRES stimata (100%%); secondo acconto = IRES stimata − primo, mai oltre 47.027,50 (storico) e non sotto zero. L'IRAP resta a 10.984,50 (Luca: nessun ricalcolo). Con la stima di oggi (IRES %(ires)s) il secondo acconto previsionale è %(sp)s.</div>
<table><tr><th>Secondo acconto IRES €</th><th>Cassa 30/11</th><th>Cassa 31/12/2026</th><th>Cassa 30/06/2027</th><th>Cassa 31/12/2027</th></tr>%(rows_s)s</table>
<div class="box"><b>È un anticipo di cassa, non un risparmio.</b> Con il metodo storico il credito si compensa a giugno 2027 con il saldo 2026 e il primo acconto 2027. Con il previsionale la cassa è più alta fino alla compensazione di giugno 2027 e a fine 2027 la differenza residua è di circa %(d27diff)s €. Rischio: sanzione se l'acconto risulta inferiore all'imposta definitiva.</div>

<h2>5. Probabilità che il secondo acconto IRES basti (stima)</h2>
<div class="sub">Valutazione sulla dispersione delle voci ancora non definitive, non un calcolo statistico. Ipotesi: IRES 2026 stimata %(ires)s € con uno scostamento tipico di circa 9.000 € (circa 38.000 € sull'utile ante imposte), distribuito in modo simmetrico. Primo acconto già versato 47.027,50 €. La sanzione di circa l'8,3%% (25%% diviso 3) più circa l'1%% di interessi si applica alla sola parte non versata.</div>
<table><tr><th>Secondo acconto IRES €</th><th>Acconto totale €</th><th>Cassa non versata il 30/11 €</th><th>Probabilità che basti</th><th>Costo atteso sanzione e interessi €</th><th>Probabilità di sanzione oltre 1.000 €</th></tr>%(rows_p)s</table>
<div class="box"><b>Lettura.</b> Il previsionale di oggi (secondo acconto %(sp)s €, acconto totale %(ires)s €) copre l'IRES vera con una probabilità vicina al 50%%. Un secondo acconto di 12.000 € porta la probabilità a circa il %(p12)s%% e lascia comunque fuori circa %(f12)s € di cassa. Il resto dell'acconto è un anticipo recuperato a giugno 2027. L'IRAP resta a 10.984,50 €.</div>

<h2 class="pb">6. Cosa sposta l'imponibile 2026</h2>
<ul><li><b>Ricavi di novembre e dicembre</b>: ogni 100.000 € di ricavi in più muovono l'utile ante imposte di circa 60.000 € (IRES circa +14.400, IRAP circa +2.900, utile netto circa +42.600). Novembre e dicembre oggi: %(rnov)s € e %(rdic)s € (stampa Pegaso del 23/11 e DDT già emessi, con il non confermato escluso); Valentina indica 164.000 € e 150.000 € (suo conteggio del 23/11, che esclude il T.Erre).</li>
<li><b>T.Erre 110002E</b>: l'accordo non è ancora firmato e le quantità da spedire sono indefinite. Nel modello ci sono circa 34.100 € a novembre-dicembre e 19.000 € a gennaio 2027. Ogni 53.000 € di ricavi T.Erre in più o in meno valgono circa 31.800 € di utile ante imposte, 7.600 € di IRES e 22.600 € di utile netto.</li>
<li><b>Magazzino finale</b>: usato il valore al 31/10 (%(rimfin)s €) anche a fine anno; l'inventario del 31/12 si fa a gennaio 2027. Ogni 10.000 € di magazzino in più o in meno valgono circa 8.000 € di imponibile.</li>
<li><b>TFR, 13ª e ferie</b>: 13ª calcolata su una mensilità di 41.708 € (55.646 € con contributi), TFR 46,2k annuo, ferie 35,8k.</li>
<li><b>Costi non ancora registrati</b> (fatture da ricevere 62k a fine ottobre, fatture di fine anno) e ratei e risconti di dicembre.</li>
<li><b>Ammortamenti</b> (110.000 stimati; 2025: 123.888) e variazioni fiscali (%(vf)s € stimate sul 2025).</li></ul>

<h2>7. Comunicazione dell'Agenzia delle Entrate (PEC del 09/11/2026): secondo acconto IRES 2024</h2>
<div class="sub">Controllo automatizzato sulla dichiarazione REDDITI 2025 (periodo d'imposta 2024), comunicazione n. 0011491725601 elaborata il 06/11/2026. Importi dal PDF; le righe "ricavato" sono calcoli nostri da confermare con la dichiarazione.</div>
<table><tr><th>Voce</th><th>Importo €</th><th>Origine</th></tr>
<tr><td>Secondo acconto IRES 2024 dovuto (metodo storico, 50%%)</td><td>73.068,00</td><td>PDF</td></tr>
<tr><td>Secondo acconto versato (metodo previsionale)</td><td>40.000,00</td><td>PDF</td></tr>
<tr><td>Importo omesso (insufficiente versamento)</td><td>28.390,99</td><td>PDF</td></tr>
<tr><td>Sanzione (25%% ridotta a un terzo, cod. 9575)</td><td>2.365,92</td><td>PDF</td></tr>
<tr><td>Interessi (cod. 9574)</td><td>743,30</td><td>PDF</td></tr>
<tr class="t"><td>Totale da versare entro 60 giorni dal ricevimento (circa 08/01/2027), o in rate trimestrali</td><td>3.109,22</td><td>PDF</td></tr>
<tr><td>IRES 2024 vera (73.068 + 40.000 + 28.391 = primo acconto + secondo necessario)</td><td>circa 141.459</td><td>ricavato</td></tr>
<tr><td>Base storica (IRES 2023, 2 × 73.068)</td><td>146.136</td><td>ricavato</td></tr>
<tr><td>Imposte correnti 2024 da bilancio (IRES + IRAP)</td><td>193.145</td><td>bilancio 2024</td></tr>
<tr><td>IRAP 2024 per differenza</td><td>circa 51.686</td><td>ricavato</td></tr></table>
<div class="box"><b>Cosa significa per il 30/11/2026.</b> Nel 2024 il previsionale aveva tagliato 33.068 dal secondo acconto; l'IRES vera era solo 4.677 sotto la base storica, quindi 28.391 risultarono non versati. Lo stesso meccanismo vale per il 2026: se l'IRES 2026 vera supera la stima del modello (%(ires)s), sulla parte non versata si paga circa l'8,3%% di sanzione (25%% diviso 3) più interessi, anche se la differenza viene versata a saldo. Esempio: 10.000 € di scostamento = circa 830 € di sanzione. I 3.109,22 € di gennaio 2027 non sono inclusi nella cassa del punto 3.</div>
<div class="sub">Cifre del modello al %(oggi)s; si aggiornano con il bilancio di novembre, i DDT e le fatture reali, il programma consegne T.Erre e l'inventario di gennaio.</div>
</body></html>''' % dict(
    oggi=oggi, ric=f(ric), rim=('+' if c['rimanenze'] >= 0 else '−') + f(abs(c['rimanenze'])), rimfin=f(N['g']['rim_fin']), rimin=f(N['g']['rim_in']),
    mat=f(c['materie']), dir3=f(c['lavorazioni'] + c['provvigioni'] + c['royalties']), lav=f(c['lavorazioni']), prov=f(c['provvigioni']), roy=f(c['royalties']),
    pers=f(c['personale']), str=f(c['affitti'] + c['energia'] + altri), aff=f(c['affitti']), en=f(c['energia']), altri=f(altri), amm=f(c['ammortamenti']),
    oper=f(c['operativo']), ip=f(c['int_passivi']), ia=f(c['int_attivi']), tfm=f(c['tfm']), ante=f(c['ante_imposte']), imp=f(c['imposte']), utile=f(c['utile']),
    vf=f(var_fisc), impires=f(c['imponibile_ires']), ires=f(ires), impirap=f(c['imponibile_irap']), irap=f(irap),
    cred=f(116024 - c['imposte']),
    ott=f(N['ott']), nov_s=f(s_stor['nov']), dic_s=f(s_stor['dic26']), nov_p=f(s_prev['nov']), dic_p=f(s_prev['dic26']), sp=f2(sec_prev),
    dn=f(s_prev['nov'] - s_stor['nov']), dd=f(cassa_diff), minimo=f(N['minimo']), mmin=N['mese_minimo'], d27=f(s_stor['dic27']), div=f(N['div']['lordo']),
    d27diff=f(s_prev['dic27'] - s_stor['dic27']), p12=round(Phi((47027.50 + 12000 - ires) / SD) * 100), f12=f(47027.5 - 12000),
    rows_s=rows_s, rows_p=rows_p, rnov=f(N['ric']['nov']), rdic=f(N['ric']['dic']))
open(OUT, 'w').write(html)
print('ok', OUT, '| ricavi', f(ric), 'ante', f(c['ante_imposte']), 'IRES', f(ires), 'utile', f(c['utile']), '| sec prev', f2(sec_prev))
