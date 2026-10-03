// Test del motore: con i parametri di partenza deve dare gli stessi numeri del calcolo di R078 (cassa 31/12/2026 e 31/12/2027).
const fs = require('fs'), M = require('../nuova/motore.js');
const D = JSON.parse(fs.readFileSync(__dirname + '/../nuova/dati.json', 'utf8'));
const P0 = M.parametriDefault(D), P = Object.assign({}, P0, { imposte_2026: 124249 }), r = M.calcola(D, P).riepilogo; // R078: imposte 2026 fissate = acconti pagati
const att = { cassa_2026: 1922348.50, cassa_2027: 1732746.27 }; // R113: acquisti in % dei ricavi, giacenza finale = leva; R110: giacenze 30/06 = 164.739; R109: matrice incassi da PDF; R108: ordini da PDF 03/10 con date; R105: metodo consumo con giacenza 30/06 (imposte 2026 forzate a 124.249 come R078)
let ok = true;
for (const k in att) { const d = Math.round((r[k] - att[k]) * 100) / 100; console.log(k, r[k].toFixed(2), 'atteso', att[k], 'diff', d); if (Math.abs(d) > 10) ok = false; }
console.log('minimo', r.minimo.toFixed(2), r.mese_minimo, '| entrate 2027', r.entrate_2027.toFixed(2), 'uscite 2027', r.uscite_2027.toFixed(2));
// sensibilità: CIG 2027 a zero deve ALZARE le uscite 2027 del costo (un tagliare costi alza la cassa)
const P2 = Object.assign({}, P, { cig27_lavoratori: 0 }), r2 = M.calcola(D, P2).riepilogo;
console.log('CIG 2027 = 0: uscite 2027', r2.uscite_2027.toFixed(2), '(più alte di', r.uscite_2027.toFixed(2) + ')'); if (!(r2.uscite_2027 > r.uscite_2027)) ok = false;
const P3 = Object.assign({}, P, { g30_mp: P.g30_mp - 20000 }), r3 = M.calcola(D, P3).riepilogo;
console.log('giacenza 30/06 -20.000: consumo piu alto, cassa 2027', r3.cassa_2027.toFixed(2), '(più bassa di', r.cassa_2027.toFixed(2) + ')'); if (!(r3.cassa_2027 < r.cassa_2027)) ok = false;
const ra = M.calcola(D, P0); console.log('imposte 2026 automatiche', ra.riepilogo.imposte_2026.toFixed(2), '= IRES', ra.ce.ires.toFixed(2), '+ IRAP', ra.ce.irap.toFixed(2), '| utile', ra.ce.utile.toFixed(2)); if (Math.abs(ra.ce.imposte - ra.riepilogo.imposte_2026) > 0.01 || ra.ce.imposte <= 0) ok = false;
const rb = M.calcola(D, Object.assign({}, P0, { ammortamenti_2026: 200000 })); console.log('ammortamenti +90k: utile', rb.ce.utile.toFixed(0), '(più basso di', ra.ce.utile.toFixed(0) + ')'); if (!(rb.ce.utile < ra.ce.utile && rb.ce.imposte < ra.ce.imposte)) ok = false;
console.log('CE 2027: operativo', ra.ce27.operativo.toFixed(0), 'utile', ra.ce27.utile.toFixed(0), 'imposte', ra.ce27.imposte.toFixed(0)); if (!(ra.ce27.ricavi > 2.0e6 && ra.ce27.imposte > 0)) ok = false;
const rc = M.calcola(D, Object.assign({}, P0, { cig27_lavoratori: 0 })); console.log('CIG 2027 = 0: utile 2027', rc.ce27.utile.toFixed(0), '(più basso di', ra.ce27.utile.toFixed(0) + ')'); if (!(rc.ce27.utile < ra.ce27.utile)) ok = false;
const rf = M.calcola(D, Object.assign({}, P0, { f26_mp: P0.f26_mp + 10000 })); console.log('magazzino finale 2026 +10.000: risultato operativo 2026', rf.ce.operativo.toFixed(0), '(+10.000 su', ra.ce.operativo.toFixed(0) + ')'); if (Math.abs(rf.ce.operativo - ra.ce.operativo - 10000) > 1) ok = false;
console.log(ok ? 'TEST OK' : 'TEST FALLITO'); process.exit(ok ? 0 : 1);
