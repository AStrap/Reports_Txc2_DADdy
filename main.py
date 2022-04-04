# -*- coding: utf-8 -*-
import os

import support_classes.data_manager as data_manager
import principal_classes.reports_computer as reports_computer

import config
PATH_OUTPUT = config.PATH_OUTPUT

def main():
    #-- data manager: gestiore dei dati
    dm = data_manager.Data_manager()
    dm.load_data()

    # lista corsi e lezioni di cui mancano le informazioni
    miss_courses, miss_lectures = dm.get_miss_info()
    if len(miss_courses)>0 or len(miss_lectures)>0:
        for c in miss_courses:
            print("Informazioni mancanti per il corso: %s" %c)

        for l in miss_lectures:
            print("Informazioni mancanti per la lezione: %s" %l)

        exit()
    #--

    #-- creazione cartelle output
    for c in dm.get_courses():
    #for c in [""]:
        try:
            os.mkdir("%s\\%s-%s" %(PATH_OUTPUT, c, dm.get_course_name(c)))
        except:
            pass

    try:
        os.mkdir("%s\\_reports" %(PATH_OUTPUT))
    except:
        pass
    #--

    #-- stampa report per ogni classe
    rc = reports_computer.Reports_computer(dm)

    for i,id_course in enumerate(dm.get_courses()):
    #for i,id_course in enumerate(["32503"]):
        print("---%d su %d" %(i+1, len(dm.get_courses())))
        print("Calcolo report: %s - %s" %(id_course, dm.get_course_name(id_course)))
        rc.compute_print(id_course)
        print("---")
    #--

    return

if __name__ == "__main__":
    main()
