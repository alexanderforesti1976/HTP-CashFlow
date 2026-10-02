/* Motore del cash flow 2026-2027 — solo calcolo, nessun DOM. Usato dalla pagina e dal test (tools/test_motore.js).
   Dati passati e scadenzari: da dati.json (bloccati). Parametri futuri: oggetto P (modificabili nella pagina). Importi in euro. */
(function (root) {
  var MESI = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'];
  var NOMI_MESI_ORD = { 'Gen 27': '2027-01', 'Feb 27': '2027-02', 'Mar 27': '2027-03', 'Apr 27': '2027-04', 'Mag 27': '2027-05' };
  // Fotovoltaico: risparmio e RID mensili indicativi (forma PVGIS a 15° sul totale E.ON 109.218 kWh/anno, autoconsumo 70%, 0,2925 €/kWh; RID 0,09 €/kWh)
  var FV_RISPARMIO = [987, 1253, 1975, 2240, 2551, 2715, 2889, 2551, 2011, 1454, 923, 814];
  var FV_RID = [130, 165, 260, 295, 336, 358, 381, 336, 265, 192, 122, 107];

  function parametriDefault(D) {
    var d = D.cf.defaults;
    return {
      cig26_lavoratori: 1, cig26_ore: 15, cig27_lavoratori: 6, cig27_ore: 30,
      ricavi27_k: 2100, quota_non_confermato: 100,
      pct_materie: d.pct_materie, pct_lavorazioni: d.pct_lavorazioni, pct_provvigioni: d.pct_provvigioni,
      pers_mese: d.pers_mese, affitti_mese: d.affitti_mese, energia_mese: d.energia_mese,
      altri_ricorrenti_mese: d.altri_ricorrenti_mese, costi_irregolari_mese: d.costi_irregolari_mese,
      fv_produzione_pct: 100, fv_canone_da: '2026-11', fv_canone: 1393.58,
      imposte_2026: 124249, acconto_prima_rata_pct: 50
    };
  }

  function calcola(D, P) {
    var C = D.cf, IR = C.iva.aliquota / 100, IE = C.iva.energia / 100, PL = C.iva.quota_plafond_acquisti / 100, QD = C.iva.quota_vendite_default / 100;
    var YM = []; for (var y = 2026; y <= 2027; y++) for (var mo = 1; mo <= 12; mo++) YM.push(y + '-' + (mo < 10 ? '0' : '') + mo);
    var FROM = YM.indexOf('2026-09');
    var pers = function (w, h) { return P.pers_mese - w / 20 * P.pers_mese * h / 100 * 0.80; };
    var pers26 = pers(P.cig26_lavoratori, P.cig26_ore), pers27 = pers(P.cig27_lavoratori, P.cig27_ore);
    var RT = { mat: P.pct_materie / 100, sub: P.pct_lavorazioni / 100, prov: P.pct_provvigioni / 100 };
    var fvK = P.fv_produzione_pct / 100;
    var mesiNC = { '2026-09': 'Settembre', '2026-10': 'Ottobre', '2026-11': 'Novembre', '2026-12': 'Dicembre' };
    // ricavi mensili
    var W = {}; Object.keys(C.ricavi_2026_mensili).forEach(function (k) { W[k] = C.ricavi_2026_mensili[k]; });
    Object.keys(C.ricavi).forEach(function (k) { W[k] = C.ricavi[k]; });
    var ord27 = {}; Object.keys(C.ordini_2027).forEach(function (k) { ord27[NOMI_MESI_ORD[k]] = C.ordini_2027[k]; });
    var sumOrd = 0; Object.keys(ord27).forEach(function (k) { sumOrd += ord27[k]; });
    var sumW = 0; for (var m1 = 1; m1 <= 12; m1++) sumW += W['2026-' + (m1 < 10 ? '0' : '') + m1];
    var rev27 = P.ricavi27_k * 1000, REV = {};
    YM.forEach(function (ym) {
      if (ym < '2027-01') {
        var nc = (C.non_confermato[mesiNC[ym]] || 0) * (1 - P.quota_non_confermato / 100);
        REV[ym] = (C.ricavi[ym] || 0) - nc;
      } else REV[ym] = (ord27[ym] || 0) + Math.max(0, rev27 - sumOrd) * W['2026-' + ym.slice(5)] / sumW;
    });
    var QS = function (ym) { return C.quota_iva_vendite[ym] !== undefined ? C.quota_iva_vendite[ym] : QD; };
    var purch = {}; YM.forEach(function (ym) { purch[ym] = (REV[ym] || 0) * (RT.mat + RT.sub); });
    var fvSave = function (ym) { return ym < '2026-11' ? 0 : FV_RISPARMIO[+ym.slice(5) - 1] * fvK; };
    var fvRid = function (ym) { return ym < '2026-11' ? 0 : FV_RID[+ym.slice(5) - 1] * fvK; };
    // IVA
    var ivaDeb = {}, ivaCrd = {};
    YM.forEach(function (ym, i) {
      if (i < FROM) return;
      ivaDeb[ym] = (REV[ym] || 0) * QS(ym) * IR;
      var en = P.energia_mese - fvSave(ym);
      ivaCrd[ym] = (purch[ym] || 0) * (1 - PL) * IR + en * IE + (P.altri_ricorrenti_mese + P.costi_irregolari_mese) * IR + (ym >= P.fv_canone_da ? P.fv_canone * IR : 0);
    });
    var ivaBal = -24925.00, ivaPay = {}, credDic = 0;
    YM.forEach(function (ym, i) {
      if (i < FROM) return;
      ivaBal += ivaDeb[ym] - ivaCrd[ym];
      if (ym === '2026-12') credDic = Math.max(0, -ivaBal);
      var nx = YM[i + 1]; if (nx && ivaBal > 0) { ivaPay[nx] = ivaBal; ivaBal = 0; }
    });
    var sumRoy = function (a, b, c) { return 0.015 * ((REV[a] || 0) + (REV[b] || 0) + (REV[c] || 0)); };
    var ROY = {
      '2026-10': 0.015 * (D.mesi['7'].ricavi_operativi + D.mesi['8'].ricavi_operativi + (REV['2026-09'] || 0)),
      '2027-01': sumRoy('2026-10', '2026-11', '2026-12'), '2027-04': sumRoy('2027-01', '2027-02', '2027-03'),
      '2027-07': sumRoy('2027-04', '2027-05', '2027-06'), '2027-10': sumRoy('2027-07', '2027-08', '2027-09')
    };
    var INAIL = ['2026-10', '2026-11', '2026-12', '2027-01', '2027-02', '2027-03', '2027-04'];
    var OUT = YM.slice(YM.indexOf('2026-10')), rows = {}, cassa = C.cassa_30_09;
    var p1 = P.acconto_prima_rata_pct / 100, base26 = 124249;
    OUT.forEach(function (ym, i) {
      var L = {}, ix = YM.indexOf(ym), prev = YM[ix - 1], is27 = ym >= '2027-01';
      L.apertiCli = C.aperti_clienti[ym] || 0;
      var nu = 0; for (var j = FROM; j <= ix; j++) { var ymr = YM[j], k = ix - j, row = C.rec_matrix[ymr] || C.rec_matrix['default']; if (k <= 6) nu += (row[k] || 0) * (REV[ymr] || 0) * (1 + QS(ymr) * IR); }
      L.nuoviCli = nu;
      L.rid = i >= 2 ? fvRid(YM[ix - 2]) : 0;
      L.ivaRel = ym === '2027-04' ? credDic : 0;
      L.prov = (['2026-12', '2027-06', '2027-12'].indexOf(ym) >= 0 ? 5950.68 : 0) + (['2026-12', '2027-03', '2027-06', '2027-09', '2027-12'].indexOf(ym) >= 0 ? 1900 : 0);
      L.apertiFor = C.aperti_fornitori[ym] || 0;
      var nf = 0; for (var j2 = FROM; j2 <= ix; j2++) { var pm = YM[j2], k2 = ix - j2; if (k2 > 6) continue; var base = purch[pm] - (pm === '2026-09' ? C.acquisti_settembre_registrati : 0); nf += ((C.pay_matrix[+pm.slice(5)] || [])[k2] || 0) * Math.max(0, base) * (1 + (1 - PL) * IR); }
      L.nuoviFor = nf;
      L.personale = (is27 ? pers27 : pers26) + (ym === '2026-12' || ym === '2027-12' ? 35000 : 0) + (ym === '2027-01' ? 17200 : 0);
      L.affitti = P.affitti_mese;
      L.energia = (P.energia_mese - fvSave(prev)) * (1 + IE);
      L.altri = P.altri_ricorrenti_mese * (1 + IR);
      L.irreg = P.costi_irregolari_mese * (1 + IR);
      L.provvigioni = (REV[prev] || 0) * RT.prov;
      L.royalties = ROY[ym] || 0;
      L.canone = ym >= P.fv_canone_da ? P.fv_canone * (1 + IR) : 0;
      L.finanz = C.finanziamenti_mensili[ym] || 0;
      L.rateAcconti = ym === '2026-10' ? 10610.00 : (ym === '2026-11' ? 4112.48 : 0);
      var t26 = P.imposte_2026;
      L.accontiBase = ym === '2026-11' ? base26 * (1 - p1) : (ym === '2027-06' ? t26 * p1 + Math.max(0, t26 - base26) : (ym === '2027-11' ? t26 * (1 - p1) : 0));
      L.accertamenti = ['2026-12', '2027-03', '2027-06', '2027-09'].indexOf(ym) >= 0 ? 9462.94 : 0;
      L.inail = INAIL.indexOf(ym) >= 0 ? 1873.98 : 0;
      L.iva = ivaPay[ym] || 0;
      L.entrate = L.apertiCli + L.nuoviCli + L.rid + L.ivaRel + L.prov;
      L.uscite = L.apertiFor + L.nuoviFor + L.personale + L.affitti + L.energia + L.altri + L.irreg + L.provvigioni + L.royalties + L.canone + L.finanz + L.rateAcconti + L.accontiBase + L.accertamenti + L.inail + L.iva;
      L.netto = L.entrate - L.uscite; L.apertura = cassa; cassa += L.netto; L.chiusura = cassa;
      L.ricavi = REV[ym] || 0;
      rows[ym] = L;
    });
    var tot = function (anno, k) { var x = 0; OUT.forEach(function (ym) { if (ym.slice(0, 4) === anno) x += rows[ym][k]; }); return x; };
    var minC = Infinity, minM = '';
    OUT.forEach(function (ym) { if (rows[ym].chiusura < minC) { minC = rows[ym].chiusura; minM = ym; } });
    return {
      mesi: OUT, righe: rows, ricavi: REV,
      riepilogo: {
        cassa_2026: rows['2026-12'].chiusura, cassa_2027: rows['2027-12'].chiusura, minimo: minC, mese_minimo: minM,
        entrate_2026: tot('2026', 'entrate'), uscite_2026: tot('2026', 'uscite'), entrate_2027: tot('2027', 'entrate'), uscite_2027: tot('2027', 'uscite'),
        netto_2026: tot('2026', 'netto'), netto_2027: tot('2027', 'netto')
      }
    };
  }
  root.Motore = { calcola: calcola, parametriDefault: parametriDefault, MESI: MESI };
  if (typeof module !== 'undefined') module.exports = root.Motore;
})(typeof window !== 'undefined' ? window : this);
