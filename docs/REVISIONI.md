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

Stato della pagina di Alex dopo R019 (parametri della pagina, obiettivi 2.200k/2.100k, magazzino 153,4k): utile 2026 91,1k, 2027 79,8k; cassa dic-26 1.353k, dic-27 1.321k. Punti di ripristino: rami `ripristino-mattina-02-10-2026` (11e47db, prima della sessione Code), `ripristino-sera-02-10-2026` (520b60c). Stato del 01/10 sera (prima di tutte le modifiche del 02/10): commit 9d5382b — modello a percentuali: utile 2026 193,7k (con obiettivi di Alex) / 251,6k (parametri file), 2027 153,4k / 114,0k, cassa dic-26 1.654-1.714k, dic-27 1.599-1.631k.

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

Alex ritiene che il percorso di stasera (da 91k verso 70-75k) contenga errori di calcolo e prevede che a fine anno le stime di Claude si rivelino sbagliate. Va verificato voce per voce col bilancio al 30/09 PRIMA di toccare il modello.

## C. Come aggiungere una revisione
Aggiungere in fondo la riga con il numero successivo (R030…), nello stesso commit della modifica. Le modifiche ai calcoli richiedono comunque prima l'ok di Alex (regola CONGELATO in CLAUDE.md).
