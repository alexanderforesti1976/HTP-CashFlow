# HTP-CashFlow — risposta alle ISTRUZIONI_PER_CODE (02/10/2026)

Repo: alexanderforesti1976/HTP-CashFlow, branch `main`, ultimo commit `a41741d`.
Commit: `54f6638` (punto 1), `3165d0c` (punto 2), `5c687e1` (punto 3), `a41741d` (correzioni successive, vedi sezione 4). Aggiornato anche CLAUDE.md ("Stato" e "Aperto").
Test: ogni punto provato con il `params.json` reale (non i default) caricato in un browser headless; prima/dopo qui sotto. Non provato sulla pagina vera con le impostazioni salvate in Firebase (obiettivi 2.200k / 2.100k).

---

## Punto 1 — Scadenzario fornitori (`openPaySched`)

**Parser verificato sui totali del PDF** (scadenzario fornitori 01/01–31/12/2026):

| | Estratto | Stampato nel PDF |
|---|---|---|
| Dare | 949.004,13 | 949.004,13 |
| Avere | 1.061.303,72 | 1.061.303,72 |
| Saldo aperto | 112.299,59 (77 righe) | 112.299,59 |

Verificati anche i subtotali per fornitore (Hexpol 60.347,30 / 89.761,61 ecc.): coincidono. I pesi sono quindi ricalcolati sul parser corretto.

**Scadenze 2027.** L'esportazione si ferma al 31/12/2026. Confronto per numero di protocollo con il registro IVA acquisti: mancano 5 fatture di settembre per 19.608,58 €, tutte con scadenza 2027:
- Hexpol 000634 (7.463,08) e 000647 (8.360,08) = 15.823,16
- EU Silicones 000678 = 2.766,96
- L.G. Italia 000655 = 786,90
- Lav.El. 000668 = 231,56 (RiBa fine mese senza +10 con scadenza 31/12, slitta al 10/01: conferma la regola)
Messe al 10/01/2027.

**Data di pagamento.** Misurata sui pagamenti reali dello scadenzario (pagato − scadenza): RiBa −1,2 giorni (pagate a scadenza), bonifici +17 giorni (mediana 2). Usati questi valori al posto del +7 uguale per tutti. Le scadute vanno in ottobre.

| Mese | `openPaySched` prima | dopo |
|---|---|---|
| Ott 26 | 63,4k | 77,8k |
| Nov 26 | 23,9k | 24,2k |
| Dic 26 | 8,4k | 10,3k |
| Gen 27 | 19,8k | 19,6k |

Ottobre sale di 14,4k perché mancavano scaduti: giugno 6,7k, luglio 3,5k, agosto 5,7k, settembre 39,2k.

**Controllo per mese fattura** (registro IVA acquisti contro scadenzario):

| Mese fattura | Registro IVA (lordo) | Scadenzario (fatture) | Registro non in scadenzario | Differenza |
|---|---|---|---|---|
| Luglio | 94.988 | 95.010 | 0 | −22 |
| Agosto | 51.685 | 53.725 | 0 | −2.040 |
| Settembre | 54.410 | 33.971 | 19.609 | +830 |

Differenze residue: lug 22 €, ago 2,0k (lo scadenzario ha 2,0k in più; non verificato da cosa dipenda), set 0,8k.

**Scadenze di dicembre 2026** (aperte, 10.257 €):

| Fornitore | Fattura | Data fattura | Importo | Scadenza | Modalità |
|---|---|---|---|---|---|
| Hexpol | 4205/VEN | 31/08/2026 | 6.617,85 | 10/12/2026 | RiBa |
| PMG East | 2026000270 | 31/08/2026 | 3.357,90 | 10/12/2026 | Bonifico |
| Belometti | 2026-V0000 | 30/09/2026 | 137,25 | 10/12/2026 | RiBa |
| Lav.El. Gomma | V2602086 | 03/09/2026 | 144,57 | 31/12/2026 | RiBa |

Hexpol agosto: una sola fattura, 6.617,85 €, coincide col registro IVA (6.618). PMG S.p.A.: nessuna fattura ad agosto/settembre (ultima 30/07, 302 €).

