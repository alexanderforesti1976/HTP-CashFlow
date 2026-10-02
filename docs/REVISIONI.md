# REVISIONI — registro incrementale delle modifiche (voluto da Alex, 02/10/2026 sera)

**Regola:** ogni volta che si tocca un dato, un parametro, una formula o una conclusione già comunicata a Alex, si aggiunge qui una riga numerata in fondo (mai riscrivere o cancellare le precedenti). Per ogni voce: data/ora, tipo, cosa, prima → dopo, fonte, commit. Le affermazioni di Claude poi corrette o ritirate vanno registrate come tali. Leggere questo file all'inizio di ogni sessione e prima di ogni verifica.
Tipi: **PUBBLICATA** (su `main`), **ANALISI** (calcolata ma NON applicata al modello), **RITRATTATA** (affermazione di Claude poi corretta), **RIPRISTINO**.
Repo pubblico: niente nomi/importi di singoli clienti o fornitori, solo aggregati.

## A. Storico 02/10/2026 (ricostruito da git log; ordine cronologico)

| N. | Tipo | Cosa | Commit |
|---|---|---|---|
| R001 | PUBBLICATA | CLAUDE.md aggiunto al repo | 1847d2a |
| R002 | PUBBLICATA | Quota ricavi non confermata (programmi 2100 e righe 2099) separata nel cash flow; backlog rigenerato da ordini aperti 02/10 (ott-dic 530,8k, non confermato 26,4%); totale anno 2.304,9k, SFORATO segnalato | 95eff26, 17fb448, 243149c |
| R003 | PUBBLICATA poi corretta | Acquisti ago/set: prima assunti non registrati (ERRORE), poi `purchRegYM` dal registro IVA | f476718, fdea592 |
| R004 | PUBBLICATA poi sostituita | Slittamento scadenze 31/08→10/09 e 31/12→10/01: prima su incassi e fornitori (errore), poi solo fornitori RiBa senza +10; `shiftSupPct` 18%→16%→25% (base sbagliata) | 730adbc … b6c8b71 |
| R005 | PUBBLICATA | Pagamenti fornitori: `payMatrix` per fornitore al posto del lag unico DPO 105 | 53b3a8e |
| R006 | PUBBLICATA (errore sintassi 16:36, corretto 16:37) | Commento nel punto sbagliato in index.html | fdea592, d8d27a0 |
| R007 | PUBBLICATA | `openPaySched` rigenerato con parser verificato sui totali PDF (Dare 949.004,13 / Avere 1.061.303,72 / aperto 112.299,59); escluse RiBa/RID scadute ≤30/09 | 54f6638, 3625fff |
| R008 | PUBBLICATA poi ANNULLATA | Incassi con DSO "reale" da "Pagata il" (ERRORE: è la presentazione RiBa, non l'incasso; nessun anticipo bancario) | 7d2980f, revert 0b6f61a |
| R009 | PUBBLICATA | Incassi cliente per cliente: `recMatrix` da condizioni di pagamento e mix backlog | dcbf79c |
| R010 | PUBBLICATA | CE 2026 = H1 reale (`H1_2026_reale`) + H2 previsto (utile 178,5k contro 237,2k con le % su tutto l'anno) | 3165d0c |
| R011 | PUBBLICATA | Imposte nel cash flow: acconti 100% anno precedente (62k+62k), saldo, credito compensato | 5c687e1 |
| R012 | PUBBLICATA | Parametri 2027 allineati al ritmo 2026 (altri fissi 25k, personale 58k/mese, energia fissa 7,5k); `_forceKeys` | d30c865 |
| R013 | PUBBLICATA | Royalties 1,5% pagate trimestralmente nel cash flow; regola fissa in CLAUDE.md | 1985700 |
| R014 | PUBBLICATA | Acquisti settembre: consuntivo registrato 22,2k + proiezione del resto | b834da7 |
| R015 | PUBBLICATA | Ratei personale: attivati, disattivati, riattivati più volte (flip-flop); tredicesima spostata da novembre a dicembre nel cash flow | 250bf5b, 5a1b078, f495868, 05ce5a6 |
| R016 | PUBBLICATA | Personale 2026 col metodo di Alex (costo 2025 senza TFR e 13ª confrontato con H1 2026, rapporto 0,893, TFR e 13ª riproporzionati): 756,3k; TFR e 13ª in riga nel CE | da69721, 6328eef |
| R017 | PUBBLICATA | Rimanenze in valore assoluto al posto della variazione (nessun cambio di calcolo) | 837e14b |
| R018 | PUBBLICATA | Pulsanti +/- più piccoli su telefono; etichetta cassa 30/09/2026 | e07656a, d9479f3 |
| R019 | PUBBLICATA | CIG 2027 (`cigW27`, `cigH27`) tolta da `_forceKeys`: ora vale l'input della pagina (prima params.json la riportava a 0 operai / 50%). Test: personale 2027 756,3→700,1k, utile 2027 79,8→112,3k con 6 operai al 30% | 1044d5c |

Stato della pagina di Alex dopo R019 (parametri della pagina, obiettivi 2.200k/2.100k, magazzino 153,4k): utile 2026 91,1k, 2027 79,8k SENZA CIG 2027 (vedi R030: con la CIG di Alex sulla pagina 2027 = 112k); cassa dic-26 1.353k, dic-27 1.321k. Punti di ripristino: rami `ripristino-mattina-02-10-2026` (11e47db, prima della sessione Code), `ripristino-sera-02-10-2026` (520b60c). Stato del 01/10 sera (prima di tutte le modifiche del 02/10): commit 9d5382b — modello a percentuali: utile 2026 193,7k (con obiettivi di Alex) / 251,6k (parametri file), 2027 153,4k / 114,0k, cassa dic-26 1.654-1.714k, dic-27 1.599-1.631k.

## B. Verifiche dopo i mastrini (sera 02/10, `MASTRINI 2026.xlsx` da Alex, 622 pagine, 226 conti, registrazioni fino a settembre)
Il file xlsx NON è nel repo (dati aziendali); tenerlo in Drive `HTP-Dati`. Il connettore Drive in Code oggi non mostrava nessun file (cartella non trovata anche con ID); Gmail dava l'allegato solo come nome e dimensione.

| N. | Tipo | Cosa | Prima → dopo / evidenza |
|---|---|---|---|
| R020 | ANALISI (non applicata) | Interessi H1: provvisorio → mastrini. Interessi attivi c/c 2.078 → 3.821 (quelli del 30/06 registrati dopo la bozza); passivi 12.761 → 13.432; titoli 5.951 invariati. Saldo C) −4,7k → −3,7k | utile 2026 +0,6k. Resta da decidere con Alex |
| R021 | RITRATTATA | "Altri costi reali 45k/mese" (inclusi i 41,5k di storno Terra Verde, che va escluso dai confronti) | Reali senza storno: 37,3k/mese in H1, 33,9k lug-ago |
| R022 | RITRATTATA | Proposta B "altri fissi 25k→30k" (utile 2026 74,4k, 2027 45,2k): basata su media che spalmava costi irregolari | Scartata. Senza pubblicità/fiere (Alex: non si spende più) e con compenso amministratore + INPS già chiusi (19.420 + 4.536 = come 2025), reali ≈ 28,0k/mese contro 30,3k del modello. Nessuna modifica a 25k + 3% |
| R023 | ANALISI | Test lug-ago: costi reali 288,0k contro 275,4k nel modello (royalties escluse: il 3° trimestre non è registrato), cioè −12,6k EBITDA 2026; margine reale 17,5k contro 30,1k | Non applicata. Utile 2026 stimato circa 84k (stima Claude, TFM e imposte a spanne) |
| R024 | ANALISI | Imposte: modello deduce il TFM (`taxBase = ebt − tfm`, 27,9% = IRES 24% + IRAP 3,9%) → 22% del risultato. Bilancio 2025: utile 171.459, IRES 102.280, IRAP 21.969, anticipata 364 → imposte 124,6k = 42,1% del risultato dopo TFM; il TFM (74.018, = 20,0% del risultato prima del TFM) non è deducibile finché non pagato | Non applicata. Stima utile 2026 73-82k. Tocca anche la cassa (acconti 2027 = 100% imposte 2026). Resta da decidere con Alex |
| R025 | RITRATTATA | Confronto proporzioni TFR/13ª: rapporto r=0,893 usava come denominatore anche l'interinale 2025 (67,4k, oggi zero); tabella "solo salari" (80,4k) ignorava il 13/12: i salari 2025 contengono la 13ª pagata, quelli H1 2026 no | Metodo standard (TFR = retribuzione annua incl. 13ª /13,5 con rivalutazione del fondo; 13ª = 1 mensilità + contributi): rapporto 0,940 → TFR 40,1k totale (di cui 10,2k già nel costo base: quota previdenza complementare) + 13ª 52,2k; da aggiungere 82,1k contro 82,7k del modello: personale 2026 ≈ 756k invariato. Ferie/permessi non goduti: a zero nel modello, servono dati del consulente del lavoro. Nessuna 14ª nel CCNL gomma plastica (non è mai stata calcolata) |
| R026 | CONFERMATO | Dai mastrini: esistenze iniziali 168.359,33; nessuna rimanenza finale registrata (è un input manuale di Alex, non un dato); TFR registrato in H1 solo 5,1k (ratei non contabilizzati); royalties 8,3k in H1 + 9,7k a luglio; affitti 8,2k; personale lug 54,3k, ago 48,8k; settembre senza stipendi | — |
| R027 | RITRATTATA | "Magazzino finale del 30/09 nei Parametri" e "bilancio provvisorio al 30/06 contiene il magazzino": non verificabili. Il magazzino finale è un'ipotesi di Alex, il 168,4k è l'unico valore certo (31/12/2025) | — |
| R028 | RITRATTATA | "Il costo personale 2026 non conteneva TFR e 13ª nel modello del 01/10": conteneva un costo all-in 58k/mese (696k), che secondo le istruzioni iniziali le comprendeva. Non è stato verificato se il 58k le contenga davvero (lo sa Alex). 756,3k potrebbe contarle due volte in parte | Aperto |
| R029 | RITRATTATA | "Non scende a 40" / "si ferma a 70-75k": nessuna garanzia, sono stime Claude. Chiusura sicura = bilancio al 30/09 (metà ottobre) | — |

| R030 | RITRATTATA | Screenshot della pagina di Alex (22:14, tab Cash Flow, confronto 2024-2027): utile 2026 92k, 2027 112k; personale 2026 754k (CIG 1 operaio al 15%), 2027 700k (6 operai al 30%); EBITDA 2026 278k, 2027 295k; interessi passivi 2027 8k (da verificare sui piani: debito residuo 31/12/26 436k). Le cifre "utile 2027 79,8k" riportate come stato della pagina erano SENZA la CIG di Alex | Conferma che il fix R019 funziona sulla pagina (test headless 112,3k) |

| R031 | ANALISI (non applicata) | Verifica per competenza di "altri servizi" e "oneri diversi" (mastrini gen-ago 2026 contro bilancio 2025 per conto). Altri servizi 2025 222,5k contro 124,0k gen-ago 2026 (8/12 del 2025 = 148,3k; sotto: consulenze amministrative 21,8 contro 57,1, interinale 0 contro 23,5; sopra: assicurazioni 16,1 contro 17,9 già quasi tutta l'annualità, consulenze legali 7,1 contro 0,9). Oneri diversi 2025 108,9k includono multe e ammende 83,5k non ricorrenti (2026: 2,7k). Altri costi 2025 (536k) includono quindi 83,5k + pubblicità 67,8k non ricorrenti → circa 385k ricorrenti. Altri costi 2026 del modello senza storno: 412,5k; per competenza (gen-ago reali 291,8k + set-dic 80,6k se consulenze amministrative già chiuse, oppure 115,9k se arrivano al livello 2025) = 372-408k | Modello al livello alto o sopra di 5-40k: nessuna correzione al rialzo. Aperto: consulenze amministrative set-dic (frequenza di fatturazione, lo sa Alex) |

| R032 | CONFERMATO (Alex) | Oneri diversi: non si moltiplicano; multe e ammende (83,5k nel 2025, 2,7k gen-ago 2026) non esisteranno più. Nel modello nessuna riga dedicata: H1 reale una volta, H2 e 2027 dentro il fisso 25k + 3% | Nessuna modifica |

| R033 | ANALISI (non applicata) | Effetto dei punti trovati il 02/10 sera, test headless con parametri di Alex (rev26 2.200, rev27 2.100, CIG 2026 1 operaio 15%, CIG 2027 6 operai 30%, magazzino 153,4k). Base del test = screenshot pagina 22:14 (utile 2026 92,4 contro 92 visto, 2027 112,3 contro 112, EBITDA 278,6 / 295,0). **Altri costi 2026 per competenza** (`otherFixedK` 2026 da 25 a 24,2 oppure 18,3): altri 454,0 → 449,2 / 413,8; EBITDA 2026 278,6 → 283,4 / 318,8; utile 2026 92,4 → 95,2 / 115,6; 2027 invariato 112,3; cassa dic-26 1.354 → 1.357 / 1.379, dic-27 1.372 → 1.374 / 1.388 (il valore basso vale solo se le consulenze amministrative set-dic sono già chiuse). Altri punti: interessi H1 dai mastrini +0,6k; imposte con TFM non deducibile −9k/−19k (stima Claude); lug-ago reali su materie, energia, provvigioni, personale netto circa −2k. Somma: utile 2026 tra circa 74k e 105k contro 92,4k | Nessuna modifica pubblicata. Da decidere con Alex dopo il bilancio al 30/09 |

| R034 | RITRATTATA | Affermazione "il TFM non è deducibile finché non pagato" (R024, R033): regola fiscale NON verificata, presentata da Claude come fatto. Il TFM nel modello è il 20% dell'utile lordo prima del TFM (verificato sul 2025: 74.018 su 370.090 = 20,0%) ed è corretto. La stima imposte −9k/−19k su utile 2026 è ritirata | Aperto: perché le imposte 2025 sono 124,6k su 296k di utile (42,1%) mentre il modello dà circa 22%: da chiedere a Verusca/Luca (SGEA), non da dedurre. Nessuna modifica al modello |

| R035 | CONFERMATO (Alex) / RITRATTATA | Il TFM è DEDUCIBILE dalle imposte: il modello (`taxBase = ebt − tfm`) è corretto. Ritirato il punto imposte −9k/−19k (R024, R033, R034). Correzione di un errore di calcolo di Claude: tolta quella voce, la fascia utile 2026 è circa 93-114k (estremo basso: altri costi con fisso 24,2k +2,8, interessi H1 +0,6, lug-ago reali −2,3 = 93,5k; estremo alto: fisso 18,3k +23,2, +0,6, −2,3 = 113,9k; partenza 92,4k), NON 83-114k come scritto in chat | Nessuna modifica al modello. Resta aperto solo perché le imposte 2025 sono il 42,1% dell'utile contro circa 22% del modello (altri costi indeducibili? da chiedere a Verusca/Luca), senza stima di effetto |

| R036 | RITRATTATA | Il "42%" delle imposte 2025 non è un'aliquota. Aliquote del modello corrette: IRES 24%, IRAP 3,9% (Lombardia), verificate online; 27,9% sull'utile dopo TFM = 22,3% dell'utile lordo. Spiegazione del 2025: IRES 102.280 / 24% = imponibile 426k contro 296k di utile ante imposte; di +130k, 83,5k sono multe e ammende indeducibili (non ricorrenti, Alex: non esisteranno più) e 4,9k costi indeducibili. Residuo circa 40k altri indeducibili e base IRAP più larga (IRAP pagata 22,0k contro 11,5k col 3,9% sull'utile): non spiegato, nessuna stima | Nessuna modifica al modello. Da chiarire con Verusca/Luca col bilancio al 30/09 |

| R037 | DECISIONE (Alex) | Alex decide di ricostruire l'app da zero (il vecchio codice non si ripristina né si ripulisce). Creato `docs/SPECIFICA_RICOSTRUZIONE.md` con regole di Alex, dati reali aggregati (bilancio 2025, mastrini 2026), parametri da fornire ed errori da non ripetere; nessuna stima di Claude. Il vecchio codice e i rami di ripristino restano | Nessuna modifica al modello esistente |

| R038 | INFORMAZIONE (Alex) | Titoli e fondi (Cedola Long 400k, fondo BTP 150k, Onemarkets 40,8k) liquidabili in giornata; polizza circa 74,9k (conto 00033000) 4-5 giorni. Dove stanno nel bilancio 2025: 02021901 e 02021902 (depositi, disponibilità liquide), 01074008 (fondi comuni 41.800), 00033000. Il bilancio 2025 non ha anticipi su fatture (solo "Credem dopo incasso" 245.194,46 tra i crediti) | Cassa operativa 1.279,66k invariata; se contare i titoli come liquidi (1.870,46k, con la polizza circa 1.945k) lo decide Alex |

| R039 | CONFERMATO (Alex) | I 74.900 (conto 00033000) sono una polizza assicurativa, liquidabile in 4-5 giorni; il riscatto anticipato ha riduzioni (con favore) in funzione dei tempi, ma non è il nostro caso: la polizza resta investita | Nessuna modifica al modello; la polizza non entra nella cassa operativa |

| R040 | CONFERMATO (Alex) / CORRETTA | La polizza non entra MAI nella liquidità. Tolta dalla specifica la dicitura "con la polizza circa 1.945k" (scritta da Claude in R038 come possibilità) | Nessuna modifica al modello |

| R041 | ANALISI (non applicata) / CONFERMATO (Alex) | Norme OIC 10 e IAS 7 sulla liquidità (fonti: ecnews, Fondazione OIC, ifrscommunity, BDO). Depositi BCC senza penali e in giornata (Alex) = cassa per norma; fondi e polizza no. Cassa per norma 1.829,66k (se Onemarkets è nei 1.870,46k) contro 1.279,66k usata: +550k su tutti i saldi (cassa dic-26 da 1.354k a circa 1.900k) | `startCash` NON modificato; la definizione la decide Alex |

| R042 | DECISIONE (Alex) | Cassa di partenza: depositi inclusi (Cedola Long 400k e fondo BTP 150k sono cassa). Valore 1.829,66k se il fondo Onemarkets (40,8k) è già nei 1.870,46k, altrimenti 1.870,46k. Fondi comuni e polizza fuori dalla cassa | Registrata nella specifica per la ricostruzione. `startCash` del vecchio codice NON modificato (l'app sarà ricostruita); conferma sul fondo Onemarkets da avere |

| R043 | DECISIONE (Alex) | Fondo Onemarkets (40,8k) lasciato fuori dalla cassa "per il momento": cassa di partenza 30/09/2026 = 1.829,66k (depositi inclusi, fondo e polizza esclusi) | Solo nella specifica. `startCash` del vecchio codice non modificato |

| R044 | DECISIONE (Alex) / CORREGGE R043 | Cassa di partenza secondo la struttura del bilancio ("in funzione del bilancio"): fondo Onemarkets conto a sé (01074008), non nei conti bancari, quindi non si sottrae: **1.870,46k** (depositi BCC inclusi, fondo e polizza fuori), non 1.829,66k | Solo nella specifica; `startCash` del vecchio codice non modificato. Da verificare sul file "situazione banche" di ottobre |

| R045 | VERIFICATO | File "SITUAZIONE BANCHE 1-31 ottobre 2026" (Alex): saldi 30/09 Credem 463.730, BCC Sebino 43.390, Unicredit 242.160, BCC Brescia 1.121.180 = 1.870.460. Nel saldo BCC Brescia sono compresi fondo BTP 150.000 e Cedola Long 400.000; polizza Assicomo 75.000 annotata a parte; Onemarkets non compare. Conferma R044: cassa di partenza 1.870,46k, la sottrazione di 40,8k del vecchio CLAUDE.md non è supportata dal file. Piano di Alex per ottobre: entrate 587.030 (di cui 250.000 giroconti interni fra banche), uscite 463.885 (di cui 250.000 giroconti), saldo totale 31/10 = 1.993.605 | Solo documentazione |

Alex ritiene che il percorso di stasera (da 91k verso 70-75k) contenga errori di calcolo e prevede che a fine anno le stime di Claude si rivelino sbagliate. Va verificato voce per voce col bilancio al 30/09 PRIMA di toccare il modello.

## C. Come aggiungere una revisione
Aggiungere in fondo la riga con il numero successivo (R030…), nello stesso commit della modifica. Le modifiche ai calcoli richiedono comunque prima l'ok di Alex (regola CONGELATO in CLAUDE.md).
