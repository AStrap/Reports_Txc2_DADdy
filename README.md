# Reports_Txc2_DADdy
  Python 3.9

## Requisiti

 - Installazione packages tramite pip: `pip install -r requirements.txt`
 - Microsoft Office Excel
 - Non obbligatorio: https://github.com/BlueHatbRit/mdpdf (impostare flag MD_PDF:False se non usato)

## Installazione

1. Download ed estrazione progetto: https://github.com/AStrap/Reports_Txc2_DADdy.git

2. Inserimento dei dati da elaborare (default: cartella "data" nella stessa posizione di "main.py")//
> Dati previsti:
> - Cartelle YY-MM: con i file csv riguardanti il mese (non obbligatorio tutte le giornate del mese)
> - "all_courses.csv" con ogni riga: id_course,nome_corso,docente,data_primo_appello,data_secondo_appello (docente=="--" se il corso e le sessioni da non considerare)
> - "all_lectures.csv" con ogni riga: id_lecture,id_course,timestamp_di_pubblicazione,nome_lezione,durata_normale_lezione,durata_turbo_lezione

3. Inserimento cartella output, se si mantiene la posizione di default

4. Creazione file config.py (seguire esempio) e modifica di parametri:
> - PATH_PRJ: path del progetto
> - DATE_RANGE_STUDY: periodo di studio dei dati modificabile in qualsiasi giornata
> - PATH_DATA: path della cartella "data" (default: stessa posizione main.py)
> - PATH_COURSES_DATA: path del file "all_courses.csv" (default: posizione in "data/")
> - PATH_LECTURES_DATA: path del file "all_lectures.csv" (default: posizione in "data/")
> - PATH_OUTPUT: path per la stampa dei risultati (default: stessa posizione main.py)
> - MD_PDF: flag che indica se eseguire la conversione dei file md
>
> parametri che comportano modifica dei grafici:
> - TIME_UNIT: unita di tempo di certi grafici a linea
> - N_LECTURES_PER_CHART: numero di lezioni considerati da grafici a barre orizzontali
> - DAY_PERIODS: periodi considerati di una giornato (non presente grafico)
> - USER_AGENTS: dispositivi considerati (non presente grafico)


## Limitazioni
Limitazione di visualizzazione grafici nei pdf, risolvibile con una gestione interativa come potrebbe essere un sito web.
