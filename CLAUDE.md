# HTP-CashFlow — istruzioni per Claude

App unica (`index.html`, GitHub Pages) con due tab: **Cash Flow** | **Contabilità Industriale** di High Tech Project S.r.l. (overmolding gomma-metallo/gomma-plastica, ~19 dipendenti, Palazzolo s/O). Rispondi in italiano, tecnico e diretto, brevissimo, un passo alla volta.

## Come lavorare
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
- Slittamento scadenze (RiBa fine mese SENZA +10, mai bonifici): 31/08→10/09 e 31/12→10/01. Fonte: `Condizioni_pagamento_clienti_fornitori_2026-10-02.xlsx` (colonne Tipo pag. R, Fine mese, Giorni dopo fine mese). Parametri `shiftMonths` {8→9, 12→1}, `shiftCustPct` 0 (verso i clienti nessuno slittamento: confermato da Alex/Valentina, i nostri clienti non hanno +10) e `shiftSupPct` 0 (fornitori: servono volumi acquisti per fornitore). Fornitori principali materie con +10 (Hexpol, PMG, EU Silicones, Selini); **senza +10 e RiBa: GBS (R35), Lav.El., Gom-Fer, Zanini, Zincover, ecc.**
- Credito IVA recuperato con dichiarazione annuale (`ivaRecoveryYM` 2027-04), non TR trimestrali.
- Input reali (scadenzari/registri Pegaso, condizioni per cliente/fornitore), non medie uniformi.
- Pegaso ordini: consegna 31/12/2099 = in attesa conto lavoro (vale data richiesta); 31/12/2100 = programma (data richiesta = data massima ritiro; ripartire sullo storico ritiri). Non sommarli alle consegne confermate.
- Mastrini completi arrivano a metà ottobre col trimestrale; quelli precedenti hanno l'ultimo mese incompleto.

## Stato al 02/10/2026
- **Cassa 30/09/2026 = 1.279,66k** (`startCash`, `cashAnchor` 2026-09): 4 c/c lordo 1.870,46k − Cedola Long 400 − F.do BTP 150 − Onemarkets 40,8. Polizza Assicomo 75k non nettata. Proiezione da ottobre.
- Incassi/pagamenti reali lug-set (`actualIn` 174,1/214,8/126,3; `actualOut` 111,6/57,3/79,2) solo in tabella.
- Ricavi: lug 213,6k, ago 91,8k (mastrini 07011000), set 220k (`OREV[2]`: 142,5 emessi + 77,5 da emettere). H1 2026 `h1Rev` 1.248,7k. Totale anno 2.304,9k (H1 1.248,7 + H2 1.056,2; SFORATO +54,9k), ricalcolato 02/10 dopo backlog rigenerato.
- Crediti/debiti aperti (Pegaso 02/10): `openRecSched` {ott 216,2; nov 66,1} lordi IVA; `openPaySched` {ott 63,4; nov 23,9; dic 8,4; gen27 19,8} = solo minimo: fatture registrate fino a `purchRegYM` 2026-07, dopo (ago/set non registrati) pagamento = max(scadenzario, piano acquisti con DPO) → dic ≈22k, gen27 ≈54k; `toInvoice` {2026-09: 77,5}.
- **DSO 60 gg, DPO 105 gg** (condizioni reali: RiBa 60 dffm ≈75 gg; R35 90 dffm ≈105 gg per Lav.El., OMECA/Cavagna, OMR; Serotti bonifico 30; Enextras/Terra Verde/Arkimat anticipato; Dichtungspartner TT 60. Fornitori Hexpol/PMG/EU Silicones 90 dffm+10, GBS 90 dffm (senza +10 da anagrafica), Selini 60 dffm+10). Cassa minima nov-26 ≈ 1.167k.
- IVA: vendite 22% solo `taxClients` (T.Erre, Watts, Sagom, OMR, Dubhe, Scaligera, E.B., Breka, Elledi), resto non imponibile; acquisti materiali 52% senza IVA (plafond), resto 22%; energia 10%; altri 22%. Credito IVA iniziale 36,3k (`ivaCreditAnchor`, da verificare).
- Backlog ott-26/mag-27: T.Erre e OMECA = confermato + programma 2100 su media ritiri 12 mesi (21,85k/m, 11,5k/m). Edscha 53,9k scaduto escluso. Ott-dic 215,5/161,6/153,7k (backlog rigenerato da OrdiniVenditaAperti_2.pdf, stampa 02/10 17:50); T.Erre/OMECA = max(confermato, media ritiri). Non confermato in `OBACKLOG[].nc` (programmi 2100 + righe 2099 Watts/Lav.El.): 140,3k = 26,4% di 530,8k. Argomm: solo 260141 (24,3k, dic); ordine quadro ~1,8M da riemettere con nuovo prezzo (richiami fermi da luglio).
- Finanziamenti in `LOANS`/`loans` mensili (k€: `sched`, `cap`, `int`, `res`) da piani di ammortamento BCC 1066083 e 1071107, Unicredit 2529480, Credem 8630473; BCC Sebino 8021/Finlombarda da bilancio; Unicredit 8823317 e Mini da scadenziario Verusca. Interessi a CE = somma `int`; debito residuo = somma `res`. 2026: rate 436,4k, interessi 19,7k, residuo 31/12 435,9k, **DSCR 1,04x** (2027 ~1,2x).
- Personale all-in lug 54,3k / ago 48,8k (modello 58k), affitti 8,2k, energia 7,4/9,0k, royalties trimestrali ~9-10k a ottobre.

## Aperto
- Valorizzare `shiftSupPct`: volumi acquisti per fornitore (registro acquisti) per pesare i RiBa senza +10.
- Mastrini/trimestrale metà ottobre: sostituire costi stimati lug-set.
- Conferma recupero credito IVA con Luca (Studio SGEA); acquisti settembre non registrati.
- Enextras FT108/FT117 (112,2k) e ordine 260143 (88,7k non spedito, chiedere a Giusi).
- Ritardi settembre: T.Erre programma 32,3k, Serotti 33,7k, Watts 18,9k.
- Classificazione IVA OMECA/Arkimat/locazione; storico ritiri vs mastrini; ripartizione T.Erre oltre tetti data.
- Piano ammortamento BCC Sebino 8021 (opzionale); magazzino al 30/06/2025.
- Argomm articolo 047002: cost breakdown per trattare il nuovo prezzo.
