# Genera il conto economico civilistico 2026 (HTML) dal bilancio analitico (testo di `pdftotext -layout`, arg 1) e dal modello (nuova/motore.js).
# Uso: python3 tools/ce_civilistico.py bilancio.txt /cartella/   -> scrive ce_conti.json (conti del CE) e acc/ce2026.html in /cartella/ (creare acc/); poi PDF con playwright page.pdf. R267.
import re,sys,json
_S=sys.argv[2]
_t=open(sys.argv[1]).read().split('\n'); _n=lambda s:float(s.replace('.','').replace(',','.'))
_i0=next(i for i,l in enumerate(_t) if 'CONTO ECONOMICO' in l); _co={}; _ri={}
for _l in _t[_i0:]:
    if 'TOTALE' in _l: continue
    for _m in re.finditer(r'(\d{8})\s+(.+?)\s{2,}([\d\.]+,\d\d)',_l):
        (_co if _m.start()<70 else _ri)[_m.group(1)]=(_m.group(2).strip(),_n(_m.group(3)))
json.dump({'costi':_co,'ricavi':_ri},open(_S+'ce_conti.json','w'))
import json,subprocess,html
S=_S
J=json.load(open(S+'ce_conti.json'));CO=J['costi'];RI=J['ricavi']
D=json.load(open('nuova/dati.json'))
# valori del modello (parametri Alex)
js=r"""
const fs=require('fs');const M=require('./nuova/motore.js');const D=JSON.parse(fs.readFileSync('nuova/dati.json','utf8'));
const P=M.parametriDefault(D);Object.assign(P,{quota_non_confermato:0,cig_o_26q4:0},M.cigMensili(2027,[936,936,936,464]));
const r=M.calcola(D,P);const c=r.ce;
const g=k=>D.h1[k]+D.mesi['7'][k]+D.mesi['8'][k]+D.mesi['9'][k]+D.mesi['10'][k];
console.log(JSON.stringify({ce:c,gsum:{materie:g('materie'),lav:g('lavorazioni_terzi'),en:g('energia'),aff:g('affitti'),prov:g('provvigioni'),pers:g('personale'),altri:g('altri_costi')},ricSD:r.ricavi['2026-11']+r.ricavi['2026-12'],I:D.cf.ce2026.integrazioni,P:{pers:P.pers_mese,aff:P.affitti_mese,altri:P.altri_ricorrenti_mese+P.costi_irregolari_mese,fv:P.fv_canone}}))
"""
out=subprocess.check_output(['node','-e',js],cwd='.')
M=json.loads(out)
c=M['ce'];G=M['gsum'];I=M['I']
f=lambda x:('{:,.0f}'.format(round(x))).replace(',','.')
def f2(x): return ('{:,.2f}'.format(x)).replace(',','X').replace('.',',').replace('X','.')
# classificazione conti costi
def grp(code):
    k=int(code)
    if 6061000<=k<=6061004: return 'esist'
    if k in (6011000,6011001,6011003,6011005,6011007,6011008): return 'mat'
    if k==6021003: return 'lav'
    if k in (6021000,6021001,6021002): return 'en'
    if k in (6021402,6021403): return 'prov'
    if k==6023010: return 'roy'
    if k==6031000: return 'aff'
    if 6041000<=k<=6041500: return 'pers'
    if 6091000<=k<6092000: return 'intp'
    if k in (6021400,6021401,6021404,6021405,6021406,6021750): return 'cons'
    if k in (6021300,6021301): return 'ass'
    if k in (6022002,6022004,6022006,6022008,6022009,6022010): return 'man'
    if k==6021808: return 'pub'
    if k in (6032001,6033000,6033001,6033003,6033005): return 'god'
    if k in (6081001,6081002,6081003,6081005,6081007,6081008,6081009,6081011,6081012,6093000,7011300): return 'onedi'
    return 'serv'
