# Procedura di aggiornamento dati (per ogni sessione Claude)

Fonte documenti: cartella **Google Drive "HTP-Dati"** (connettore Google Drive di claude.ai; se non è disponibile in sessione, chiedere ad Alex di collegarlo su https://claude.ai/customize/connectors e aprire una nuova sessione). Il repo è PUBBLICO: non committare mai documenti (PDF/Excel con clienti, fornitori, importi); qui solo codice.

## File attesi in HTP-Dati (nomi indicativi; prendere il più recente per data)
- `SCADENZARIO_FORNITORI...pdf`, `SCADENZARIO_CLIENTI...pdf` (Pegaso, per scadenza)
- `REGISTRI_IVA_ACQUISTI...pdf`, `REGISTRI_IVA_VENDITE...pdf`, `UTILIZZO_PLAFOND_*.pdf`
- `OrdiniVenditaAperti*.pdf` (backlog)
- `Condizioni_pagamento_clienti_fornitori*.xlsx` (anagrafica condizioni)
- bilancio/situazione contabile al 30/09 (atteso verso il 15/10), mastrini, situazione banche (Verusca)

## Passi
1. Scaricare i file, `pdftotext -layout file.pdf file.txt`.
2. Scadenzari: `python3 tools/parse_pegaso.py fornitori|clienti file.txt out.json`. **Verificare che Dare/Avere/saldo coincidano con i totali stampati nel PDF (ultime righe)**, altrimenti fermarsi e chiedere l'Excel.
3. Rigenerare in `params.json` (e nei default di `index.html`): `openPaySched`, `openRecSched`, `payMatrix`, `recMatrix`, `OBACKLOG`/`OREV`/`nc`/`ORDCRIT`, `purchPartial`, `H1_2026_reale`... come descritto in CLAUDE.md.
4. Testare con il `params.json` reale (browser headless con stub Firebase), confrontare prima/dopo, aggiornare CLAUDE.md ("Stato" e "Aperto"), commit + push su `main`.

## Regole che hanno causato errori (non ripeterle)
- RiBa clienti: NESSUN anticipo bancario; il "Pagata il" è la presentazione in banca, non l'incasso: la cassa arriva alla scadenza.
- Voci aperte in Pegaso con scadenza ≤ data cassa che sono RiBa/RID fornitori sono già addebitate dalla banca: non contarle di nuovo.
- Royalties: 1,5% del fatturato, maturate e pagate trimestralmente.
- Il costo all-in del personale contiene già TFR, 13ª, TFM: non aggiungere ratei.
- Costi: consuntivo registrato + proiezione in proporzione ai ricavi solo per quello che manca.
