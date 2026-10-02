# HTP-CashFlow — istruzioni per Claude

App unica (`index.html`, GitHub Pages) con due tab: **Cash Flow** | **Contabilità Industriale** di High Tech Project S.r.l. (overmolding gomma-metallo/gomma-plastica, ~19 dipendenti, Palazzolo s/O). Rispondi in italiano, tecnico e diretto, brevissimo, un passo alla volta.

## Come lavorare
- Storico e motivazioni delle decisioni del 02/10/2026 (CE 2026, imposte, fornitori, errori fatti): `docs/RIEPILOGO_02-10-2026.md`. Leggilo all'inizio di ogni sessione insieme a questo file.
- **REGOLA: aggiorna sempre.** A ogni nuovo PDF/dato (ordini aperti Pegaso, scadenziari, mastrini) rigenera subito `params.json` (OBACKLOG, OREV, `nc`, ORDCRIT, `_backlogSource`), ricalcola il totale anno, aggiorna "Stato" e "Aperto" in CLAUDE.md, poi commit + push su `main`. Non limitarti a segnalare.
- Pubblica direttamente con `git commit` + `git push` su questo repo. Niente token, niente browser, niente passaggi manuali per Alex.
- Metodo sempre più rapido e a minor consumo di token.
- Non deviare dall'architettura; niente over-engineering. Alex corregge spesso: prendi sul serio le correzioni.
- Mai inventare menu/opzioni dell'interfaccia: se non sai, dillo.

## Architettura
- Stato condiviso in memoria tra i due tab: `P`, `OREV`, `OBACKLOG`, `H1_2026_REALE`. Contabilità non fa più `fetch()` di params.json.
- `params.json` = fonte persistita (sync Firebase) dei parametri condivisi, incluso `H1_2026_reale`.
- Firebase: progetto `htp-tools`, RTDB `htp-tools-default-rtdb.europe-west1.firebasedatabase.app`; contabilità → `htp_contabilita` (state), cash flow → `htp_cashflow`.
- Repo `HTP-Contabilita` ora fa solo redirect qui.
- Fattori stagionali capacità (agosto, dicembre ridotti) uguali in tutti i tool.

