#!/usr/bin/env python3
"""Parser scadenzari Pegaso (fornitori e clienti) da testo `pdftotext -layout`.
Uso:  pdftotext -layout SCADENZARIO.pdf s.txt && python3 tools/parse_pegaso.py fornitori s.txt out.json
      (oppure `clienti`).  Stampa Dare/Avere/saldo: DEVONO coincidere con i totali stampati nel PDF
      (ultime righe TOTALI/SALDO), altrimenti fermarsi e chiedere l'Excel.
Convenzioni: fornitori Avere = fattura (debito), Dare = pagamenti; clienti Dare = fattura (credito), Avere = incassi.
ATTENZIONE: nelle RiBa il 'Pagata il' e' la data di PRESENTAZIONE in banca, NON l'incasso (nessun anticipo bancario): la cassa arriva alla scadenza.
"""
import re, json, sys, datetime as dt
num = lambda s: float(s.replace('.', '').replace(',', '.'))
d = lambda s: dt.datetime.strptime(s, '%d/%m/%Y').date()
AM = r'(-?[\d.]+,\d\d)'
ITEM_F = re.compile(r'^(?P<head>.*?)\s*(?P<scad>\d\d/\d\d/\d{4})\s+(?P<nr>.+?)\s+(?P<prot>\d{6})\s+(?P<doc>\d\d/\d\d/\d{4})\s+(?P<rata>\d+)\s+€\s+' + AM + r'\s+' + AM + r'\s+' + AM + r'\s*(?P<mod>.*)$')
ITEM_C = re.compile(r'^(?P<head>.*?)\s*(?P<scad>\d\d/\d\d/\d{4})\s+(?P<nr>.+?)\s+(?P<doc>\d\d/\d\d/\d{4})\s+(?P<rata>\d+)\s+€\s+' + AM + r'\s+' + AM + r'\s+' + AM + r'\s*(?P<mod>.*)$')
PAY = re.compile(r'^\s{20,}(?P<pag>\d\d/\d\d/\d{4})\s+(?:\S+\s+)?(?P<reg>\d\d/\d\d/\d{4})\s+€\s+' + AM + r'\s+' + AM + r'\s+' + AM)

def parse(path, kind='fornitori'):
    ITEM = ITEM_F if kind == 'fornitori' else ITEM_C
    gi = (7, 8) if kind == 'fornitori' else (6, 7)
    items, sup, code, cur, td, ta = [], None, None, None, 0.0, 0.0
    for l in open(path, encoding='utf-8'):
        l = l.rstrip('\n')
        m = ITEM.match(l)
        if m:
            head = m.group('head').strip()
            mm = re.match(r'^(.*?)\s+(\d{6})$', head) if head else None
            if mm: sup, code = mm.group(1).strip(), mm.group(2)
            dare, avere = num(m.group(gi[0])), num(m.group(gi[1])); td += dare; ta += avere
            cur = dict(sup=sup, code=code, scad=str(d(m.group('scad'))), nr=m.group('nr').strip(), prot=(m.group('prot') if kind == 'fornitori' else None), doc=str(d(m.group('doc'))),
                       dare=dare, avere=avere, mod=m.group('mod').strip()[:22], pays=[])
            items.append(cur); continue
        p = PAY.match(l)
        if p and cur is not None:
            a, b = num(p.group(3)), num(p.group(4)); cur['pays'].append((str(d(p.group('pag'))), a, b)); td += a; ta += b
    return items, td, ta

def residuo(i, kind):
    """importo ancora aperto di una riga (fornitori: debito; clienti: credito)"""
    pays = sum(p[1] - p[2] for p in i['pays'])
    return (i['avere'] - i['dare'] - pays) if kind == 'fornitori' else (i['dare'] - i['avere'] + pays)

if __name__ == '__main__':
    kind, src, out = sys.argv[1:4]
    it, td, ta = parse(src, kind)
    print(len(it), 'righe | Dare', round(td, 2), 'Avere', round(ta, 2), 'saldo', round(ta - td if kind == 'fornitori' else td - ta, 2))
    op = [i for i in it if abs(residuo(i, kind)) > 0.005]
    print('righe aperte', len(op), 'residuo', round(sum(residuo(i, kind) for i in op), 2), '<- deve coincidere col SALDO stampato nel PDF')
    json.dump(it, open(out, 'w'))
