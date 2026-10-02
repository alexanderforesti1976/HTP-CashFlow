# Uso: python3 tools/aggiorna_nuova.py "cosa ho fatto"  -> riscrive nuova/aggiornamento.json e la versione in nuova/index.html
import json, re, sys, time
ts = int(time.time() * 1000)
json.dump({"ts": ts, "cosa": sys.argv[1]}, open('nuova/aggiornamento.json', 'w'), ensure_ascii=False)
s = open('nuova/index.html').read()
s = re.sub(r"var VER=\d+;", "var VER=%d;" % ts, s)
s = re.sub(r"motore\.js\?v=\d+", "motore.js?v=%d" % ts, s)
open('nuova/index.html', 'w').write(s)