## Convenzioni contabili
- Royalties 1,5% ricavi (1% + 0,5%) = costo variabile; H1 più basso = effetto timing.
- Conto 107011300 "Variazione ricavi x resi e premi" €41.502,04 = storno Terra Verde nei costi con rifatturazione a ricavo (Enextras): mantenere, ed escluderlo dai confronti costi.
- Ammortamenti, TFM, imposte calcolati da params, mai hardcoded.
- Cash flow con tutto ciò che muove cassa, IVA inclusa, per aliquote/regimi reali (22%, 10%, non imponibile/dichiarazione d'intento), non percentuali medie.
- Obiettivo 2.250k = ricavi netti IVA. Consuntivo + ordini NON vanno scalati: se superano l'obiettivo, segnalare "SFORATO".
- Slittamento scadenze (RiBa fine mese SENZA +10, mai bonifici): 31/08→10/09 e 31/12→10/01. Fonte: `Condizioni_pagamento_clienti_fornitori_2026-10-02.xlsx` (colonne Tipo pag. R, Fine mese, Giorni dopo fine mese). Fornitori: lo slittamento è dentro `payMatrix` (`shiftSupPct`=0). Clienti: `shiftCustPct` 0 (verso i clienti nessuno slittamento: confermato da Alex/Valentina, i nostri clienti non hanno +10). Fornitori principali materie con +10 (Hexpol, PMG, EU Silicones, Selini); **senza +10 e RiBa: GBS (R35), Lav.El., Gom-Fer, Zanini, Zincover, ecc.**
- Imposte nel cash flow: acconti anno N = 100% imposte N-1 (`accontoSplit` 0,5: giugno/novembre; 2026: 62k + 62k su imposte 2025 = 124k); giugno N+1 = saldo N (imposte N − acconti) + 1a rata acconto N+1; saldo a credito compensato nel mese (residuo con la rata successiva). Imposte 2026 = 51,0k (CE H1 reale + H2) → saldo 2026 a credito −73k: giu-27 0, nov-27 0.
- Credito IVA recuperato con dichiarazione annuale (`ivaRecoveryYM` 2027-04), non TR trimestrali.
- Input reali (scadenzari/registri Pegaso, condizioni per cliente/fornitore), non medie uniformi.
- Pegaso ordini: consegna 31/12/2099 = in attesa conto lavoro (vale data richiesta); 31/12/2100 = programma (data richiesta = data massima ritiro; ripartire sullo storico ritiri). Non sommarli alle consegne confermate.
- Mastrini completi arrivano a metà ottobre col trimestrale; quelli precedenti hanno l'ultimo mese incompleto.

## Stato al 02/10/2026
- **Cassa 30/09/2026 = 1.279,66k** (`startCash`, `cashAnchor` 2026-09): 4 c/c lordo 1.870,46k − Cedola Long 400 − F.do BTP 150 − Onemarkets 40,8. Polizza Assicomo 75k non nettata. Proiezione da ottobre.
- Incassi/pagamenti reali lug-set (`actualIn` 174,1/214,8/126,3; `actualOut` 111,6/57,3/79,2) solo in tabella.
- Ricavi: lug 213,6k, ago 91,8k (mastrini 07011000), set 220k (`OREV[2]`: 142,5 emessi + 77,5 da emettere). H1 2026 `h1Rev` 1.248,7k. Totale anno 2.304,9k (H1 1.248,7 + H2 1.056,2; SFORATO +54,9k), ricalcolato 02/10 dopo backlog rigenerato.
- Crediti/debiti aperti (Pegaso 02/10): `openRecSched` {ott 216,2; nov 66,1} lordi IVA; `openPaySched` {ott 77,8; nov 24,2; dic 10,3; gen27 19,6} (rigenerato 02/10 da scadenzario fornitori con parser verificato sui totali PDF: Dare 949.004,13 / Avere 1.061.303,72 / aperto 112.299,59; RiBa pagate a scadenza, bonifici +17 gg, scaduti in ottobre; + 5 fatture set con scadenza 2027 dal registro IVA, 19,6k al 10/01) = quota già nota: fatture registrate fino a `purchRegYM` 2026-09 (registro IVA acquisti arriva al 30/09: ago 68,1k, set 59,6k già dentro) = quota già nota (Dic 26 ≈10,3k: Hexpol 4205/VEN 6,6k, PMG East 3,4k, Belometti, Lav.El.); la proiezione aggiunge gli acquisti di ott-dic con `payMatrix`: Dic 26 ≈11k per struttura (60 gg fine mese di ottobre scadono 31/12 → 10/01), Gen 27 ≈50k; `toInvoice` {2026-09: 77,5}.
- **DSO 60 gg; pagamenti fornitori da `payMatrix` (mese acquisto → mesi di ritardo), costruita fornitore per fornitore: peso fatture a credito da aprile (Hexpol 30%, FGR 13%, Selini 8%, PMG 8%, PMG East 6%, EU Silicones 5%…; pesi ricalcolati con parser verificato) × condizioni da anagrafica (giorni, dffm, +10, RiBa fine mese senza +10 ad agosto/dicembre → +1 mese); sostituisce il lag unico DPO 105** (condizioni reali: RiBa 60 dffm ≈75 gg; R35 90 dffm ≈105 gg per Lav.El., OMECA/Cavagna, OMR; Serotti bonifico 30; Enextras/Terra Verde/Arkimat anticipato; Dichtungspartner TT 60. Fornitori Hexpol/PMG/EU Silicones 90 dffm+10, GBS 90 dffm (senza +10 da anagrafica), Selini 60 dffm+10). Cassa minima 1.085k (dic-27; nov-26 1.123k), saldo dic-26 1.160k, dic-27 1.085k dopo l'allineamento dei parametri 2027.
- IVA: vendite 22% solo `taxClients` (T.Erre, Watts, Sagom, OMR, Dubhe, Scaligera, E.B., Breka, Elledi), resto non imponibile; acquisti materiali 52% senza IVA (plafond), resto 22%; energia 10%; altri 22%. Credito IVA iniziale 36,3k (`ivaCreditAnchor`, da verificare).
- Backlog ott-26/mag-27: T.Erre e OMECA = confermato + programma 2100 su media ritiri 12 mesi (21,85k/m, 11,5k/m). Edscha 53,9k scaduto escluso. Ott-dic 215,5/161,6/153,7k (backlog rigenerato da OrdiniVenditaAperti_2.pdf, stampa 02/10 17:50); T.Erre/OMECA = max(confermato, media ritiri). Non confermato in `OBACKLOG[].nc` (programmi 2100 + righe 2099 Watts/Lav.El.): 140,3k = 26,4% di 530,8k. Argomm: solo 260141 (24,3k, dic); ordine quadro ~1,8M da riemettere con nuovo prezzo (richiami fermi da luglio).
- Finanziamenti in `LOANS`/`loans` mensili (k€: `sched`, `cap`, `int`, `res`) da piani di ammortamento BCC 1066083 e 1071107, Unicredit 2529480, Credem 8630473; BCC Sebino 8021/Finlombarda da bilancio; Unicredit 8823317 e Mini da scadenziario Verusca. Interessi a CE = somma `int`; debito residuo = somma `res`. 2026: rate 436,4k, interessi 19,7k, residuo 31/12 435,9k, **DSCR 1,04x** (2027 ~1,2x).
- Personale all-in lug 54,3k / ago 48,8k (modello 58k), affitti 8,2k, energia 7,4/9,0k, royalties trimestrali ~9-10k a ottobre.

## Parametri 2027 e test
- 2027 allineato al ritmo reale 2026: personale come 2026 (`labor27` = `laborK` 58k/mese, nessuna CIG: 696k/anno), altri costi fissi 25k/mese (`otherFixedK27`), energia quasi fissa 7,5k/mese (`energyFixedK27`, sostituisce la % sul fatturato se > 0). CE 2027 con rev 2.000k: EBITDA 228,4k (era 314,6k), utile netto 73,9k (era 123,6k); saldo dic-27 1.085k.
- `params.json` → `_forceKeys`: elenco di parametri che prevalgono sulle modifiche manuali salvate nella pagina/Firebase (oggi i parametri 2027 sopra). Gli altri parametri modificati a mano nella pagina prevalgono sempre sul file.
- Da Code Firebase NON è raggiungibile (proxy dell'ambiente): i test usano `params.json`, quindi possono differire dalla pagina di Alex. Esempio: magazzino totale 153,4k (variazione rimanenze 2026 −15k) → utile 2026 109,0k invece di 131,9k (rimanenze 24,6k con magazzino 193k). Per testare lo stato reale servono i valori della pagina (screenshot dei Parametri).

## CE 2026 (calcPL)
- 2026 = H1 reale (`H1_2026_REALE`, riclassifica: mat = MP+materiali+imballi+PF; sub = lav. c/terzi; personale = salari+contributi+TFR+welfare; affitti = solo affitti; altri = leasing, noleggi, manutenzioni, pubblicità, consulenze, compenso amm., spese bancarie, altri G&A) + H2 previsto con i parametri sui ricavi lug-dic (h1Rev + ordini). Ammortamenti, rimanenze, TFM e imposte sull'anno intero. Interessi = H1 reale + piano H2.
- Utile 2026 131,9k (era 237,2k con le % su tutto l'anno): EBITDA 347,0k, imposte 51,0k, TFM 45,7k. Royalties 2026 = 1,5% dei ricavi su tutto l'anno (34,6k; H1 reale basso = timing). Personale H1 + ratei non presenti nel bilancio provvisorio, stima esplicita 40,3k (TFR 12,3 su salari H1 al 7,41% meno 5,1 già a bilancio; 13a tredK/2 = 19,0; ferie maturate `ferieH1K` = 9,0 STIMA da confermare), mostrati nel CE come "di cui ratei H1". `otherFixedK` 2026 = 25.

## Aperto
- Inserire `accontoGiu26` (acconto imposte giugno 2026 dall'F24, da Luca/Verusca): oggi stima 62k. Confermare `ferieH1K` (ratei ferie H1, stima 9k).
- Rigenerare `payMatrix` quando arrivano nuove fatture/condizioni (pesi fornitori da scadenzario).
- Mastrini/trimestrale metà ottobre: sostituire costi stimati lug-set.
- Conferma recupero credito IVA con Luca (Studio SGEA). Registro IVA vendite fermo al 21/09 (set 3,8k registrati vs 142,5k emessi).
- Plafond clienti (dichiarazioni d'intento): residui Lav.El. 58,3k (ott-nov 70,4k → ~12k oltre, IVA 22%), Cavagna/OMECA 35,8k (ott-dic ~37,6k), MCM 6,2k (ordine dic 14,0k). Servono nuove dichiarazioni o IVA sul superamento.
- Enextras FT108/FT117 (112,2k) e ordine 260143 (88,7k non spedito, chiedere a Giusi).
- Ritardi settembre: T.Erre programma 32,3k, Serotti 33,7k, Watts 18,9k.
- Classificazione IVA OMECA/Arkimat/locazione; storico ritiri vs mastrini; ripartizione T.Erre oltre tetti data.
- Piano ammortamento BCC Sebino 8021 (opzionale); magazzino al 30/06/2025.
- Argomm articolo 047002: cost breakdown per trattare il nuovo prezzo.
