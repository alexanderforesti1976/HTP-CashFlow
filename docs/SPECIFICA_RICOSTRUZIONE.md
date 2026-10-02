# SPECIFICA PER LA RICOSTRUZIONE DELL'APP (02/10/2026)

Scopo: base di partenza per rifare da zero Cash Flow e Contabilità Industriale di High Tech Project S.r.l. **Contiene solo regole date da Alex e dati reali. Dove manca un dato è scritto "DA FORNIRE": non va riempito con stime.** Il codice esistente (`index.html`, `params.json`) e i rami `ripristino-mattina-02-10-2026`, `ripristino-sera-02-10-2026` restano su GitHub e non vanno cancellati. Registro di tutte le modifiche e delle affermazioni ritrattate: `docs/REVISIONI.md`. Repo pubblico: niente dati di singoli clienti/fornitori.

## 1. Principi di lavoro (Alex)
1. Le stime seguono le regole di Alex, mai quelle di Claude. Nessuna formula, percentuale o parametro cambia senza ok esplicito, con prima/dopo (utile e cassa).
2. Un numero è "della pagina di Alex" solo da un suo screenshot; altrimenti è "test" con i parametri usati.
3. Ogni modifica a dati/formule/conclusioni si registra (REVISIONI).
4. Nessuna garanzia sui risultati finché non c'è il bilancio al 30/09 (metà ottobre, Verusca).
5. Mai inventare menu o opzioni dell'interfaccia. Italiano, tecnico, breve, un passo alla volta.

## 2. Struttura richiesta
- Un'unica pagina (GitHub Pages) con due tab: Cash Flow | Contabilità Industriale. Stato condiviso in memoria; parametri persistiti (sync Firebase `htp-tools`, nodi `htp_cashflow`, `htp_contabilita`).
- CE per anno (2024, 2025 consuntivo; 2026, 2027 previsione) con rimanenze in VALORE ASSOLUTO (finali e iniziali), non in variazione. Pulsanti dei parametri leggibili su telefono, sola lettura per Valentina (`?mode=view`).
- Obiettivo ricavi (2.200k nella pagina di Alex, 2.250k nel file): consuntivo + ordini NON si scalano; se superano l'obiettivo si segnala "SFORATO".

