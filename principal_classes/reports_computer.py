# -*- coding: utf-8 -*-
import os

import config
import support_classes.reports_manager as reports_manager

class Reports_computer:
    
    PATH_OUTPUT = config.PATH_OUTPUT
    
    def __init__(self, dm, em):
        
        #-- data_manager
        self.dm = dm
        #--
        
        #-- excel_manager
        self.em = em
        #--
        
        #-- report manager: elaborazione informazione per report
        self.rm = reports_manager.Reports_manager(self.dm, self.em)
        #--
        return
    
    """
        Calcolo e stampa del report
    """
    def compute_print(self, id_course):
        
        #-- cartella immagini per i reports
        self.path_imgs = "../%s-%s/img" %(id_course, self.dm.get_course_name(id_course))
        #--
        
        #-- file markdown report
        f = open("%s\\_reports\\%s-%s.md"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course)), "w")
        f.write("# Report per il corso %s \n" %(self.dm.get_course_name(id_course)))
        
        self.general_info(f, id_course)
        
        self.first_period_info(f, id_course)
        
        self.second_period_info(f, id_course)
        
        self.lectures_info(f, id_course)
        
        self.users_info(f, id_course)
        
        self.keywords_info(f, id_course)
        
        f.close()
        #--
        
        #-- md file to pdf
        os.chdir("%s\\_reports" %(self.PATH_OUTPUT))
        os.system('cmd /k "mdpdf \"./%s-%s.md\"" --border=12mm' %(id_course, self.dm.get_course_name(id_course)))
        os.remove("%s\\_reports\\%s-%s.md"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))) 
        #--
        
        return
        
    """
        Stampa informazioni generali riguardo il corso
        
        Parametri:
            md_file: iowrapper
                file markdown output
                
            id_course: string
                
    """
    def general_info(self, md_file, id_course):
        
        first_date, last_date = self.rm.get_first_last_lecture_dates(id_course)
        md_file.write("**Data primo caricamento video:** %s \n" %(self.edit_date(first_date)))
        md_file.write("**Data ultimo caricamento video:** %s <br/> \n" %(self.edit_date(last_date)))
        
        md_file.write("**Numero totale video caricati:** %d <br/> \n" %(len(self.dm.get_lectures_by_course(id_course))))
       
        first_exam, second_exam = self.rm.get_first_second_exam_dates(id_course)
        md_file.write("**Data primo appello d'esame:** %s \n" %(first_exam))        
        md_file.write("**Data secondo appello d'esame:** %s <br/> \n" %(second_exam))
        
        md_file.write("**Numero di studenti che hanno almeno una sessione:** %d <br/> \n" %(len(self.dm.get_users_by_course(id_course))))
        
        lectures = self.rm.get_lectures_total_info(id_course)
        md_file.write("**Dettagli generali sulle lezioni:**\n")
        md_file.write("Visione media: media ercentuale tra le percentuali di visione di ogni utente che ha visto la lezione \n")
        md_file.write("| LEZIONE | #UTENTI | #SESSIONI | #DOWNLOAD | VISIONE MEDIA | \n")
        md_file.write("| ------- | ------- | ------- | ------- | ------- | \n")
        for l in lectures:
            md_file.write("| %s | %s | %s | %s | %s | \n" %(l[0], l[1], l[2], l[3], l[4]))
        
        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")             
        return
    
    """
        Stampa informazioni generali riguardo il periodo durante lo svolgimento 
        del corso
        
        Parametri:
            md_file: iowrapper
                file markdown output
                
            id_course: string
    """
    def first_period_info(self, md_file, id_course):
        
        first_period = self.rm.get_periods(id_course)[0]
        md_file.write("## Durante lo svolgimento del corso <br/> (Periodo 1: %s - %s ): \n" %(self.edit_date(first_period[0]), self.edit_date(first_period[1])))
        
        users = self.rm.users_period(first_period, id_course)
        md_file.write("**Numero di studenti che hanno almeno una sessione nel Periodo 1:** %d \n" %(len(users)))
        sessions = self.rm.sessions_period(first_period, id_course)
        md_file.write("**Numero totale di sessioni nel Periodo 1:** %s  \n" %(len(sessions)))
        md_file.write("**Numero medio di sessioni per studente nel Periodo 1:** %s  <br/> \n" %(str(round(len(sessions)/len(users), 2)) if len(users)>0 else 0))
        
        self.rm.print_session_day_distribution(id_course, first_period, "primo periodo")
        md_file.write("**Grafico con il numero di sessioni (verso il tempo)** \n")
        md_file.write("<img src=\"%s/day_distribution_primo periodo/chart1.png\"/> <br/> \n" %(self.path_imgs))
        
        md_file.write("**Grafico con il numero di sessioni (verso data visualizzazione &#8722; data caricamento)** \n")
        md_file.write("<img src=\"%s/day_distribution_primo periodo/chart2.png\"/> <br/> \n" %(self.path_imgs))
        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")

        self.rm.print_course_vision(id_course, first_period, "primo periodo")
        md_file.write("**Grafico con la distribuzione della copertura** \n")
        md_file.write("<img src=\"%s/course_vision_primo periodo/chart1.png\" width=\"80%s\"/> <br/> \n" %(self.path_imgs, "%"))

        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")              
        return
    
    """
        Stampa informazioni generali riguardo il periodo dopo lo svolgimento 
        del corso
        
        Parametri:
            md_file: iowrapper
                file markdown output
                
            id_course: string
    """
    def second_period_info(self, md_file, id_course):
        second_period = self.rm.get_periods(id_course)[1]
        
        if second_period[1] == "-":
            
            md_file.write("## Dopo il termine del corso <br/> (Periodo 2: %s - -- ): \n" %(self.edit_date(second_period[0])))
            md_file.write("**Dati ancora non disponibili**")
            
        else:
            
            md_file.write("## Dopo il termine del corso <br/> (Periodo 2: %s - %s ): \n" %(self.edit_date(second_period[0]), self.edit_date(second_period[1])))
            
            users = self.rm.users_period(second_period, id_course)
            md_file.write("**Numero di studenti che hanno almeno una sessione nel Periodo 2:** %d \n" %(len(users)))
            sessions = self.rm.sessions_period(second_period, id_course)
            md_file.write("**Numero totale di sessioni nel Periodo 2:** %s  \n" %(len(sessions)))
            md_file.write("**Numero medio di sessioni per studente nel Periodo 2:** %s  <br/> \n" %(str(round(len(sessions)/len(users), 2)) if len(users)>0 else 0))
            
            self.rm.print_session_day_distribution(id_course, second_period, "secondo periodo")
            md_file.write("**Grafico con il numero di sessioni (verso il tempo)** \n")
            md_file.write("<img src=\"%s/day_distribution_secondo periodo/chart1.png\"/> <br/> \n" %(self.path_imgs))
            md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
    
            self.rm.print_course_vision(id_course, second_period, "secondo periodo")
            md_file.write("**Grafico con la distribuzione della copertura** \n")
            md_file.write("<img src=\"%s/course_vision_secondo periodo/chart1.png\" width=\"80%s\"/> <br/> \n" %(self.path_imgs, "%"))
    
        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")              
        return
    
    """
        Stampa informazioni generali riguardo le lezioni
        
        Parametri:
            md_file: iowrapper
                file markdown output
                
            id_course: string
    """
    def lectures_info(self, md_file, id_course):
        md_file.write("## Dettagli sulle lezioni \n")
        
        i = 0
        self.rm.print_lectures_average_speed(id_course)
        self.rm.print_lectures_vision(id_course)
        for i,id_lecture in enumerate(self.dm.get_lectures_by_course(id_course)):
            
            md_file.write("### %s \n" %(self.dm.get_lecture_name(id_lecture)))
            
            md_file.write("**grafico velocit&#224; media visualizzazione** \n")
            md_file.write("<img src=\"%s/lecture_average_speed/chart%d.png\"/> <br/> \n" %(self.path_imgs, i+1))
            md_file.write("**grafico copertura** \n")
            md_file.write("<img src=\"%s/lecture_vision/chart%d.png\"/> <br/> \n" %(self.path_imgs, i+1))
            
            if i%2 == 1:
                md_file.write("<div style=\"page-break-after: always;\"></div>\n\n") 
        if i%2 == 0:
            md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
        
        return
    
    """
        Stampa informazioni generali riguardo gli utenti
        
        Parametri:
            md_file: iowrapper
                file markdown output
                
            id_course: string
    """
    def users_info(self, md_file, id_course):
        md_file.write("## Dettagli sugli utenti \n")
        md_file.write("Visione media: media percentuale tra le percentuali di visione delle lezioni viste dall'utente \n")
        md_file.write("Lezione pi&#249; vista: in termini di secondi di lezione visti dall'utente <br/> \n")
        
        md_file.write("| UTENTE | #SESSIONI | #LEZIONI | VISIONE MEDIA | LEZIONE PI&#217; VISTA | #EVENTI | #PAUSE | #BACKWARD | \n")
        md_file.write("| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | \n")

        for user_info in self.rm.get_users_info(id_course): 
            md_file.write("| %s | %s | %s | %s | %s | %s | %s | %s | \n" %(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5], user_info[6], user_info[7]))

        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
        return
    
    
    """
        Stampa informazioni riguardo le keyword cercate
        
        Parametri:
            md_file: iowrapper
                file markdown output
                
            id_course: string
    """
    def keywords_info(self, md_file, id_course):
        keywords = self.rm.get_keywords(id_course)
        
        md_file.write("## Dettagli sulle keyword cercate \n")
        md_file.write("**Numero di ricerche effettuate:** %s \n" %(len(keywords)))
        
        md_file.write("**Keywords cercate:** \n")
        md_file.write("| KEYWORD | LEZIONE | MINUTAGGIO LEZIONE | ID UTENTE | \n")
        md_file.write("| ------- | ------- | ------- | ------- | \n")
        for k in keywords:
            md_file.write("| %s | %s | %s | %s | \n" %(k[0], k[1], k[2], k[3]))
        return
    
    #--------------------------------------------------------------------------
    
    """
        Modifica formato data YYYY-MM-DD -> DD-MM-YYYY
    """
    def edit_date(self, date):
        y = date[:4]; m = date[5:7]; d = date[8:]
        return "%s-%s-%s" %(d,m,y)
