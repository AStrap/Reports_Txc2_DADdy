# Reports_Txc2_DADdy
  Windows10 - (testato in)Python 3.9
  
  Ubuntu20.04 (git checkout linux_version) - (testato in)Python 3.9
  
  Versione excel - https://github.com/AStrap/Reports_Txc2_DADdy/tree/a97c4ffb51211d0ad905433e0b6ab6894c5400ba
 
## Requisiti

 - Installazione packages tramite pip: `pip install -r requirements.txt`
 - Non obbligatorio: installazione https://github.com/BlueHatbRit/mdpdf tramite node - npm (impostare flag MD_PDF:False nel file config.py, se non usato)

## Installazione

1. Download ed estrazione progetto: https://github.com/AStrap/Reports_Txc2_DADdy.git

2. Inserimento dei dati da elaborare (default: cartella "data" nella stessa posizione di "main.py")<br/>
> Dati previsti:
> - Cartelle YY-MM: con i file json riguardanti il mese
> - "all_courses.csv" con ogni riga: `id_course,nome_corso,docente,data_primo_appello,data_secondo_appello` (docente=="--" se è un corso di test), è possibile decidere che corsi ignorare inserendo `#,` all'inizio della riga corripondente dei corsi, attenzione la prima riga dev'essere l'intestazione "courseId,title,professor,firstExamsSessions,secondExamsSession".
> - "all_lectures.csv" con ogni riga: `id_lecture,id_course,timestamp_di_pubblicazione,nome_lezione,durata_normale_lezione,durata_turbo_lezione`, attenzione la prima riga dev'essere l'intestazione "lectureUUID,courses,insertedAt,title,duration,turboDuration".

3. In caso di cambio posizione di output, ricordarsi di inserire anche l'immagine "output/legend_seek_lectures.png"

4. Creazione file config.py (seguire esempio) e necessaria modifica dei parametri:
> - PATH_PRJ: path del progetto
> - DATE_RANGE_STUDY: periodo di studio dei dati modificabile in qualsiasi giornata
> - MD_PDF: flag che indica se eseguire la conversione dei file md (default: False)
>
> parametri che non necessitano modifiche:
> - PATH_DATA: path della cartella "data" (default: stessa posizione main.py)
> - PATH_COURSES_DATA: path del file "all_courses.csv" (default: posizione in "data/")
> - PATH_LECTURES_DATA: path del file "all_lectures.csv" (default: posizione in "data/")
> - PATH_OUTPUT: path per la stampa dei risultati (default: stessa posizione main.py)
>
> parametri che comportano modifica dei grafici:
> - TIME_UNIT: unita di tempo di certi grafici a linea
> - N_LECTURES_PER_CHART: numero di lezioni considerati da grafici a barre orizzontali

## Esecuzione
`python main.py` (tempo di esecuzione di 25 minuti, ottobre-gennaio)

## Output
La cartella "_reports" conterrà tutti i report elaborati. <br/>
Le altre cartelle hanno una funzione di supporto

## Struttura

<img src="https://github.com/AStrap/Reports_Txc2_DADdy/blob/main/utility/img/Struttura%20progetto.jpg" alt="Struttura del progetto"/>
