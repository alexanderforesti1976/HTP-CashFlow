# DATI RICEVUTI DA ALEX E GIÀ VERIFICATI (memoria permanente, 02/10/2026)

**Regola (Alex):** questi documenti sono già stati allegati e letti. NON chiederli di nuovo: usare i dati qui sotto. I PDF/xlsx originali NON sono nel repo (repo pubblico, dati aziendali) e le sessioni cloud non li conservano: se serve rileggerne uno, dirlo e chiedere solo quello. Il connettore Google Drive in Code oggi non mostra i file di Alex.

## 1. Bilancio provvisorio al 30/06/2026 — "HTP - BILANCIO 30-06-26 - BOZZA 13-07-26" (5 pagine, stampato 13/07/2026 15:19) — GIÀ RICONCILIATO (R058)
- CE: totale costi 1.215.491,60 (di cui esistenze iniziali 168.359,33 e storno 41.502,04), totale ricavi 1.257.026,72, **utile 41.535,12** (non è l'utile del semestre: esistenze iniziali spesate senza rimanenze finali).
- `H1_2026_reale` in params.json = questa bozza **al centesimo** (costi operativi 1.047.132,27; ricavi 1.257.026,72).
- Voci principali H1 (k€): salari 235,3; contributi 72,4 + INAIL 12,6; welfare 9,8; TFR 1,6 + 3,5; energia 44,9 + riscaldamento 2,1 + acqua 1,0; lavorazioni terzi 49,8; materie prime 195,6; pubblicità e fiere 46,9; consulenze amministrative 21,8; affitti 52,4; royalties 8,3; provvigioni 32,4 + ENASARCO 2,5; interessi passivi 12,8; ricavi da titoli 5,95; interessi attivi 2,08.
- SP 30/06: totale attivo 5.170.399,40; banche Credem 544.227, BCC Brescia 534.276, Unicredit 370.803, BCC Sebino 27.671; depositi BCC Brescia 400.000 (Cedola Long) e 147.911,75 (fondo BTP); fondi comuni 40.400 (Onemarkets, 40,8k al 30/09); polizza 74.900 (conto 00033000, fuori dalla liquidità); crediti clienti 343.842 nazionali + 78.919 esteri; Credem dopo incasso 247.105; credito IRAP 18.018; debito IRES 2025 20.987; IVA a debito 19.746; fondo TFR 180.155; fondo TFM 406.221; finanziamenti 30.000 + 20.000 (BCC Sebino/Finlombarda), 21.716 (BCC Brescia 1066083), 123.890 (1071107), 263.553 (Unicredit 2529480), 177.910 (Credem 8630473); rateizzazione accertamenti 48.686,68; rateizzazione INAIL 18.740,47.
- Gli acconti 2026 NON sono nella bozza (F24 del 20/07).

## 2. Bilancio 2025 (31/12/2025, ufficiale) — vedi `docs/SPECIFICA_RICOSTRUZIONE.md` §4
Utile 171.458,79; imposte 124.613 (IRES 102.280, IRAP 21.969, anticipata 364); TFM 74.018; personale 847,2k; rimanenze finali 168.359,33; depositi 400.000 e 148.650,62; fondi comuni 41.800; polizza 74.900; rateizzazione accertamenti 66.240,31 (7 rate trimestrali da 9.462,94, fine 09/2027); rateizzazione INAIL 22.488,43.

## 3. Mastrini 2026 (xlsx, estratti 02/10 16:02; 622 pagine, 226 conti; gen-ago completi, settembre incompleto)
Riepilogo per classi in `docs/SPECIFICA_RICOSTRUZIONE.md` §4. Acconti e saldi 2026 reali: R048. INAIL: rata 1.873,98 al mese (29/05, 30/06, 29/07, 28/08).

## 4. Situazione banche 1-31 ottobre 2026 (previsione di Verusca)
Saldi 30/09: Credem 463.730, BCC Sebino 43.390, Unicredit 242.160, BCC Brescia 1.121.180 (compresi fondo BTP 150.000 e Cedola Long 400.000) = **1.870.460** (cassa di partenza decisa da Alex). Previsione ottobre di Verusca: R046/R047.

## 5. Altri file ricevuti il 02/10/2026
Scadenzari clienti e fornitori 2026 (Pegaso), registri IVA vendite e acquisti 2026, utilizzo plafond clienti e fornitori, condizioni di pagamento clienti/fornitori (xlsx), ordini aperti Pegaso (stampa 02/10 17:50), riepilogo sessione e istruzioni per Code (md). Dati già in `params.json` e `CLAUDE.md`.