rows={}
for code,(nm,a) in CO.items(): rows.setdefault(grp(code),[]).append((code,nm,a))
tot=lambda g:sum(a for _,_,a in rows.get(g,[]))
altri_sum=sum(tot(g) for g in ('cons','ass','man','pub','god','onedi','serv'))
print('verifica materie',round(tot('mat')-216.50,2),'modello',round(G['materie'],2))
print('verifica altri conti',round(altri_sum,2),'modello altri_costi',round(G['altri'],2))
print('lav',tot('lav'),G['lav'],'en',tot('en'),G['en'],'aff',tot('aff'),G['aff'],'prov',tot('prov'),G['prov'],'pers',tot('pers'),G['pers'])
json.dump({'rows':{k:v for k,v in rows.items()},'M':M},open(S+'ce_model.json','w'))

# ---------------- documento ----------------
RIC=lambda code:RI[code][1]
H=[]
def row(label,a=None,b=None,r=None,t=None,cls='',ind=0):
    cells=[]
    for v in (a,b,r,t):
        cells.append('' if v is None else (f(v)))
    H.append('<tr class="%s"><td style="padding-left:%dpx">%s</td>%s</tr>'%(cls,6+ind*10,html.escape(label),''.join('<td>%s</td>'%x for x in cells)))
def sec(label): H.append('<tr class="sec"><td colspan="5">%s</td></tr>'%html.escape(label))
SG=lambda g:tot(g)
ricSD=M['ricSD']
# A
sec('A) VALORE DELLA PRODUZIONE')
vend=RIC('07011000');stampi=RIC('07011400');div=RIC('07011200')
row('1) Ricavi delle vendite e delle prestazioni',vend+stampi+div,ricSD,None,vend+stampi+div+ricSD,'t')
row('Vendite prodotti (conto 07011000)',vend,None,None,None,'d',1)
row('Ricavi per vendita stampi (07011400)',stampi,None,None,None,'d',1)
row('Ricavi diversi (07011200)',div,None,None,None,'d',1)
row('Novembre: DDT emessi fino al 23/11 (84.085) più ordini aperti della stampa 23/11; dicembre: ordini aperti 23/11 senza le righe PRV di DPH (20.600) e con OMR 178002 (4.500)',None,ricSD,None,None,'d',1)
a2=c['a2_fin']-c['a2_in']
row('2) Variazione rimanenze prodotti finiti e semilavorati',None,None,a2,a2,'t')
row('Finali %s (valore al 31/10 dal gestionale, ipotesi uguale a fine anno) meno iniziali %s'%(f(c['a2_fin']),f(c['a2_in'])),None,None,None,None,'d',1)
altr=RIC('07051001')+RIC('07051002')
row('5) Altri ricavi (sconti, abbuoni e arrotondamenti attivi)',altr,None,None,altr,'t')
sep9=D['cf']['ricavi']['2026-09']-D['mesi']['9']['ricavi_operativi']  # settembre: fatture chiuse (modello) contro registrato in bilancio
row('Settembre: fatture emesse (231.237,87) oltre il registrato in bilancio (231.235,60)',None,None,sep9,sep9,'t')
A_gen=vend+stampi+div+altr
A_tot=A_gen+ricSD+a2+sep9
row('TOTALE VALORE DELLA PRODUZIONE',A_gen,ricSD,a2+sep9,A_tot,'tt')
# B
sec('B) COSTI DELLA PRODUZIONE')
mat=SG('mat')-216.50
projmat=c['materie']-(SG('mat')-216.50)
row('6) Materie prime, sussidiarie, di consumo e merci',mat,projmat,None,mat+projmat,'t')
for code,nm,a in sorted(rows['mat']): row('%s %s'%(code[1:],nm.title()),a,None,None,None,'d',1)
row('Resi e abbuoni su acquisti (06011006)',-216.50,None,None,None,'d',1)
row('Novembre-dicembre: consumo '+('%.2f'%(c['acquisti_pct_setdic']*100)).replace('.',',')+'% dei ricavi (previsione)',None,projmat,None,None,'d',1)
# servizi
altri_proj=c['altri']-G['altri']
groups=[('en','Energia e riscaldamento',c['energia']-G['en']),('lav','Lavorazioni c/terzi',c['lavorazioni']-G['lav']),('prov','Provvigioni e Enasarco',c['provvigioni']-G['prov'])]
serv_gen=sum(SG(g) for g,_,_ in groups)+sum(SG(g) for g in ('cons','ass','man','pub','serv'))
serv_proj=sum(p for _,_,p in groups)+altri_proj
row('7) Costi per servizi',serv_gen,serv_proj,None,serv_gen+serv_proj,'t')
for g,nm,p in groups:
    row(nm,SG(g),p,None,SG(g)+p,'s',1)
    for code,n2,a in sorted(rows[g]): row('%s %s'%(code[1:],n2.title()),a,None,None,None,'d',2)
