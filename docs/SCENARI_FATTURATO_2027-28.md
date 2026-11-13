# Scenari di fatturato 2027-2028 (preparato il 13/11/2026, da valutare nella chat delle strategie)

**Scopo.** Alex (13/11) vuole parlare con Valentina (lunedì/martedì) con numeri davanti: cosa succede a utile, cassa e CIG se il fatturato 2027-28 è 2.000k, 1.600k o 1.400k, con le ore di CIG adeguate e con l'uscita di due dipendenti (non sostituiti). Test headless: NON modifica l'app. Ricalcolabile con `node tools/scenari_fatturato.js` (R243).

## Premesse (da rivedere)
- Parametri della pagina di Alex (screenshot 02/11 13:08, R221): CIG Q4-26 = 0, 2027 = 936/936/936/464 ore al mese, quota non confermato = 0. Ricavi 2027 = 2.000k è il piano; ricavi 2028 = stesso valore dello scenario.
- **Lavoro proporzionale ai ricavi:** a 2.000k il piano di Alex di 936 ore di CIG significa circa 1.639 ore lavorate al mese (19 persone x 135,5 ore lavorabili - 936). Con meno ricavi le ore lavorate calano in proporzione e la CIG sale (capacità - ore lavorate). Nota: nel 2026 i ricavi calano solo del 13% (2.000k contro 2.304k) mentre le ore lavorate del piano calano del 42%: se le 936 ore non sono quelle giuste, cambia tutta la scala.
- **Due uscite** (due dipendenti dello stampaggio, dimissioni annunciate 13/11): dal 01/01/2027, non sostituiti. Costo mensile 5.718 senza 13ª e TFR (prospetto paghe gen-lug), TFR del primo circa 10,5k in cassa (non incluso). 2027: 17 persone; 2028: 16 (come R174).
- **Valore di un'ora di CIG per l'azienda:** 18,04 euro risparmiati (19,14 costo ora lavorata - addizionale 9%): è il parametro che decide quanto "pesano" le teste (R241). Da verificare con lo studio paghe (costo reale di un'ora di CIG: addizionale, ratei, TFR).
- **Limiti di CIGO:** 52 settimane nel biennio mobile e un terzo delle ore lavorabili nel biennio mobile (circa 26.300 ore con 19 persone). Con "3 giorni su 5" una settimana in CIG conta 0,4 (ragguagliata, da confermare). Fonti: INPS (scheda CIGO), Assolombarda, d.lgs. 148/2015.
- Il fatturato di gennaio 2027 oggi è circa 130k (Alex), contro 184k del modello: possibile materiale già pronto (poca produzione). Non inserito.

## Risultati (euro; "due escono" = senza sostituti)
| Ricavi | Due | CIG al mese 2027 (gen-set / ott-dic) | CIG 2028 | Utile 2027 | Utile 2028 | Cassa dic-27 | Cassa dic-28 | Minimo cassa (mese) | Mesi dal 1/2027 al tetto di 26.300 ore |
|---|---|---|---|---|---|---|---|---|---|
| 2.000k | escono | 665 / 193 | 529 | 212.073 | 207.347 | 1.981.040 | 2.218.975 | 1.843.218 (ott-26) | oltre 36 |
| 1.600k | escono | 992 / 520 | 857 | 83.989 | 73.774 | 1.774.210 | 1.871.507 | 1.723.963 (mar-28) | 33 |
| 1.400k | escono | 1.156 / 684 | 1.021 | 19.947 | 6.987 | 1.670.795 | 1.679.111 | 1.589.479 (mar-28) | 27 |
| 2.000k | restano | 936 / 464 | 529 | 205.635 | 207.347 | 1.968.888 | 2.214.242 | 1.843.218 (ott-26) | oltre 36 |
| 1.600k | restano | 1.263 / 791 | 857 | 77.551 | 73.774 | 1.762.058 | 1.866.774 | 1.714.003 (mar-28) | 29 |
| 1.400k | restano | 1.427 / 955 | 1.021 | 13.510 | 6.987 | 1.658.643 | 1.669.152 | 1.579.519 (mar-28) | 24 |

**Se la CIG NON venisse adeguata** (resta 936/464 ore anche con meno ricavi), il 2027 sarebbe: 1.800k utile 118,7k; 1.600k utile 31,8k; 1.400k utile -75,0k; cassa dic-27 1.831k / 1.694k / 1.556k (ricavi 2027 con i due presenti, R-test del 13/11). Pareggio circa 1.550-1.600k.

## Cosa dicono
- La liquidità non è il problema: debiti verso banche a 92k a fine 2027 e 0 a fine 2028 (rate 2027 352k, 2028 93k), cassa sopra 1,56 milioni in tutti gli scenari.
- Il problema è la redditività: sotto 1.600k di ricavi l'utile è vicino a zero, e a 1.400k pari a zero anche con la CIG adeguata. Con la CIG adeguata il risultato regge solo finché la CIG è utilizzabile (limite di un terzo delle ore e 52 settimane): a 1.400k con i due presenti il tetto arriva dopo circa 24 mesi (fine 2028), poi servono provvedimenti sul personale.
- Le due uscite valgono poco sul conto (circa +6k di utile a 2.000k, circa +6k a 1.400k): la leva è il fatturato, non i costi.
- Un'ora di CIG si risparmia a 18,04 euro: se per l'azienda costasse di più (TFR, ratei), le teste in più/in meno peserebbero di più (R241).

## Dati contesto (Alex, 13/11)
Fatturato 2024 circa 4,5 milioni, 2026 circa 2,3 (2.362k nel modello); perso il progetto dei due articoli 117.010W e 117.011W (circa 800k l'anno: cliente nostro in lite col suo cliente, fornitura spostata); mercato debole; strategie commerciali fatte senza risultati; debiti bancari azzerati tra marzo e aprile 2028; ammortamenti in calo.

## Da rifare quando
- Fatture reali di ottobre e novembre e fatturato di gennaio 2027 (130k?).
- Ore di CIG realmente autorizzate (la procedura è in corso), costo reale di un'ora di CIG, date delle due uscite.
- Decisione sul temporaneo (R238).