**Pesi `payMatrix`** (fatture a credito da 01/04/2026, 39 fornitori, 175k): Hexpol 30%, FGR 13%, Selini 8%, PMG 8%, PMG East 6%, EU Silicones 5%, Sidera 4%… incluse le 5 fatture con scadenza 2027.

---

## Punto 2 — Conto economico 2026 = H1 reale + H2 previsto

Riclassifica H1 (da `H1_2026_REALE`): materie = MP + materiali + imballi + PF; lav. terzi; personale = salari + contributi + TFR + welfare; energia; affitti = solo affitti; provvigioni; royalties; altri = leasing, noleggi, manutenzioni, pubblicità, spese commerciali, consulenze, compenso amm., revisore, spese bancarie, altri G&A. H2 = parametri attuali × ricavi lug-dic (1.056,2k). Ammortamenti (110k), rimanenze (24,6k), TFM e imposte sull'anno intero. Interessi attivi = H1 reale + 5k; interessi passivi = H1 reale + piano H2.

| Voce (k€) | H1 reale | H2 previsto | Totale | Prima (% su tutto l'anno) |
|---|---|---|---|---|
| Ricavi | 1.248,7 | 1.056,2 | 2.304,9 | 2.304,9 |
| Var. rimanenze | | | 24,6 | 24,6 |
| Materie prime | 231,8 | 190,1 | 421,9 | 414,9 |
| Lavorazioni terzi | 49,8 | 42,2 | 92,0 | 92,2 |
| Personale | 336,8 | 348,0 | 684,8 | 696,0 |
| Energia | 48,0 | 40,1 | 88,2 | 87,6 |
| Affitti | 52,4 | 49,8 | 102,2 | 99,6 |
| Provvigioni | 34,9 | 29,6 | 64,5 | 64,5 |
| Royalties | 8,3 | 15,8 | 24,2 | 34,6 |
| Altri costi | 272,3 | 151,7 | 424,0 | 309,1 |
| **EBITDA** | | | **427,7** | 531,0 |
| Ammortamenti | | | 110,0 | 110,0 |
| EBIT | | | 317,7 | 421,0 |
| Interessi attivi | 8,0 | 5,0 | 13,0 | 10,0 |
| Interessi passivi | 12,8 | 8,6 | 21,4 | 19,7 |
| EBT | | | 309,4 | 411,3 |
| TFM | | | 61,9 | 82,3 |
| Imposte | | | 69,1 | 91,8 |
| **Utile netto** | | | **178,5** | **237,2** |

**Da guardare:** "Altri costi" H2 previsti 151,7k contro 272,3k di H1 reale. In H1 ci sono lo storno Terra Verde (41,5k) e la pubblicità (46,9k); anche togliendoli, H2 resta molto più basso. `otherFixedK` e `otherVarPct` sembrano sottostimati. Non toccati, perché le istruzioni dicevano "parametri attuali".

---

## Punto 3 — Imposte nel cash flow

Logica: acconti anno N = 100% imposte N−1, split 50/50 (`accontoSplit` 0,5, modificabile); giugno N+1 = saldo N + 1ª rata acconto N+1; saldo a credito compensato nel mese, residuo con la rata successiva.

Imposte 2026 (CE corretto) 69,1k; acconti 2026 su imposte 2025 (124k) = 62k + 62k; saldo 2026 = 69,1 − 124 = **−54,9k (credito)**.

| Mese | Cosa si paga | Prima | Ora |
|---|---|---|---|
| Giu 26 | 1ª rata acconto 2026 (50% di 124k) | in cassa ancorata | 62,0k |
| Nov 26 | 2ª rata acconto 2026 | 45,9k | 62,0k |
| Giu 27 | saldo 2026 (−54,9) + 1ª rata acconto 2027 (34,6) | 23,9k | 0 (credito residuo 20,4k) |
| Nov 27 | 2ª rata acconto 2027 (34,6) − credito residuo | 23,9k | 14,1k |

Il residuo del credito lo uso con la rata successiva: le istruzioni non dicevano cosa fare se il credito supera la rata del mese.

---

## Risultato complessivo sul cash flow

| | Prima | Ora |
|---|---|---|
| Cassa minima | 1.166k (nov-26) | **1.135k (nov-26)** |
| Saldo dic-26 | 1.211k | **1.178k** |
| Saldo dic-27 | 1.174k | **1.177k** |

Il peggioramento della minima viene da: scaduto di ottobre (+14,4k) e nov-26 imposte (+16,1k). Il Dicembre fornitori incide poco.

---

## Come ragionavo prima e chi ha ragione (richiesta di Alex)

**Come ragionavo prima:**
- Leggevo i PDF con regex veloci e non verificavo mai i totali con quelli stampati. Il parser attribuiva a Hexpol il pagamento di un altro fornitore (IAO) e saltava i numeri documento con spazi: circa 1,5% di errore sugli importi.
- Quando Alex diceva "Dicembre a 8 è impossibile" cambiavo il modello prima di verificare i dati: lag unico DPO 105, poi `payLag`, poi percentuale di slittamento, poi matrice per fornitore: quattro versioni in poche ore.
- Ho dato per non registrati gli acquisti di agosto e settembre, ma il registro IVA arriva al 30/09.
- Ho pubblicato per pochi minuti un errore di sintassi in `index.html` (corretto subito).

**Chi ha ragione:**
- **Io, sul Dicembre fornitori:** con il parser corretto è circa 10-11k, non 8,4k ma neanche "molto di più". Hexpol ad agosto ha fatturato solo 6.617,85 € (coincide col registro IVA), quindi non c'è altro da pagare a dicembre da quel fornitore. Dicembre resta basso per struttura: le fatture di ottobre a 60 giorni scadono il 31/12 e slittano al 10/01, quelle di settembre a 90+10 vanno a gennaio.
- **L'altra chat, sul resto:**
  - Il 8,4k poggiava su un estratto sbagliato; ora `openPaySched` è rigenerato (ottobre da 63,4k a 77,8k).
  - Il CE 2026 applicava le percentuali a tutto l'anno (utile 237k): con H1 reale è 178,5k.
  - Le imposte nel cash flow erano calcolate male: con acconti sull'anno prima c'è un credito di 54,9k e novembre 2026 costa 62k.

---

---

## Punto 4 — Correzioni successive (messaggio dell'altra chat, 4 punti)

1. **Royalties 2026** = 1,5% dei ricavi su tutto l'anno = 34,6k (prima 24,2k); l'H1 reale basso è timing.
2. **Personale H1 + ratei** non presenti nel bilancio provvisorio, stima esplicita **40,3k** (mostrata nel CE come "di cui ratei H1"):
   - TFR: salari H1 235,3k × 7,41% = 17,4k meno 5,1k già a bilancio = **12,3k**
   - 13ª maturata: `tredK`/2 = **19,0k**
   - Ferie maturate non godute: **9,0k** (`ferieH1K`) — È UNA MIA STIMA (circa 5 giorni a dipendente più oneri), non un dato: da confermare.
3. **`otherFixedK` 2026 = 25** (prima 20).
4. **Acconto novembre 2026** = stessa cifra dell'acconto di giugno versato. Nuovo campo in Parametri "Acconto imposte giu-26 versato (F24)" (`accontoGiu26`, in k€): 0 = non inserito, e finché è 0 uso la stima 62k (imposte 2025 × 50%). **Serve l'F24 di giugno 2026 (Luca / Verusca).**

| Voce (k€) | Dopo punto 2 | Dopo correzioni |
|---|---|---|
| Personale | 684,8 | 725,2 |
| Royalties | 24,2 | 34,6 |
| Altri costi | 424,0 | 454,0 |
| EBITDA | 427,7 | 347,0 |
| EBT | 309,4 | 228,7 |
| TFM | 61,9 | 45,7 |
| Imposte | 69,1 | 51,0 |
| **Utile netto** | 178,5 | **131,9** |

| Cash flow | Prima | Ora |
|---|---|---|
| Cassa minima | 1.135k (nov-26) | **1.123k (nov-26)** |
| Saldo dic-26 | 1.178k | **1.160k** |
| Saldo dic-27 | 1.177k | **1.180k** |

Effetto imposte: imposte 2026 51,0k, acconti 2026 (stima) 124k → credito di 73k: giugno e novembre 2027 a zero.

---

## Verifica: l'utile è NETTO? (richiesta di Alex)

Sì: l'"Utile netto" della pagina è dopo TFM amministratore e dopo IRES + IRAP. Catena completa (k€, `calcPL(2026)`):

| Passaggio | k€ |
|---|---|
| Ricavi netti | 2.304,9 |
| + variazione rimanenze | 24,6 |
| = Valore della produzione | 2.329,5 |
| − Materie prime 421,9 − Lavorazioni 92,0 − Personale 725,2 − Energia 88,2 − Affitti 102,2 − Provvigioni 64,5 − Royalties 34,6 − Altri 454,0 | −1.982,5 |
| **= EBITDA** | **347,0** |
| − Ammortamenti | −110,0 |
| = EBIT | 237,0 |
| + Interessi attivi 13,0 − Interessi passivi 21,4 | −8,3 |
| **= EBT (prima del TFM)** | **228,7** |
| − TFM amministratore (20% di EBT) | −45,7 |
| = Imponibile | 182,9 |
| − IRES 24% (43,9) − IRAP 3,9% (7,1) | −51,0 |
| **= UTILE NETTO** | **131,9** |

Controllo aritmetico: 228,7 − 45,7 − 51,0 = 131,9. Quadra.

**Limiti del calcolo (da conoscere):**
- IRAP è calcolata sulla stessa base dell'IRES (EBT − TFM) al 3,9%: è un'approssimazione, la base IRAP reale è diversa (costo del lavoro, interessi).
- Il TFM al 20% dell'EBT e le imposte sono calcolati sull'anno intero con le aliquote dei parametri, non dal bilancio.
- **Controllo di coerenza H1/H2 (da guardare):** il bilancio provvisorio H1 dà utile netto 41,5k. Se l'anno è 131,9k, H2 verrebbe ~90k, più dell'H1 con ricavi più bassi (H2 1.056k contro H1 1.249k). Nell'H1 pesano lo storno Terra Verde (41,5k) e la pubblicità (46,9k), ma resta il sospetto che i costi H2 siano ancora sottostimati (altri costi, personale). Con i ratei H1 aggiunti (40,3k) l'H1 reale scenderebbe a circa 10-20k di utile netto. Questa è una verifica di buon senso, non un calcolo certo.

---

## Aperto
- **F24 giugno 2026** (acconto imposte): oggi stima 62k (`accontoGiu26` = 0). Da Luca o Verusca.
- **`ferieH1K` 9k** è una stima: da confermare con il consulente del lavoro.
- **Coerenza H1/H2** dell'utile (vedi sopra): H2 sembra ottimistico; servono i mastrini/trimestrale di metà ottobre per verificare costi e personale.
- **Dicembre fornitori ≈ 11k** per struttura: confermare con l'altra chat cosa si aspetta e da quali fatture (le uniche aperte a dicembre: Hexpol 6.617,85, PMG East 3.357,90, Belometti 137,25, Lav.El. 144,57).
- Ad agosto lo scadenzario ha 2,0k in più del registro IVA acquisti: da capire.
- Plafond clienti: Lav.El. residuo 58,3k contro 70,4k ott-nov; Cavagna/OMECA 35,8k contro ~37,6k ott-dic; MCM 6,2k contro ordine dic 14,0k.
- Test fatto in headless con `params.json` reale, non sulla pagina con le impostazioni salvate (Firebase/localStorage). Se in pagina hai già modificato a mano un parametro (es. obiettivi 2.200k/2.100k), il valore salvato prevale sul file.
- Mastrini/trimestrale metà ottobre; credito IVA con Luca (SGEA); Enextras FT108/FT117 e ordine 260143.
