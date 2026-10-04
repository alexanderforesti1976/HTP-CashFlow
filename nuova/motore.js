/* Motore del cash flow 2026-2027 — solo calcolo, nessun DOM. Usato dalla pagina e dal test (tools/test_motore.js).
   Dati passati e scadenzari: da dati.json (bloccati). Parametri futuri: oggetto P (modificabili nella pagina). Importi in euro. */
(function (root) {
  var MESI = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'];
  var NOMI_MESI_ORD = { 'Gen 27': '2027-01', 'Feb 27': '2027-02', 'Mar 27': '2027-03', 'Apr 27': '2027-04', 'Mag 27': '2027-05' };
  // Fotovoltaico: risparmio e RID mensili indicativi (forma PVGIS a 15° sul totale E.ON 109.218 kWh/anno, autoconsumo 70%, 0,2925 €/kWh; RID 0,09 €/kWh)
  var FV_RISPARMIO = [987, 1253, 1975, 2240, 2551, 2715, 2889, 2551, 2011, 1454, 923, 814];
  var FV_RID = [130, 165, 260, 295, 336, 358, 381, 336, 265, 192, 122, 107];

  function parametriDefault(D) {
    var d = D.cf.defaults, G = D.cf.giacenze_30_06;
    // magazzino 31/12/2026 e 2027: valore di partenza = giacenze al 30/06 (indicazione di Alex 03/10), modificabile per categoria
    var F26 = { pf: G.prodotto_finito, sl: G.semilavorato, mp: G.materia_prima, imb: G.imballi };
    return {
      cig26_lavoratori: 1, cig26_ore: 15, cig26_da: '2026-09', cig26_a: '2026-12', cig27_lavoratori: 6, cig27_ore: 30, cig27_da: '2027-01', cig27_a: '2027-12',
      ricavi27_k: 2100, quota_non_confermato: 100,
      pct_lavorazioni: d.pct_lavorazioni, pct_provvigioni: d.pct_provvigioni,
      pers_mese: d.pers_mese, affitti_mese: d.affitti_mese, energia_mese: d.energia_mese,
      altri_ricorrenti_mese: d.altri_ricorrenti_mese, costi_irregolari_mese: d.costi_irregolari_mese,
      fv_produzione_pct: 100, fv_canone_da: '2026-11', fv_canone: 1393.58,
      g30_pf: G.prodotto_finito, g30_sl: G.semilavorato, g30_mp: G.materia_prima, g30_imb: G.imballi,
      f26_pf: F26.pf, f26_sl: F26.sl, f26_mp: F26.mp, f26_imb: F26.imb, f27_pf: F26.pf, f27_sl: F26.sl, f27_mp: F26.mp, f27_imb: F26.imb,
      imposte_2026: 0, acconto_prima_rata_pct: 50,
      ammortamenti_2026: d.ammortamenti_2026, ammortamenti_2027: d.ammortamenti_2027, rimanenze_finali_2027: d.rimanenze_finali_2026, rimanenze_finali_2026: d.rimanenze_finali_2026, var_ires: D.cf.ce2026.variazioni_fiscali['2026'].totale, var_ires_27: D.cf.ce2026.variazioni_fiscali['2027'].totale, add_irap: D.cf.ce2026.compenso_amministratore_anno + D.cf.ce2026.multe_indeducibili_gen_ago, add_irap_27: D.cf.ce2026.compenso_amministratore_anno
    };
  }

  function calcola(D, P) {
    var somma = function (p) { return (P[p + '_pf'] || 0) + (P[p + '_sl'] || 0) + (P[p + '_mp'] || 0) + (P[p + '_imb'] || 0); };
    P = Object.assign({}, P, { giacenza_30_06: somma('g30'), rimanenze_finali_2026: somma('f26'), rimanenze_finali_2027: somma('f27') });
    var C = D.cf, IR = C.iva.aliquota / 100, IE = C.iva.energia / 100, PL = C.iva.quota_plafond_acquisti / 100, QD = C.iva.quota_vendite_default / 100;
    var YM = []; for (var y = 2026; y <= 2027; y++) for (var mo = 1; mo <= 12; mo++) YM.push(y + '-' + (mo < 10 ? '0' : '') + mo);
    var FROM = YM.indexOf('2026-09');
    // CIG: riduce il costo del personale solo nei mesi del periodo scelto (da - a), con lavoratori e % ore dell'anno (regola Alex: lavoratori/20 x costo x % ore x 80%)
    var persM = function (ym) {
      var is26 = ym < '2027-01', w = is26 ? P.cig26_lavoratori : P.cig27_lavoratori, h = is26 ? P.cig26_ore : P.cig27_ore;
      var da = is26 ? P.cig26_da : P.cig27_da, a = is26 ? P.cig26_a : P.cig27_a;
      return P.pers_mese - (ym >= da && ym <= a ? w / 20 * P.pers_mese * h / 100 * 0.80 : 0);
    };
    var sumSD = 0, sum27 = 0;
    ['2026-09', '2026-10', '2026-11', '2026-12'].forEach(function (ym) { sumSD += persM(ym); });
    ['2027-01', '2027-02', '2027-03', '2027-04', '2027-05', '2027-06', '2027-07', '2027-08', '2027-09', '2027-10', '2027-11', '2027-12'].forEach(function (ym) { sum27 += persM(ym); });
    var RT = { mat: 0, mat27: 0, sub: P.pct_lavorazioni / 100, prov: P.pct_provvigioni / 100 };
    var fvK = P.fv_produzione_pct / 100;
    var mesiNC = { '2026-09': 'Settembre', '2026-10': 'Ottobre', '2026-11': 'Novembre', '2026-12': 'Dicembre' };
    // ricavi mensili
    var W = {}; Object.keys(C.ricavi_2026_mensili).forEach(function (k) { W[k] = C.ricavi_2026_mensili[k]; });
    Object.keys(C.ricavi).forEach(function (k) { W[k] = C.ricavi[k]; });
    var ord27 = {}; Object.keys(C.ordini_2027).forEach(function (k) { ord27[NOMI_MESI_ORD[k] || k] = C.ordini_2027[k]; });
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
    // Materie: consumo gen-giu = acquisti + rimanenze iniziali - giacenza al 30/06 (valore finale di Alex) = rapporto consumo/ricavi;
    // lug-dic e 2027: ACQUISTI in proporzione ai ricavi con quel rapporto; la giacenza finale (31/12) e un valore scelto da Alex:
    // consumo = acquisti + iniziali - finali, quindi ogni euro di giacenza finale in piu e un euro di risultato in piu.
    var Hh = D.h1;
    var rCons = (Hh.materie + C.ce2026.esistenze_iniziali - P.giacenza_30_06) / Hh.ricavi_operativi;
    RT.mat = rCons; RT.mat27 = rCons;
    var purch = {}; YM.forEach(function (ym) { purch[ym] = (REV[ym] || 0) * ((ym >= '2027-01' ? RT.mat27 : RT.mat) + RT.sub); });
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
    // CE 2026: gen-ago reale, set-dic da regole (variabile in proporzione ai ricavi, fisso per mese); imposte automatiche
    var E = C.ce2026, H = D.h1, M7 = D.mesi['7'], M8 = D.mesi['8'];
    var ric26 = H.ricavi_operativi + M7.ricavi_operativi + M8.ricavi_operativi, ricSD = 0; YM.slice(8, 12).forEach(function (ym) { ric26 += REV[ym]; ricSD += REV[ym]; }); // gen-giu = ricavi reali della bozza (vendite + stampi + diversi), non la somma dei mesi di consegna
    var gsum = function (k) { return H[k] + M7[k] + M8[k]; };
    var SD = ['2026-09', '2026-10', '2026-11', '2026-12'];
    var ce = { ricavi: ric26 };
    ce.rim_fin = P.rimanenze_finali_2026; ce.rim_in = E.esistenze_iniziali; ce.rimanenze = ce.rim_fin - ce.rim_in;
    var EC = E.esistenze_iniziali_categorie;
    // A2 (valore della produzione): prodotti finiti + semilavorati; B11 (costi): materie prime + imballi/consumo
    ce.a2_in = EC.prodotti_finiti + EC.semilavorati; ce.a2_fin = P.f26_pf + P.f26_sl;
    ce.b11_in = EC.materie_prime + EC.materiali_consumo_imballi; ce.b11_fin = P.f26_mp + P.f26_imb;
    ce.materie = gsum('materie') + ricSD * RT.mat; ce.lavorazioni = gsum('lavorazioni_terzi') + ricSD * RT.sub;
    ce.provvigioni = gsum('provvigioni') + ricSD * RT.prov; ce.royalties = 0.015 * ric26;
    ce.personale = gsum('personale') + sumSD + E.integrazioni.tfr_da_aggiungere + E.integrazioni.tredicesima_con_contributi;
    ce.affitti = gsum('affitti') + 4 * P.affitti_mese;
    var enSD = 0, canSD = 0; SD.forEach(function (ym) { enSD += P.energia_mese - fvSave(ym); if (ym >= P.fv_canone_da) canSD += P.fv_canone; });
    ce.energia = gsum('energia') + enSD;
    ce.altri = gsum('altri_costi') + 4 * (P.altri_ricorrenti_mese + P.costi_irregolari_mese) + canSD;
    var lm = function (k) { return M7[k] + M8[k]; }, ricLM = lm('ricavi_operativi');
    ce.parti = {
      ricavi: [H.ricavi_operativi, ricLM, ricSD], materie: [H.materie, lm('materie'), ricSD * RT.mat], lavorazioni: [H.lavorazioni_terzi, lm('lavorazioni_terzi'), ricSD * RT.sub],
      provvigioni: [H.provvigioni, lm('provvigioni'), ricSD * RT.prov], royalties: [0.015 * H.ricavi_operativi, 0.015 * ricLM, 0.015 * ricSD],
      personale: [H.personale, lm('personale'), sumSD], affitti: [H.affitti, lm('affitti'), 4 * P.affitti_mese], energia: [H.energia, lm('energia'), enSD],
      altri: [H.altri_costi, lm('altri_costi'), 4 * (P.altri_ricorrenti_mese + P.costi_irregolari_mese) + canSD]
    };
    ce.tfr13 = E.integrazioni.tfr_da_aggiungere + E.integrazioni.tredicesima_con_contributi;
    ce.consumo_materie = ce.materie + ce.rim_in - ce.rim_fin; ce.consumo_pct_gen_giu = rCons; ce.acquisti_pct_setdic = RT.mat;
    ce.ammortamenti = P.ammortamenti_2026;
    ce.operativo = ce.ricavi + ce.rimanenze - ce.materie - ce.lavorazioni - ce.provvigioni - ce.royalties - ce.personale - ce.affitti - ce.energia - ce.altri - ce.ammortamenti;
    ce.int_passivi = E.interessi_passivi_gen_ago + E.interessi_passivi_set_dic_piani;
    ce.int_attivi = E.interessi_attivi_gen_ago + E.ricavi_titoli_gen_giu + 1900 * 2 + 5950.68;
    ce.ante_tfm = ce.operativo - ce.int_passivi + ce.int_attivi;
    ce.tfm = Math.max(0, 0.20 * ce.ante_tfm);
    ce.ante_imposte = ce.ante_tfm - ce.tfm;
    ce.imponibile_ires = ce.ante_imposte + P.var_ires; ce.ires = Math.max(0, 0.24 * ce.imponibile_ires);
    ce.imponibile_irap = ce.operativo + P.add_irap; ce.irap = Math.max(0, 0.039 * ce.imponibile_irap);
    ce.imposte = ce.ires + ce.irap; ce.utile = ce.ante_imposte - ce.imposte;
    // CE 2027: tutto da previsione con le stesse regole (ricavi dei parametri, variabili in %, fissi per mese, CIG 2027, fotovoltaico a regime)
    var Y27 = YM.slice(12), ric27 = 0, en27 = 0, can27 = 0;
    Y27.forEach(function (ym) { ric27 += REV[ym]; en27 += P.energia_mese - fvSave(ym); if (ym >= P.fv_canone_da) can27 += P.fv_canone; });
    var base26p = gsum('personale') + sumSD, scala = sum27 / base26p, c7 = { ricavi: ric27 };
    c7.rim_fin = P.rimanenze_finali_2027; c7.rim_in = P.rimanenze_finali_2026; c7.rimanenze = c7.rim_fin - c7.rim_in;
    c7.a2_in = P.f26_pf + P.f26_sl; c7.a2_fin = P.f27_pf + P.f27_sl; c7.b11_in = P.f26_mp + P.f26_imb; c7.b11_fin = P.f27_mp + P.f27_imb;
    c7.materie = ric27 * RT.mat27; c7.lavorazioni = ric27 * RT.sub; c7.provvigioni = ric27 * RT.prov; c7.royalties = 0.015 * ric27;
    c7.personale = sum27 + (E.integrazioni.tfr_da_aggiungere + E.integrazioni.tredicesima_con_contributi) * scala;
    c7.affitti = 12 * P.affitti_mese; c7.energia = en27; c7.altri = 12 * (P.altri_ricorrenti_mese + P.costi_irregolari_mese) + can27;
    c7.consumo_materie = c7.materie + c7.rim_in - c7.rim_fin; c7.acquisti_pct = RT.mat27;
    c7.ammortamenti = P.ammortamenti_2027;
    c7.operativo = c7.ricavi + c7.rimanenze - c7.materie - c7.lavorazioni - c7.provvigioni - c7.royalties - c7.personale - c7.affitti - c7.energia - c7.altri - c7.ammortamenti;
    c7.int_passivi = E.interessi_passivi_2027_piani; c7.int_attivi = 1900 * 4 + 5950.68 * 2;
    c7.ante_tfm = c7.operativo - c7.int_passivi + c7.int_attivi; c7.tfm = Math.max(0, 0.20 * c7.ante_tfm); c7.ante_imposte = c7.ante_tfm - c7.tfm;
    c7.imponibile_ires = c7.ante_imposte + P.var_ires_27; c7.ires = Math.max(0, 0.24 * c7.imponibile_ires);
    c7.imponibile_irap = c7.operativo + P.add_irap_27; c7.irap = Math.max(0, 0.039 * c7.imponibile_irap);
    c7.imposte = c7.ires + c7.irap; c7.utile = c7.ante_imposte - c7.imposte;
    var OUT = YM.slice(YM.indexOf('2026-10')), rows = {}, cassa = C.cassa_30_09;
    var p1 = P.acconto_prima_rata_pct / 100, base26 = 124249, t26 = P.imposte_2026 > 0 ? P.imposte_2026 : ce.imposte;
    var cred = Math.max(0, base26 - t26), giu27 = t26 * p1 + (t26 - base26 > 0 ? t26 - base26 : -Math.min(cred, t26 * p1)), res = Math.max(0, cred - t26 * p1);
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
      L.personale = persM(ym) + (ym === '2026-12' || ym === '2027-12' ? 35000 : 0) + (ym === '2027-01' ? 17200 : 0);
      L.affitti = P.affitti_mese;
      L.energia = (P.energia_mese - fvSave(prev)) * (1 + IE);
      L.altri = P.altri_ricorrenti_mese * (1 + IR);
      L.irreg = P.costi_irregolari_mese * (1 + IR);
      L.provvigioni = (REV[prev] || 0) * RT.prov;
      L.royalties = ROY[ym] || 0;
      L.canone = ym >= P.fv_canone_da ? P.fv_canone * (1 + IR) : 0;
      L.finanz = C.finanziamenti_mensili[ym] || 0;
      L.rateAcconti = ym === '2026-10' ? 10610.00 : (ym === '2026-11' ? 4112.48 : 0);
      L.accontiBase = ym === '2026-11' ? base26 * (1 - p1) : (ym === '2027-06' ? giu27 : (ym === '2027-11' ? Math.max(0, t26 * (1 - p1) - res) : 0));
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
      mesi: OUT, righe: rows, ricavi: REV, ce: ce, ce27: c7,
      riepilogo: {
        cassa_2026: rows['2026-12'].chiusura, cassa_2027: rows['2027-12'].chiusura, minimo: minC, mese_minimo: minM,
        entrate_2026: tot('2026', 'entrate'), uscite_2026: tot('2026', 'uscite'), entrate_2027: tot('2027', 'entrate'), uscite_2027: tot('2027', 'uscite'),
        imposte_2026: t26, utile_2026: ce.utile, utile_2027: c7.utile, netto_2026: tot('2026', 'netto'), netto_2027: tot('2027', 'netto')
      }
    };
  }
  root.Motore = { calcola: calcola, parametriDefault: parametriDefault, MESI: MESI };
  if (typeof module !== 'undefined') module.exports = root.Motore;
})(typeof window !== 'undefined' ? window : this);