## 3. Regole contabili e di cassa date da Alex
- **Royalties:** 1,5% del fatturato (1% + 0,5%), maturate e PAGATE TRIMESTRALMENTE (un pagamento per trimestre = 1,5% dei ricavi dei 3 mesi, nel mese successivo; gen/apr/lug/ott). CE: 1,5% su tutto l'anno; il 2° trimestre si registra a luglio.
- **TFM amministratore:** 20% dell'utile lordo prima del TFM (2025: 74.018 su 370.090 = 20,0%). Deducibile dalle imposte (Alex). Non è cassa mensile.
- **Imposte:** IRES 24% sull'IMPONIBILE IRES e IRAP 3,9% (Lombardia) sull'IMPONIBILE IRAP: due basi diverse, mai una percentuale media o una base unica. Nel 2025 (bilancio): imponibile IRES circa 426k (102.280 / 24%) e imponibile IRAP circa 563k (21.969 / 3,9%), contro 296k di utile ante imposte; la differenza viene da variazioni fiscali e, per l'IRAP, dalla base che comprende il costo del lavoro. **Metodo (norma):** IRES = (utile ante imposte ± variazioni TUIR) × 24%. IRAP (da bilancio) = (A − B) escludendo B.9 personale, B.10 c-d, B.12, B.13, meno le deduzioni sul costo del lavoro a tempo indeterminato (non verificate), × 3,9%. Stima 2025: A − B senza TFM circa 364k contro imponibile IRAP circa 563k (circa 199k di personale non dedotto, non spiegato per intero); IRES: utile ante imposte 296k, variazioni +130k (di cui multe 83,5k; senza multe indeducibili ricorrenti circa 46k, DA CONFERMARE). Cifre esatte di variazioni e deduzioni: dichiarazione dei redditi 2025 (quadri RF e IC), DA FORNIRE. Il TFM è deducibile (Alex). Cassa: acconti dell'anno N = 100% delle imposte N−1 in due rate (giugno e novembre); giugno N+1 = saldo N + 1ª rata acconto N+1; saldo a credito compensato nel mese, residuo con la rata successiva. Acconto di giugno 2026 reale (F24): DA FORNIRE.
- **Acconti e saldi (norma, verificata online):** acconto IRES e IRAP = 100% dell'imposta dell'anno precedente, in due rate (30/06 o 30/07 con maggiorazione, e 30/11). **HTP NON è soggetto ISA (Alex): per legge 40% e 60%** (2026: prima rata 49.700, seconda 74.549 = 124.249). ATTENZIONE: i versamenti reali tornano meglio con 50/50 (IRAP 1ª rata 10.984,50 = 50% esatto di 21.969; ottobre ancora 10,6k di rate acconti): DA CHIARIRE con Verusca. Si può rateizzare in rate mensili solo saldo e prima rata di acconto; la seconda rata (30/11) si paga per intero. Se 50/50: IRES 51.140 + 51.140, IRAP 10.984,50 + 10.984,50; se 40/60: prima rata 49.700, seconda 74.549. Versamenti reali (mastrini): 20/07 saldo IRES 2025 20.987, acconto IRES 1ª rata in rate (15.506,88 il 20/07, 10.506,88 il 20/08, 10.506,88 il 16/09; ottobre circa 10,6k; resto a novembre), acconto IRAP 1ª rata 10.984,50 il 20/07 con credito IRAP 15.984,50 compensato. Saldo dell'anno N a giugno/luglio N+1, con compensazione dei crediti.
- **Debiti per rateizzazione di accertamenti e INAIL (dal bilancio 2025):** atti di adesione 66.240,31 in 7 rate trimestrali da 9.462,94 (marzo, giugno, settembre, dicembre 2026; marzo, giugno, settembre 2027), più piccoli interessi; residuo 48.686,68 al 30/09/2026 (rata di settembre non so se già pagata). INAIL 22.488,43 in 12 rate mensili da circa 1.874 (giugno 2026 - maggio 2027); residuo 14.992,51 al 30/09 (8 rate). Nel vecchio modello assenti.
- **Personale:** TFR e 13ª vanno calcolati per competenza. Metodo di Alex: costo 2025 senza TFR e 13ª confrontato col costo H1 2026 registrato (che non li contiene), proporzione riportata su tutto l'anno; vedi R025 per i difetti trovati (interinale nel denominatore, 13/12 sui salari). La 13ª si paga a DICEMBRE. NON esiste la 14ª (CCNL gomma plastica). TFR = retribuzione annua incl. 13ª / 13,5 più rivalutazione (da conto 6041200 e quota previdenza complementare 6041201). Ferie e permessi non goduti: solo la variazione del debito, DA FORNIRE (consulente del lavoro). CIG = lavoratori / 20 × costo × % ore × 80%; la CIG 2026 e 2027 sono input di Alex e prevalgono sempre sul file. Costo all-in 58k/mese: DA CONFERMARE se comprende TFR e 13ª.
- **Rimanenze (Alex, 02/10 sera):** le giacenze le valorizza Alex a mano e le inserisce in VALORE ASSOLUTO (input manuale, non un dato ricavabile). Il metodo di valorizzazione fino al 31/12/2025 era uno, oggi è un altro e Alex sta ancora scegliendo il metodo che si avvicini a quello usato prima a mano: i valori sono INDICATIVI e possono cambiare leggermente, non stravolgersi. Quindi i confronti di utile che dipendono dal magazzino sono indicativi. Nel vecchio modello 10k di magazzino finale spostano l'utile netto di circa 5,7k. Iniziali 2026 = 168.359,33 (certo, bilancio 2025, metodo vecchio). Le finali sono un'IPOTESI MANUALE di Alex a fine anno (+/− rispetto alle iniziali), non un dato; iniziali 2027 = finali 2026.
- **Storno Terra Verde:** conto 7011300 "Variazione ricavi per resi e premi" 41.502,04 (storno con rifatturazione a ricavo): contare UNA volta, ed escluderlo dai confronti sui costi.
- **Incassi:** NESSUN anticipo bancario sulle RiBa (da 25 anni). Il "Pagata il" è la presentazione, non l'incasso. Incasso = scadenza per condizioni di pagamento cliente per cliente (RiBa fine mese, TT, prepagati).
- **Slittamento scadenze:** solo RiBa fine mese SENZA +10: 31/08→10/09 e 31/12→10/01; mai sui bonifici; verso i clienti nessuno slittamento (i clienti non hanno +10); i fornitori principali con +10 e quelli senza (RiBa fine mese) sono nel file condizioni di pagamento.
- **Pagamenti fornitori:** per scadenza reale (scadenzari Pegaso, parser verificato sui totali PDF) più acquisti previsti con le condizioni per fornitore.
- **IVA:** per aliquote e regimi reali (22%, 10%, non imponibile / dichiarazione d'intento / plafond), non medie; credito IVA recuperato con la dichiarazione annuale (aprile 2027). Residui plafond clienti: DA FORNIRE.
- **Assicurazioni:** non vanno moltiplicate. Oneri diversi non si moltiplicano; le multe e ammende (83,5k nel 2025) non esisteranno più. Pubblicità/fiere: non si spende più.
- **Ordini Pegaso:** consegna 31/12/2099 = in attesa conto lavoro (vale la data richiesta); 31/12/2100 = programma (ripartire sullo storico dei ritiri). Mai sommare i non confermati alle consegne confermate; mostrarli a parte.
- **Cassa operativa 30/09/2026 = 1.279,66k** (4 c/c 1.870,46k − titoli e fondi 590,8k: Cedola Long 400, fondo BTP 150, Onemarkets 40,8); la proiezione parte da ottobre. In bilancio 2025 questi importi sono: depositi BCC Brescia 02021901 (400.000,00) e 02021902 (148.650,62) tra le disponibilità liquide, fondi comuni 01074008 (41.800,00) tra le attività finanziarie.
- **Liquidità (Alex, 02/10):** Cedola Long, fondo BTP e Onemarkets sono liquidabili IN GIORNATA; la polizza assicurativa (74.900, conto 00033000 "Altri titoli", Assicomo 75k nel CLAUDE.md) in 4-5 giorni; il riscatto anticipato comporta riduzioni (con condizioni favorevoli) in funzione dei tempi, ma NON è il nostro caso: la polizza resta investita e non entra nella cassa operativa. Se contati come liquidi: liquidità disponibile 1.870,46k. La polizza NON entra mai nella liquidità (Alex). Se la cassa di partenza debba restare 1.279,66k o essere questa: DECISIONE DI ALEX, non modificata.
- **Norme (OIC 10, IAS 7):** sono cassa i depositi bancari prelevabili subito senza penalità e senza rischio di valore; non lo sono fondi comuni (rischio di valore) e polizze (penalità di riscatto). Alex conferma che i depositi BCC (Cedola Long, fondo BTP) sono senza penali e in giornata: per norma sono CASSA. Cassa secondo la norma = 1.870,46k − fondo Onemarkets 40,8k = 1.829,66k (solo se il fondo è compreso nei 1.870,46k: DA CONFERMARE), contro la cassa operativa 1.279,66k usata finora: +550k su tutti i saldi. **DECISIONE DI ALEX (02/10 sera): depositi INCLUSI nella cassa.** Fondo Onemarkets (40,8k): FUORI dalla cassa "per il momento" (Alex), e secondo la struttura del bilancio (Alex: "in funzione del bilancio") è un conto a sé (01074008), separato dai conti bancari: NON è nei 1.870,46k e NON si sottrae. **Cassa di partenza 30/09/2026 = 1.870,46k** (depositi BCC inclusi; fondo e polizza fuori). Il vecchio CLAUDE.md sottraeva 40,8k: criterio superato. **Verificato (file "SITUAZIONE BANCHE 1-31 ottobre 2026", saldi al 30/09/2026):** Credem 463.730 + BCC Sebino 43.390 + Unicredit 242.160 + BCC Brescia 1.121.180 = 1.870.460. Nelle note del saldo BCC Brescia sono "compresi nel saldo iniziale" il fondo BTP (150.000, c/deposito) e la Cedola Long (400.000, 3% semestrale, scad. 03/27); la polizza Assicomo (75.000, 03/25-03/55) è annotata senza dicitura "compreso" e il bilancio la tiene a parte (00033000). Il fondo Onemarkets NON compare nel file: non è in nessun saldo, quindi non si sottrae. Cassa di partenza = 1.870.460 (Alex 02/10).
- **Ciclo di chiusura:** costi registrati = consuntivo; costi non ancora registrati = proiezione in proporzione ai ricavi del mese, finché non arrivano i dati veri. Settembre provvisorio (fatture non ancora allo SDI, acquisti incompleti).

## 4. Dati reali (aggregati, k€)

**CE 2025 (bilancio):** ricavi 3.060; materie 642; lavorazioni terzi 144; personale 847,2 (salari 542,3; interinale 67,4; contributi 165,8; INAIL 13,8; welfare 11,7; TFR 37,1 + 5,6; sanitaria 3,5); energia 102; affitti 97; provvigioni 68; royalties 38,5; altri costi 536 (di cui pubblicità 67,8 e multe e ammende 83,5, non ricorrenti); ammortamenti 124; interessi attivi 36,2; interessi passivi 30,1; TFM 74,0; utile prima delle imposte 296,1; IRES 102,3; IRAP 22,0; IRES anticipata 0,4; utile 171,5. Rimanenze: iniziali 265, finali 168,4.

**Mastrini 2026 (xlsx di Alex, non nel repo), classi di costo, k€:**

| | gen-giu | luglio | agosto | settembre (incompleto) |
|---|---|---|---|---|
| Ricavi (vendite + stampi + diversi) | 1.248,7 | 213,8 | 91,8 | 0 (provvisorio 220) |
| Materie (acquisti) | 237,2 | 33,4 | 27,9 | 25,2 |
| Lavorazioni terzi | 49,8 | 7,3 | 4,0 | 3,0 |
| Energia | 48,0 | 7,4 | 9,0 | 5,4 |
| Provvigioni + ENASARCO | 35,3 | 8,5 | 3,3 | 10,1 |
| Royalties | 8,3 | 9,7 (2° trim.) | 0 | 0 |
| Affitti | 52,4 | 8,2 | 8,2 | 8,2 |
| Personale (senza TFR/13ª) | 336,8 | 54,3 | 48,8 | 0 (non registrato) |
| Altri costi (senza storno) | 224,0 | 45,2 | 22,6 | 9,8 |
| Interessi passivi | 13,4 | 1,0 | 0,8 | 0,1 |

Altri costi: ricorrenti 16,4k al mese (voci presenti in almeno 6 mesi su 8); irregolari gen-ago 157,1k (di cui pubblicità 55,9, consulenze amministrative 21,8, compenso amministratore 19,4 e INPS 4,5 già chiusi per l'anno). Interessi H1 reali: attivi c/c 3,8 (non 2,1 del provvisorio), titoli 6,0, passivi 13,4.
Rimanenze finali 2026: nessuna registrata. TFM e ammortamenti: non registrati (stime).

## 4 bis. La bozza al 30/06 va INTEGRATA (Alex, 02/10 sera): scritture di assestamento e competenza
La bozza al 30/06/2026 (13/07) è solo contabilità registrata: non comprende rimanenze finali, ratei/risconti, TFR, 13ª, TFM, ferie, ammortamenti, imposte di competenza. Per il CE di competenza si aggiungono (metodo; nessuna stima di Claude):
- **Rimanenze finali al 30/06:** DA FORNIRE (la bozza ha solo le esistenze iniziali 168.359,33 spesate: per questo l'utile 41.535,12 non è il risultato del semestre).
- **TFR:** retribuzione utile (13ª compresa) / 13,5 più rivalutazione del fondo; già registrati 1.563 (conto 6041200) + 3.537 (previdenza complementare).
- **13ª:** 6/12 di una mensilità più contributi sul periodo; paga a dicembre; niente 14ª.
- **TFM:** 20% dell'utile lordo prima del TFM (deducibile).
- **Ferie e permessi non goduti:** variazione del debito; DA FORNIRE (consulente del lavoro).
- **Ammortamenti:** non registrati; DA FORNIRE (piano).
- **Royalties 2° trimestre:** 1,5% dei ricavi aprile-giugno, registrate a luglio (9,7k nei mastrini) → rateo H1.
- **Costi annuali o pluriennali anticipati** (assicurazioni, canoni software, tassa di circolazione, canoni di manutenzione): risconti attivi per la parte di competenza dopo il 30/06; servono inizio e fine di ogni polizza/contratto: DA FORNIRE.
- **Ratei sugli interessi dei finanziamenti** non ancora scaduti: dai piani di ammortamento.
- **Compenso amministratore:** due rate semestrali (19.420 l'anno), da ripartire per competenza.
- **Imposte di competenza:** IRES e IRAP su basi separate, con variazioni fiscali (DA FORNIRE, Verusca/Luca).
Le voci già inserite in bozza di cui si può dedurre la quota di competenza (annuali e periodiche) vanno ripartite nel tempo, non moltiplicate né spalmate come mensili.

## 4 ter. Impostazione del ricalcolo (Alex, 02/10 sera)
- **Tutto si riproporziona al 31/12/2026**: dalla bozza/mastrini reali più le integrazioni di competenza (sezione 4 bis) si arriva al CE annuale.
- **Gli UNICI input modificabili dopo il ricalcolo sono due:** (1) il costo del personale con la CIG (lavoratori e % ore); (2) la valorizzazione del magazzino (rimanenze finali). **Non c'è altro.** Tutto il resto deriva da dati reali e da regole fisse (royalties, TFM, imposte, TFR/13ª, ratei, scadenze), non da manopole liberate: niente percentuali di costo da regolare a mano.
- **Flussi di dati che alimentano il modello (non sono manopole, si aggiornano quando arrivano dati nuovi):** ordini aperti Pegaso con le previsioni (consegna 31/12/2099 = in attesa conto lavoro, vale la data richiesta; 31/12/2100 = programma, data richiesta = data massima ritiro, ripartito sullo storico dei ritiri; i non confermati sempre mostrati a parte), scadenzari clienti e fornitori, condizioni di pagamento cliente per cliente e fornitore per fornitore, registri IVA, plafond. Tutti ricevuti il 02/10/2026 (vedi `docs/DATI_RICEVUTI.md`). Il modello deve essere preciso sui dati e dichiarare dove entrano previsioni (quota non confermata, mesi senza ordini, settembre provvisorio).
- Implicazione per la costruzione: i parametri-percentuale del vecchio modello (materie %, altri fissi, ecc.) non sono input liberi; dove servono una proiezione si ricavano dai dati reali del periodo e dalle regole elencate.

## 5. Parametri da chiedere ad Alex prima di costruire
Obiettivi ricavi 2026/2027; rimanenze finali ipotizzate; CIG 2026/2027; acconto IRES giugno 2026 (F24); frequenza di fatturazione delle consulenze amministrative (set-dic); se il 58k/mese comprende TFR e 13ª; ferie/permessi non goduti; piani di ammortamento aggiornati dei finanziamenti (interessi H2 2026 e 2027); plafond clienti residui; fatture di settembre mancanti.

## 6. Errori da non ripetere (dal registro)
Usare "Pagata il" come incasso; ripetere un pagamento (RiBa) già nella cassa bancaria; trattare costi annuali o trimestrali come mensili; contare lo storno Terra Verde due volte; presentare un test come stato della pagina; confrontare salari senza la 13ª con salari con la 13ª; mettere l'interinale nel denominatore dei ratei; stimare senza dire che è una stima; cambiare un calcolo senza prima/dopo approvato; regex sui PDF senza verifica dei totali.

## 7. Fonti
Bilancio 2025 PDF; mastrini 2026 (xlsx, estratti 02/10 16:02); registri IVA 2026; scadenzari Pegaso clienti/fornitori; condizioni di pagamento (xlsx); ordini aperti Pegaso 02/10; situazione banche; piani di ammortamento finanziamenti; bilancio provvisorio 30/06; bilancio al 30/09 (metà ottobre, DA RICEVERE).
