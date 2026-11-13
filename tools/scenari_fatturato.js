// Scenari fatturato 2027-28 con CIG adeguata e uscita di due dipendenti (R243). Uso: node tools/scenari_fatturato.js
// Non modifica l'app: legge nuova/motore.js, ne fa una copia in memoria con un gancio `scen_extra` (costo mensile in piu/meno nel 2027) e calcola.
const fs = require('fs'), vm = require('vm'), path = require('path');
let src = fs.readFileSync(path.join(__dirname, '../nuova/motore.js'), 'utf8');
const a = "return P.pers_mese - dimessi(ym) - oreCig(ym) * cigRisp; };";
if (src.indexOf(a) < 0) throw new Error('motore.js cambiato: aggiornare il gancio');
src = src.replace(a, "return P.pers_mese - dimessi(ym) - oreCig(ym) * cigRisp + (ym >= '2027-01' && ym < '2028-01' ? (P.scen_extra || 0) : 0); };");
const mod = { exports: {} }; vm.runInNewContext(src, { module: mod, exports: mod.exports, window: undefined, self: undefined, Math, Object, JSON, Date, Array, Number, String, isNaN, parseFloat });
const M = mod.exports.calcola ? mod.exports : (mod.exports.Motore || mod.exports);
const D = JSON.parse(fs.readFileSync(path.join(__dirname, '../nuova/dati.json'), 'utf8'));
// parametri della pagina di Alex del 02/11/2026 13:08 (R221): CIG Q4-26 = 0, 2027 = 936/936/936/464, quota non confermato = 0
const baseP = Object.assign(M.parametriDefault(D), { cig_o_26q4: 0, quota_non_confermato: 0, cig_o_27q1: 936, cig_o_27q2: 936, cig_o_27q3: 936, cig_o_27q4: 464 });
const W = 1639;            // ore lavorate al mese nel piano di Alex a 2.000k (19 persone x 135,5 ore - 936 ore di CIG)
const ORE = 135.5;         // ore lavorabili al mese per persona (prospetto paghe gen-lug 2026)
const CAP = 26300;         // un terzo delle ore lavorabili nel biennio mobile (19 x 173,33 x 24 / 3), da verificare con lo studio paghe
const rows = [];
function run(R, leave) {
  const k = 1 - R / 2000, cap27 = (leave ? 17 : 19) * ORE, cap28 = 16 * ORE;
  const q13 = Math.max(0, cap27 - W * (1 - k)), q4 = Math.max(0, q13 - 472), c28 = Math.max(0, cap28 - W * (1 - k)), c28q4 = Math.max(0, c28 - 472);
  const P = Object.assign({}, baseP, { ricavi27_k: R, ricavi28_k: R, scen_extra: leave ? -5718 : 0,
    cig_o_27q1: q13, cig_o_27q2: q13, cig_o_27q3: q13, cig_o_27q4: q4, cig_o_28q1: c28, cig_o_28q2: c28, cig_o_28q3: c28, cig_o_28q4: c28q4 });
  const r = M.calcola(D, P); let min = 1e12, mm = '';
  r.mesi.forEach(function (ym) { if (r.righe[ym].chiusura < min) { min = r.righe[ym].chiusura; mm = ym; } });
  let cum = 0, mesi = 0; for (let m = 0; m < 36; m++) { const y = Math.floor(m / 12), mo = m % 12; cum += y === 0 ? (mo < 9 ? q13 : q4) : (mo < 9 ? c28 : c28q4); mesi++; if (cum >= CAP) break; }
  rows.push({ R, leave, cig_q13: Math.round(q13), cig_q4: Math.round(q4), cig_2028: Math.round(c28), utile27: Math.round(r.ce27.utile), utile28: Math.round(r.ce28.utile), cassa27: Math.round(r.riepilogo.cassa_2027), cassa28: Math.round(r.riepilogo.cassa_2028), min: Math.round(min), mese_min: mm, mesi_al_tetto: cum >= CAP ? mesi : '>36' });
}
[true, false].forEach(function (l) { [2000, 1600, 1400].forEach(function (R) { run(R, l); }); });
console.table(rows);
