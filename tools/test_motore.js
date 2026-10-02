// Test del motore: con i parametri di partenza deve dare gli stessi numeri del calcolo di R078 (cassa 31/12/2026 e 31/12/2027).
const fs = require('fs'), M = require('../nuova/motore.js');
const D = JSON.parse(fs.readFileSync(__dirname + '/../nuova/dati.json', 'utf8'));
const P = M.parametriDefault(D), r = M.calcola(D, P).riepilogo;
const att = { cassa_2026: 1921559.05, cassa_2027: 1732612.56 };
let ok = true;
for (const k in att) { const d = Math.round((r[k] - att[k]) * 100) / 100; console.log(k, r[k].toFixed(2), 'atteso', att[k], 'diff', d); if (Math.abs(d) > 10) ok = false; }
console.log('minimo', r.minimo.toFixed(2), r.mese_minimo, '| entrate 2027', r.entrate_2027.toFixed(2), 'uscite 2027', r.uscite_2027.toFixed(2));
// sensibilità: CIG 2027 a zero deve ALZARE le uscite 2027 del costo (un tagliare costi alza la cassa)
const P2 = Object.assign({}, P, { cig27_lavoratori: 0 }), r2 = M.calcola(D, P2).riepilogo;
console.log('CIG 2027 = 0: uscite 2027', r2.uscite_2027.toFixed(2), '(più alte di', r.uscite_2027.toFixed(2) + ')'); if (!(r2.uscite_2027 > r.uscite_2027)) ok = false;
const P3 = Object.assign({}, P, { pct_materie: P.pct_materie + 2 }), r3 = M.calcola(D, P3).riepilogo;
console.log('materie +2 punti: cassa 2027', r3.cassa_2027.toFixed(2), '(più bassa di', r.cassa_2027.toFixed(2) + ')'); if (!(r3.cassa_2027 < r.cassa_2027)) ok = false;
console.log(ok ? 'TEST OK' : 'TEST FALLITO'); process.exit(ok ? 0 : 1);
