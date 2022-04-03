#---
# Configuarzioni del progetto
#---

#--- path del progetto
#-- DA MODIFICARE
PATH_PRJ = "/home/user/"
#---

#--- periodo di studio
DATE_RANGE_STUDY = ("2021-10-01", "2022-02-28")
#---

#--- path dei dati
#- path dati json delle sessioni
PATH_DATA = "%s/data" %(PATH_PRJ)
#-

#- path file corsi
PATH_COURSES_DATA = "%s/all_courses.csv" %(PATH_DATA)
#-

#- path file lectures
PATH_LECTURES_DATA = "%s/all_lectures.csv" %(PATH_DATA)
#-
#---

#--- path dei risultati in output
PATH_OUTPUT = "%s/output" %(PATH_PRJ)
#---

#--- flag esecuzione conversione markdown to pdf
# linea codice esecuzione conversione reports_computer.py [94-95]
MD_PDF = False
#---

#--- unità di tempo di studio (secondi)
TIME_UNIT = 1*60
#---

#--- numero lezioni per grafico a barre
N_LECTURES_PER_CHART = 30
#---
