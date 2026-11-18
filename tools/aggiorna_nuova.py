# Uso: python3 tools/aggiorna_nuova.py "cosa ho fatto"  -> riscrive nuova/aggiornamento.json e la versione in nuova/index.html
import json, re, sys, time
ts = int(time.time() * 1000)
json.dump({"ts": ts, "cosa": sys.argv[1]}, open('nuova/aggiornamento.json', 'w'), ensure_ascii=False)
s = open('nuova/index.html').read()
s = re.sub(r"var VER=\d+;", "var VER=%d;" % ts, s)
s = re.sub(r"motore\.js\?v=\d+", "motore.js?v=%d" % ts, s)
open('nuova/index.html', 'w').write(s)
# Promemoria (regola di Alex 18/11/2026): controllare che le date scritte nelle pagine siano ancora vere
import re
for f in ('nuova/index.html', 'nuova/ce.html'):
    for i, l in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
        if re.search(r'30/09|02/10|bloccati|Dati reali fino al', l):
            print('CONTROLLA LA DATA', f, 'riga', i, ':', re.sub(r'\s+', ' ', l)[:110])
