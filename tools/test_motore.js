// Test del motore: con i parametri di partenza deve dare gli stessi numeri del calcolo di R078 (cassa 31/12/2026 e 31/12/2027).
const fs = require('fs'), M = require('../nuova/motore.js');
const D = JSON.parse(fs.readFileSync(__dirname + '/../nuova/dati.json', 'utf8'));
const CIG_ZERO = { cig_o_26q4: 0, cig_o_27q1: 0, cig_o_27q2: 0, cig_o_27q3: 0, cig_o_27q4: 0 }, PALEX = M.parametriDefault(D); // PALEX = valori di partenza (CIG di Alex); i confronti sotto sono a CIG zero
const P0 = Object.assign({}, PALEX, CIG_ZERO), P = Object.assign({}, P0, { imposte_2026: 124249 }), r = M.calcola(D, P).riepilogo; // R078: imposte 2026 fissate = acconti pagati
const att = { cassa_2026: 1942754.61, cassa_2027: 1696020.13 }; // R160: provvigioni 2027 senza Tusa (era 1608975.25, +27.332); R158: ricavi 2027 2.000k e non confermati 90% (valori di Alex; prima 1922518.43 e 1689680.05); R150: incassi 2027 cliente per cliente (era 1706462.19, -16.782); R136: ore di CIG al mese; R135: CIG di partenza zero; R132: nessun anticipo CIG (paga INPS); R129: CIG da legge (addizionale); R115: giacenze 30/06 = 176.608; R113: acquisti in % dei ricavi, giacenza finale = leva; R110: giacenze 30/06 = 164.739; R109: matrice incassi da PDF; R108: ordini da PDF 03/10 con date; R105: metodo consumo con giacenza 30/06 (imposte 2026 forzate a 124.249 come R078)
let ok = true;
for (const k in att) { const d = Math.round((r[k] - att[k]) * 100) / 100; console.log(k, r[k].toFixed(2), 'atteso', att[k], 'diff', d); if (Math.abs(d) > 10) ok = false; }
console.log('minimo', r.minimo.toFixed(2), r.mese_minimo, '| entrate 2027', r.entrate_2027.toFixed(2), 'uscite 2027', r.uscite_2027.toFixed(2));
// sensibilità: CIG 2027 a zero deve ALZARE le uscite 2027 del costo (un tagliare costi alza la cassa)
const CIG27 = { cig_o_27q1: 312, cig_o_27q2: 312, cig_o_27q3: 312, cig_o_27q4: 312 };
const P2 = Object.assign({}, P, CIG27), r2 = M.calcola(D, P2).riepilogo;
console.log('CIG 2027 (6 persone x 52 ore al mese): uscite 2027', r2.uscite_2027.toFixed(2), '(più basse di', r.uscite_2027.toFixed(2) + ', CIG di partenza = zero)'); if (!(r2.uscite_2027 < r.uscite_2027)) ok = false;
const P3 = Object.assign({}, P, { g30_mp: P.g30_mp - 20000 }), r3 = M.calcola(D, P3).riepilogo;
console.log('giacenza 30/06 -20.000: consumo piu alto, cassa 2027', r3.cassa_2027.toFixed(2), '(più bassa di', r.cassa_2027.toFixed(2) + ')'); if (!(r3.cassa_2027 < r.cassa_2027)) ok = false;
const ra = M.calcola(D, P0); console.log('imposte 2026 automatiche', ra.riepilogo.imposte_2026.toFixed(2), '= IRES', ra.ce.ires.toFixed(2), '+ IRAP', ra.ce.irap.toFixed(2), '| utile', ra.ce.utile.toFixed(2)); if (Math.abs(ra.ce.imposte - ra.riepilogo.imposte_2026) > 0.01 || ra.ce.imposte <= 0) ok = false;
const rb = M.calcola(D, Object.assign({}, P0, { ammortamenti_2026: 200000 })); console.log('ammortamenti +90k: utile', rb.ce.utile.toFixed(0), '(più basso di', ra.ce.utile.toFixed(0) + ')'); if (!(rb.ce.utile < ra.ce.utile && rb.ce.imposte < ra.ce.imposte)) ok = false;
console.log('CE 2027: operativo', ra.ce27.operativo.toFixed(0), 'utile', ra.ce27.utile.toFixed(0), 'imposte', ra.ce27.imposte.toFixed(0)); if (!(ra.ce27.ricavi >= 2.0e6 && ra.ce27.imposte > 0)) ok = false;
const rc = M.calcola(D, Object.assign({}, P0, CIG27)); console.log('CIG 2027 inserita: utile 2027', rc.ce27.utile.toFixed(0), '(più alto di', ra.ce27.utile.toFixed(0) + ', CIG di partenza = zero)'); if (!(rc.ce27.utile > ra.ce27.utile)) ok = false;
const rf = M.calcola(D, Object.assign({}, P0, { f26_mp: P0.f26_mp + 10000 })); console.log('magazzino finale 2026 +10.000: risultato operativo 2026', rf.ce.operativo.toFixed(0), '(+10.000 su', ra.ce.operativo.toFixed(0) + ')'); if (Math.abs(rf.ce.operativo - ra.ce.operativo - 10000) > 1) ok = false;
// Riscontro sul bilancio 2025 (imposte pagate: IRES 102.280, IRAP 21.969) con le stesse regole: IRES 24% su utile ante imposte + variazioni; IRAP 3,9% su risultato operativo + non deducibili
const ante25 = 296071.79, op25 = 364600;
const var25 = 83508.75 + 4894.83 + 0.8 * (6485.95 + 5111.06 + 829.52 + 1655.73 + 1422.76 + 2224.91 + 1618.54 + 3428.30 + 21346.83) + 0.3 * (1765.57 + 1269.55 + 17321.50 + 1646.10) + 0.2 * (2402.19 + 1627.20 + 456.17);
const ires25 = 0.24 * (ante25 + var25), irap25 = 0.039 * (op25 + 19420 + 67386.33 + 23489.65 + 83508.75 + 2000);
console.log('2025: IRES calcolata', ires25.toFixed(0), 'pagata 102280 | IRAP calcolata', irap25.toFixed(0), 'pagata 21969');
if (Math.abs(ires25 / 102280 - 1) > 0.02 || Math.abs(irap25 / 21969 - 1) > 0.02) ok = false;
// periodo CIG: CIG 2027 (6 lavoratori 30%) solo gen-mar 2027 deve costare piu di tutto l'anno; CIG dal 2026-11 al 2027-01 riduce il personale solo in quei mesi
const rg = M.calcola(D, Object.assign({}, P0, { cig_o_27q1: 312 })); console.log('CIG 2027 solo nel 1o trimestre: personale 2027', rg.ce27.personale.toFixed(0), '(più alto di', rc.ce27.personale.toFixed(0) + ', CIG in tutto l\'anno)'); if (!(rg.ce27.personale > rc.ce27.personale && rg.ce27.personale < ra.ce27.personale)) ok = false;
const rp = M.calcola(D, Object.assign({}, P0, { cig_o_26q4: 215, cig_o_27q1: 215 }));
const dm = rp.righe['2026-11'].personale - ra.righe['2026-11'].personale;
console.log('CIG 5 persone x 43 ore al mese: personale nov', dm.toFixed(0)); if (!(dm < 0)) ok = false;
// la CIG del 2026 non deve cambiare il risultato 2027; la CIG del 2027 lo deve alzare
const rz = M.calcola(D, Object.assign({}, P0, { cig_o_26q4: 0 })), rq = M.calcola(D, Object.assign({}, P0, { cig_o_26q4: 435 }));
console.log('utile 2027 con e senza CIG nel 2026:', rq.ce27.utile.toFixed(0), rz.ce27.utile.toFixed(0)); if (Math.abs(rq.ce27.utile - rz.ce27.utile) > 1) ok = false;
// CIG di partenza zero: nessun risparmio sul personale
if (Math.abs(ra.ce27.personale - (12 * (P0.pers_mese - 6516) + (D.cf.ce2026.integrazioni.tfr_da_aggiungere + D.cf.ce2026.integrazioni.tredicesima_con_contributi) * (P0.pers_mese - 6516) / P0.pers_mese)) > 1) ok = false; // R164: due dimissioni senza sostituto (-3.807 e -2.709 al mese; ratei in proporzione)
// valori di partenza = CIG impostata da Alex (384 ore al mese ott-dic 2026 e nei primi tre trimestri 2027): utile come nella sua pagina del 04/10 22:09
const rA = M.calcola(D, PALEX); console.log('valori di partenza (CIG di Alex): utile 2026', rA.ce.utile.toFixed(0), 'utile 2027', rA.ce27.utile.toFixed(0), '(attesi 99709 e 124893: CIG di Alex, ricavi 2027 2.000k, non confermati 90%)'); if (Math.abs(rA.ce.utile - 99709) > 2 || Math.abs(rA.ce27.utile - 124893) > 2) ok = false;
// CIG anticipata in busta (R161): 384 ore x min(80% paga oraria media, 1.423,69/176) = 3.106 euro anticipati in ottobre e recuperati a novembre; non è costo
console.log('CIG anticipata: ottobre', rA.righe['2026-10'].cigAnticipo.toFixed(0), 'rimborso novembre', rA.righe['2026-11'].cigRimborso.toFixed(0));
if (Math.abs(rA.righe['2026-10'].cigAnticipo - 432 * 1423.69 / 176) > 1 || Math.abs(rA.righe['2026-11'].cigRimborso - rA.righe['2026-10'].cigAnticipo) > 0.01 || Math.abs(rA.righe['2027-12'].cigAnticipo - 360 * 1423.69 / 176) > 1) ok = false;
// CE 2028 (R174): sulla base del 2027, senza CIG, 3 persone in meno (organico 19): personale = 12 x (costo mensile - 6.516) x 16/19 + 13ª e TFR in proporzione
const c8 = rA.ce28, f28 = 16 / 19, pm28 = (P0.pers_mese - 6516) * f28;
const att28 = 12 * pm28 + (D.cf.ce2026.integrazioni.tfr_da_aggiungere + D.cf.ce2026.integrazioni.tredicesima_con_contributi) * pm28 / P0.pers_mese;
console.log('CE 2028: personale', c8.personale.toFixed(0), '(atteso', att28.toFixed(0) + ') utile', c8.utile.toFixed(0));
if (Math.abs(c8.personale - att28) > 1 || Math.abs(c8.ricavi - 2000000) > 1) ok = false;
const c80 = M.calcola(D, Object.assign({}, PALEX, { persone_in_meno_28: 0 })).ce28; if (!(c80.personale > c8.personale && c80.utile < c8.utile)) ok = false;
const c8g = M.calcola(D, Object.assign({}, PALEX, { cig_o_27q1: 0, cig_o_27q2: 0, cig_o_27q3: 0, cig_o_27q4: 0, cig_o_26q4: 0 })).ce28; if (Math.abs(c8g.utile - c8.utile) > 1) ok = false; // il 2028 non dipende dalla CIG
console.log(ok ? 'TEST OK' : 'TEST FALLITO'); process.exit(ok ? 0 : 1);
