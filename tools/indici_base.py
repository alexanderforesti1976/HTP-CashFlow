# Dati di base per gli indici bancari (da params.json: piani di ammortamento e SP 30/06/2026). Uso: python3 tools/indici_base.py  -> aggiunge 'indici_base' a nuova/dati.json
import json

def calcola(P):
    def residuo(lim):
        t = 0.0
        for l in P['loans']:
            if l.get('res'):
                ks = sorted(l['res']); v = None
                for k in ks:
                    if k <= lim: v = l['res'][k]
                if v is None: v = l['res'][ks[0]] + (l['cap'][ks[0]] if l.get('cap') else 0)
                t += v
            elif l.get('sched'):
                t += sum(x for k, x in l['sched'].items() if k > lim)
        return round(t * 1000, 2)
    rate = lambda y: round(sum(x for l in P['loans'] for k, x in l.get('sched', {}).items() if k.startswith(y)) * 1000, 2)
    return {'rate_2026': rate('2026'), 'rate_2027': rate('2027'),
            'debito_31_12_2026': residuo('2026-12'), 'debito_31_12_2027': residuo('2027-12'),
            'pn_apertura_2026': 1655929.71, 'debiti_bancari_30_06_2026': 637070.07,
            '_fonte': 'rate e debiti dai piani di ammortamento (params.json loans); patrimonio netto di apertura e debiti bancari dalla bozza 30/06/2026 (SP_H1_2026_reale)'}

if __name__ == '__main__':
    P = json.load(open('params.json')); D = json.load(open('nuova/dati.json'))
    D['indici_base'] = calcola(P)
    json.dump(D, open('nuova/dati.json', 'w'), ensure_ascii=False, indent=1)
    print(D['indici_base'])