for g,nm in (('cons','Consulenze e compensi professionali'),('ass','Assicurazioni'),('man','Manutenzioni e assistenza'),('pub','Pubblicità e fiere'),('serv','Altri servizi (carburanti, telefono, viaggi, banche, trasporti, auto, ecc.)')):
    row(nm,SG(g),None,None,SG(g),'s',1)
    for code,n2,a in sorted(rows[g]): row('%s %s'%(code[1:],n2.title()),a,None,None,None,'d',2)
row('Novembre-dicembre: altri costi ricorrenti e irregolari a media '+f(M['P']['altri'])+' al mese (10 mesi) + canone fotovoltaico (previsione, anche servizi, noleggi e oneri)',None,altri_proj,None,altri_proj,'s',1)
roy_p=c['royalties']-SG('roy')
god_gen=SG('aff')+SG('roy')+SG('god')
god_proj=(c['affitti']-SG('aff'))+roy_p
row('8) Godimento di beni di terzi',god_gen,god_proj,None,god_gen+god_proj,'t')
row('Affitti passivi (6031000)',SG('aff'),c['affitti']-SG('aff'),None,c['affitti'],'s',1)
row('Royalties 1,5% (6023010): 3 trimestri già registrati, 4° da accantonare',SG('roy'),roy_p,None,c['royalties'],'s',1)
row('Noleggi e leasing',SG('god'),None,None,SG('god'),'s',1)
for code,n2,a in sorted(rows['god']): row('%s %s'%(code[1:],n2.title()),a,None,None,None,'d',2)
integ_tfr=I['tfr_da_aggiungere'];integ_13=I['tredicesima_con_contributi'];integ_fer=I['ferie_rateo_fine_2026']+3655
pers_proj=M['ce']['personale']-SG('pers')-integ_tfr-integ_13-integ_fer
rett_pers=integ_tfr+integ_13+integ_fer
row('9) Costi per il personale',SG('pers'),pers_proj,rett_pers,c['personale'],'t')
for code,n2,a in sorted(rows['pers']): row('%s %s'%(code[1:],n2.title()),a,None,None,None,'d',1)
row('Novembre-dicembre: costo medio '+f(pers_proj/2)+' al mese (organico dopo le due dimissioni)',None,pers_proj,None,None,'d',1)
row('TFR di competenza da aggiungere (maturato annuo 46.157 meno già registrato)',None,None,integ_tfr,None,'d',1)
row('Tredicesima con contributi',None,None,integ_13,None,'d',1)
row('Ferie: rateo 32.136 (neutralizza lo storno di gennaio) + saldo 3.655',None,None,integ_fer,None,'d',1)
amm=c['ammortamenti']
row('10) Ammortamenti (stima, non ancora registrati)',None,None,amm,amm,'t')
b11=c['b11_in']-c['b11_fin']
row('11) Variazione rimanenze materie prime, sussidiarie e consumo',None,None,b11,b11,'t')
row('Iniziali '+f(c['b11_in'])+' meno finali '+f(c['b11_fin'])+' (valore al 31/10 dal gestionale, ipotesi uguale a fine anno)',None,None,None,None,'d',1)
tfm=c['tfm']
row('13) Accantonamento indennità fine mandato amministratore (TFM, 20% del risultato)',None,None,tfm,tfm,'t')
ond=SG('onedi')
row('14) Oneri diversi di gestione',ond,None,None,ond,'t')
for code,n2,a in sorted(rows['onedi']): row('%s %s'%(code[1:],n2.title()),a,None,None,None,'d',1)
B_gen=mat+serv_gen+god_gen+SG('pers')+ond
# riconciliazione al centesimo col modello: il bilancio provvisorio e i dati del modello (fatture di settembre, H1) differiscono di pochi euro
_fin=c['int_attivi']-c['int_passivi']
_ante0=A_tot-(B_gen+projmat+serv_proj+god_proj+pers_proj+rett_pers+amm+b11+tfm)+_fin
recon=c['ante_imposte']-_ante0
B_proj=projmat+serv_proj+god_proj+pers_proj
B_ret=rett_pers+amm+b11+tfm
B_tot=B_gen+B_proj+B_ret
row('TOTALE COSTI DELLA PRODUZIONE',B_gen,B_proj,B_ret,B_tot,'tt')
row('DIFFERENZA TRA VALORE E COSTI DELLA PRODUZIONE (A − B)',A_gen-B_gen,ricSD-B_proj,a2+sep9-B_ret,A_tot-B_tot,'tt')
# C
sec('C) PROVENTI E ONERI FINANZIARI')
pf=RIC('07051004')+RIC('07051901');pf_proj=c['int_attivi']-pf
row('16) Proventi finanziari: cedola/titoli e interessi attivi',pf,pf_proj,None,pf+pf_proj,'t')
row('Ricavi da titoli (07051004)',RIC('07051004'),None,None,None,'d',1)
row('Interessi attivi su c/c (07051901)',RIC('07051901'),None,None,None,'d',1)
row('Novembre-dicembre: cedola di dicembre e interessi (previsione)',None,pf_proj,None,None,'d',1)
ip=SG('intp');ip_proj=c['int_passivi']-ip
row('17) Interessi e altri oneri finanziari',-ip,-ip_proj,None,-(ip+ip_proj),'t')
for code,n2,a in sorted(rows['intp']): row('%s %s'%(code[1:],n2.title()),-a,None,None,None,'d',1)
row('Novembre-dicembre: piano dei finanziamenti (2 mesi)',None,-ip_proj,None,None,'d',1)
fin_gen=pf-ip;fin_proj=pf_proj-ip_proj
row('TOTALE PROVENTI E ONERI FINANZIARI',fin_gen,fin_proj,None,fin_gen+fin_proj,'tt')
ante=A_tot-B_tot+fin_gen+fin_proj
row('RISULTATO PRIMA DELLE IMPOSTE',None,None,None,ante,'tt')
ires,irap=c['ires'],c['irap']
row('20) Imposte sul reddito: IRES (24%) e IRAP (3,9%) di competenza',None,None,-(ires+irap),-(ires+irap),'t')
row('IRES su imponibile '+f(c['imponibile_ires'])+' (utile ante imposte '+f(c['ante_imposte'])+' + variazioni fiscali '+f(c['imponibile_ires']-c['ante_imposte'])+')',None,None,-ires,None,'d',1)
row('IRAP su imponibile '+f(c['imponibile_irap']),None,None,-irap,None,'d',1)
ut=ante-ires-irap
row('UTILE (PERDITA) DELL\'ESERCIZIO',None,None,None,ut,'tt')
assert abs(ante-c['ante_imposte'])<0.005 and abs(ut-c['utile'])<0.005,'CE non quadra con il modello al centesimo'
print('ante',round(ante,2),'(app',round(c['ante_imposte'],2),') utile',round(ut,2),'(app',round(c['utile'],2),')')
print('A_tot',round(A_tot),'B_tot',round(B_tot),'A-B',round(A_tot-B_tot))
body='\n'.join(H)
doc='''<!doctype html><html lang="it"><head><meta charset="utf-8"><title>HTP - Conto economico 2026</title>
<style>@page{size:A4;margin:12mm 11mm}body{font-family:Helvetica,Arial,sans-serif;font-size:8.6pt;line-height:1.28;color:#1a1a1a}
h1{font-size:15pt;margin:0}.sub{color:#555;font-size:8.6pt;margin:3px 0 7px}table{border-collapse:collapse;width:100%}
th,td{border-bottom:1px solid #ddd;padding:1.5px 4px;text-align:right;vertical-align:top}th{background:#1f4e79;color:#fff;font-weight:bold}
td:first-child,th:first-child{text-align:left;width:46%}tr.sec td{background:#dfe8f2;font-weight:bold;text-align:left;border-top:2px solid #1f4e79}
tr.t td{font-weight:bold;background:#f3f6fa}tr.tt td{font-weight:bold;background:#e4ecf6;border-top:1.5px solid #1f4e79}
tr.s td{font-weight:600}tr.d td{color:#444}.box{background:#fff6e5;border-left:4px solid #d98200;padding:5px 9px;margin:6px 0;font-size:8.6pt}
.ok{background:#eef6ee;border-left:4px solid #2e7d32;padding:5px 9px;margin:6px 0;font-size:8.6pt}</style></head><body>
<h1>HTP S.r.l. — Conto economico 2026 (stima a fine anno)</h1>
<div class="sub">Schema civilistico (art. 2425 c.c.) con il dettaglio dei conti. Colonne: <b>gen-ott</b> = bilancio provvisorio al 31/10/2026 di Verusca (conti reali); <b>nov-dic</b> = previsione del modello (ordini aperti e medie dei costi sui 10 mesi); <b>rettifiche</b> = voci di competenza che il bilancio provvisorio non contiene ancora (rimanenze, ammortamenti, TFR, 13ª, ferie, TFM). Importi in euro. Preparato per Alex Foresti il 23/11/2026 (dati Pegaso del 23/11): sono stime, non dati definitivi.</div>
<table><tr><th>Voce</th><th>Gen-ott reale</th><th>Nov-dic previsione</th><th>Rettifiche di competenza</th><th>Totale 2026</th></tr>
'''+body+'''
</table>
<div class="ok"><b>Quadratura:</b> il risultato prima delle imposte ({ANTE}) e l'utile netto ({UTILE}) coincidono con la pagina Economico dell'app (al centesimo, senza righe di riconciliazione). Il bilancio provvisorio al 31/10 ha utile 139.812 prima di rimanenze, ammortamenti, TFR/13ª/ferie, TFM e imposte.</div>
<div class="box"><b>Ipotesi e punti aperti:</b> (1) novembre-dicembre: DDT emessi fino al 23/11 e ordini aperti del 23/11 (stampa 14:02), con T.Erre 110002E incerto (accordo non firmato: circa 34.100 in nov-dic e 19.000 a gennaio, ogni 53.000 di ricavi T.Erre valgono circa 22.600 di utile netto); (2) magazzino: valore al 31/10 dal gestionale (199.613, 97 righe non determinate) usato anche come ipotesi a fine anno: l'inventario del 31/12 si fa a gennaio 2027 (ogni 10.000 di magazzino valgono circa 5.700 di utile netto); (3) ammortamenti 110.000 e TFM 20% stimati; (4) consulenze di ottobre 48.538, di cui 33.000 fatture da ricevere; (5) interessi passivi: reali gen-ott più piano dei finanziamenti.</div>
</body></html>'''
doc=doc.replace('{ANTE}',f(ante)).replace('{UTILE}',f(ut))
open(S+'acc/ce2026.html','w').write(doc)
