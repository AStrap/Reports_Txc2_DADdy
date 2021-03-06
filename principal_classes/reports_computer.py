# -*- coding: utf-8 -*-
import os
import subprocess
import math
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
import fitz
import gc

import support_classes.reports_manager as reports_manager

import config

class Reports_computer:

    PATH_OUTPUT = config.PATH_OUTPUT

    def __init__(self, dm):

        #-- data_manager
        self.dm = dm
        #--

        #-- report manager: elaborazion informazione per i report
        self.rm = reports_manager.Reports_manager(self.dm)
        #--
        return

    """
        Se flag config.MD_PDF == True:
            Stampa del report in markdown (es. idcorso_nomecorso-tmp.md)
            Conversione da markdown a pdf (es. idcorso_nomecorso-tmp.pdf)
            Conversione da pdf senza bookmarks a pdf con bookmarks (es. idcorso_nomecorso.pdf)
        altrimenti:
            Stampa del report in markdown (es. idcorso_nomecorso.md)

        Parametri:
            - id_course: str
                id del corso a cui si fa riferimento nel report
    """
    def compute_print(self, id_course):

        #-- cartella immagini per i reports
        self.path_imgs = "../%s-%s" %(id_course, self.dm.get_course_name(id_course))
        #--

        #-- file markdown del report
        total_bookmarks = list()
        if config.MD_PDF:
            name_file = "%s\\_reports\\%s-%s-tmp"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))
        else:
            name_file = "%s\\_reports\\%s-%s"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        f = open("%s.md" %(name_file), "w")
        f.write("# Report per il corso %s \n" %(self.dm.get_course_name(id_course)))

        #-- STRUTTURA DEI BOOKMARK
        # total_bookmars: lista dei bookmark principali
        #
        # Struttura singolo bookmarks
        #       ( nome bookmark per esempio: indice-indice bookmark padre-nome bookmark, nomero pagina rispetto bookmark root)
        # [("0-/-bookmark_root",0), [("1-0-esempio_nome",0),("2-0-esempio_nome",1),[("3-0-esempio_nome",2),[("4-3-esempio_nome",2)]]]]
        #
        # Sceglie nome bookmark univoco per una ricerca di pagine tramite ricerca per nome
        #--

        #-- sezioni report
        bookmarks_pdf = self.general_info(f, id_course)
        total_bookmarks.append(bookmarks_pdf)

        bookmarks_pdf = self.first_period_info(f, id_course)
        total_bookmarks.append(bookmarks_pdf)

        bookmarks_pdf = self.second_period_info(f, id_course)
        total_bookmarks.append(bookmarks_pdf)

        bookmarks_pdf = self.lectures_info(f, id_course)
        total_bookmarks.append(bookmarks_pdf)

        bookmarks_pdf = self.users_info(f, id_course)
        total_bookmarks.append(bookmarks_pdf)

        bookmarks_pdf = self.keywords_info(f, id_course)
        total_bookmarks.append(bookmarks_pdf)

        f.close()
        #--


        if config.MD_PDF:
            #-- md file to pdf
            p = subprocess.Popen('cmd /k "mdpdf \"%s/_reports/%s-%s-tmp.md\"" --border=12mm && exit' %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course)))
            p.wait()

            os.remove("%s.md"%(name_file))
            #--

            #-- pdt to pdf+bookmarks
            self.create_pdf_bookmarks(name_file, total_bookmarks)
            os.remove("%s.pdf"%(name_file))
            #--

        gc.collect
        return

    """
        Stampa informazioni generali riguardo il corso

        Parametri:
            - md_file: iowrapper
                file markdown del report

            - id_course: str
                id del corso a cui si fa riferimento nel report
    """
    def general_info(self, md_file, id_course):

        cur_page = 0
        bookmarks = [("Informazioni generali del corso", cur_page), list()]

        first_date, last_date = self.rm.get_first_last_lecture_dates(id_course)
        md_file.write("**Data primo caricamento video:** %s \n" %(self.edit_date(first_date)))
        md_file.write("**Data ultimo caricamento video:** %s <br/> \n" %(self.edit_date(last_date)))

        md_file.write("**Numero totale video caricati:** %d <br/> \n" %(len(self.dm.get_lectures_by_course(id_course))))

        first_exam, second_exam = self.rm.get_first_second_exam_dates(id_course)
        md_file.write("**Data primo appello d'esame:** %s \n" %(first_exam))
        md_file.write("**Data secondo appello d'esame:** %s <br/> \n" %(second_exam))

        md_file.write("**Numero di studenti che hanno almeno una sessione:** %d <br/> \n" %(len(self.dm.get_users_by_course(id_course))))

        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
        cur_page += 1

        return bookmarks

    """
        Stampa informazioni generali riguardo il periodo durante lo svolgimento
        del corso

        Parametri:
            - md_file: iowrapper
                file markdown del report

            - id_course: str
                id del corso a cui si fa riferimento nel report
    """
    def first_period_info(self, md_file, id_course):

        cur_page = 0
        bookmarks = [("Informazioni durante lo svolgimento del corso", cur_page), list()]

        first_period = self.rm.get_periods(id_course)[0]
        md_file.write("## Informazioni durante lo svolgimento del corso <br/> (Periodo 1: %s - %s ): \n" %(self.edit_date(first_period[0]), self.edit_date(first_period[1])))

        users = self.rm.users_period(first_period, id_course)
        md_file.write("**Numero di studenti che hanno almeno una sessione nel Periodo 1:** %d \n" %(len(users)))
        sessions = self.rm.sessions_period(first_period, id_course)
        md_file.write("**Numero totale di sessioni nel Periodo 1:** %s  \n" %(len(sessions)))
        md_file.write("**Numero medio di sessioni per studente nel Periodo 1:** %s  <br/> \n" %(str(round(len(sessions)/len(users), 2)) if len(users)>0 else 0))

        self.rm.print_session_day_distribution(id_course, first_period, "primo periodo")
        md_file.write("**Grafico con il numero di sessioni (verso il tempo)** \n")
        md_file.write("> <img src=\"%s/Sessioni_giorni_primo periodo.png\"/> <br/> \n \n" %(self.path_imgs))
        bookmarks[1].append(("grafico numero sessioni (verso il tempo)", cur_page))

        md_file.write("**Grafico con il numero di sessioni (verso data visualizzazione &#8722; data caricamento)** \n")
        md_file.write("> <img src=\"%s/Sessioni_pubblicazione_primo periodo.png\"/> <br/> \n \n" %(self.path_imgs))
        bookmarks[1].append(("grafico numero sessioni (verso data visualizzazione - data caricamento)", cur_page))

        self.rm.print_session_hours_distribution(id_course, first_period, "primo periodo")
        md_file.write("**Grafico con il numero di sessioni (verso orario della giornata)** \n")
        md_file.write("> <img src=\"%s/Sessioni_orario_primo periodo.png\"/> <br/> \n \n" %(self.path_imgs))
        bookmarks[1].append(("grafico numero sessioni (verso orario della giornata)", cur_page))

        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
        cur_page += 1

        self.rm.print_lectures_events(id_course, first_period, "primo periodo")
        md_file.write("**Grafico con il numero di eventi per lezione (eventi di salto o ricerca)** \n")
        bookmarks[1].append(("grafico numero eventi per lezione", cur_page))
        for c in range(math.ceil(len(self.dm.get_lectures_by_course(id_course))/config.N_LECTURES_PER_CHART)):
            md_file.write("> <img src=\"%s/Eventi_lezioni(%d)_primo periodo.png\" width=\"80%s\"/> <br/> \n" %(self.path_imgs, c, "%"))
            md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
            cur_page += 1

        self.rm.print_course_vision(id_course, first_period, "primo periodo")
        md_file.write("**Grafico con la distribuzione della copertura** \n")
        bookmarks[1].append(("grafico numero utenti per lezione", cur_page))
        for c in range(math.ceil(len(self.dm.get_lectures_by_course(id_course))/config.N_LECTURES_PER_CHART)):
            md_file.write("> <img src=\"%s/Utenti_lezioni(%d)_primo periodo.png\" width=\"80%s\"/> <br/> \n" %(self.path_imgs, c, "%"))
            md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
            cur_page += 1

        return bookmarks

    """
        Stampa informazioni generali riguardo il periodo dopo lo svolgimento
        del corso

        Parametri:
            - md_file: iowrapper
                file markdown del report

            - id_course: str
                id del corso a cui si fa riferimento nel report
    """
    def second_period_info(self, md_file, id_course):

        cur_page = 0
        bookmarks = [("Informazioni dopo il termine del corso", cur_page), list()]

        second_period = self.rm.get_periods(id_course)[1]

        if second_period[1] == "-":

            md_file.write("## Informazioni dopo il termine del corso <br/> (Periodo 2: %s - -- ): \n" %(self.edit_date(second_period[0])))
            md_file.write("**Dati ancora non disponibili**\n")

        else:

            md_file.write("## Informazioni dopo il termine del corso <br/> (Periodo 2: %s - %s ): \n" %(self.edit_date(second_period[0]), self.edit_date(second_period[1])))

            users = self.rm.users_period(second_period, id_course)
            md_file.write("**Numero di studenti che hanno almeno una sessione nel Periodo 2:** %d \n" %(len(users)))
            sessions = self.rm.sessions_period(second_period, id_course)
            md_file.write("**Numero totale di sessioni nel Periodo 2:** %s  \n" %(len(sessions)))
            md_file.write("**Numero medio di sessioni per studente nel Periodo 2:** %s  <br/> \n" %(str(round(len(sessions)/len(users), 2)) if len(users)>0 else 0))

            self.rm.print_session_day_distribution(id_course, second_period, "secondo periodo")
            md_file.write("**Grafico con il numero di sessioni (verso il tempo)** \n")
            md_file.write("> <img src=\"%s//Sessioni_giorni_secondo periodo.png\"/> <br/> \n \n" %(self.path_imgs))
            bookmarks[1].append(("grafico numero sessioni (verso il tempo)", cur_page))

            self.rm.print_session_hours_distribution(id_course, second_period, "secondo periodo")
            md_file.write("**Grafico con il numero di sessioni (verso orario della giornata)** \n")
            md_file.write("> <img src=\"%s/Sessioni_orario_secondo periodo.png\"/> <br/> \n \n" %(self.path_imgs))
            bookmarks[1].append(("grafico numero sessioni (verso orario della giornata)", cur_page))

            md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
            cur_page += 1

            self.rm.print_lectures_events(id_course, second_period, "secondo periodo")
            md_file.write("**Grafico con il numero di eventi per lezione (eventi di salto o ricerca)** \n")
            bookmarks[1].append(("grafico numero eventi per lezione", cur_page))
            for c in range(math.ceil(len(self.dm.get_lectures_by_course(id_course))/config.N_LECTURES_PER_CHART)):
                md_file.write("> <img src=\"%s/Eventi_lezioni(%d)_secondo periodo.png\" width=\"80%s\"/> <br/> \n" %(self.path_imgs, c, "%"))
                md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
                cur_page += 1

            self.rm.print_course_vision(id_course, second_period, "secondo periodo")
            md_file.write("**Grafico con la distribuzione della copertura** \n")
            bookmarks[1].append(("grafico numero utenti per lezione", cur_page))
            for c in range(math.ceil(len(self.dm.get_lectures_by_course(id_course))/config.N_LECTURES_PER_CHART)):
                md_file.write("> <img src=\"%s/Utenti_lezioni(%d)_secondo periodo.png\" width=\"80%s\"/> <br/> \n" %(self.path_imgs, c, "%"))
                md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
                cur_page += 1

        return bookmarks

    """
        Stampa informazioni generali riguardo le lezioni

        Parametri:
            - md_file: iowrapper
                file markdown del report

            - id_course: str
                id del corso a cui si fa riferimento nel report
    """
    def lectures_info(self, md_file, id_course):

        cur_page = 0
        bookmarks = [("Dettagli sulle lezioni", cur_page), list()]

        md_file.write("## Dettagli sulle lezioni \n")

        lectures = self.rm.get_lectures_total_info(id_course)
        md_file.write("Visione media: media ercentuale tra le percentuali di visione di ogni utente che ha visto la lezione \n")
        md_file.write("| LEZIONE | #UTENTI | #SESSIONI | #DOWNLOAD | VISIONE MEDIA | \n")
        md_file.write("| ------- | ------- | ------- | ------- | ------- | \n")
        for l in lectures:
            md_file.write("| %s | %s | %s | %s | %s | \n" %(l[0], l[1], l[2], l[3], l[4]))

        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
        cur_page += 1

        i = 0
        for i,id_lecture in enumerate(self.dm.get_lectures_by_course(id_course)):
            try:
                os.mkdir("%s\\%s-%s\\lezioni" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course)))
            except:
                pass
        for i,id_lecture in enumerate(self.dm.get_lectures_by_course(id_course)):
            gc.collect
            try:
                os.mkdir("%s\\%s-%s\\lezioni\\lezione_%d" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course), i))
            except:
                pass
        self.rm.print_lectures_vision(id_course)
        self.rm.print_lectures_average_speed(id_course)
        self.rm.print_lectures_seek_events(id_course)
        for i,id_lecture in enumerate(self.dm.get_lectures_by_course(id_course)):
            md_file.write("### %s \n" %(self.dm.get_lecture_name(id_lecture)))
            md_file.write("**grafico copertura di visione** \n")
            md_file.write("> <img src=\"%s/lezioni/lezione_%d/Visioni_lezione_%d.png\"/> <br/> \n \n" %(self.path_imgs, i, i))
            md_file.write("**grafico copertura di visione univoca per utente** \n")
            md_file.write("> <img src=\"%s/lezioni/lezione_%d/Visioni_unic_lezione_%d.png\"/> <br/> \n \n" %(self.path_imgs, i, i))
            md_file.write("**grafico velocit&#224; media visualizzazione** \n")
            md_file.write("> <img src=\"%s/lezioni/lezione_%d/Velocita_lezione_%d.png\"/> <br/> \n \n" %(self.path_imgs, i, i))
            md_file.write("**grafico studio eventi di salto temporale** \n")
            md_file.write("> <div><img src=\"../legend_seek_lectures.png\" width=\"70%s\"/> \n" %("%"))
            md_file.write(" <img src=\"%s/lezioni/lezione_%d/Seek_lezione_%d.png\"/></div> <br/> \n \n" %(self.path_imgs, i, i))
            bookmarks[1].append(("grafici lezione: %s" %(self.dm.get_lecture_name(id_lecture)), cur_page))

            md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
            cur_page += 1

        return bookmarks

    """
        Stampa informazioni generali riguardo gli utenti

        Parametri:
            - md_file: iowrapper
                file markdown del report

            - id_course: str
                id del corso a cui si fa riferimento nel report
    """
    def users_info(self, md_file, id_course):

        cur_page = 0
        bookmarks = [("Dettagli sugli utenti", cur_page), list()]

        md_file.write("## Dettagli sugli utenti \n")
        users_info = self.rm.get_users_info(id_course)
        users_clusters = self.rm.get_users_clusters(id_course)
        n_clusters = len(users_clusters)
        if len(users_info)>0:
            md_file.write("Cluster%d -> cluster%d\n" %(0, n_clusters-1))
            md_file.write("visione pi&#249; completa del corso -> visione pi&#249; mirata in punti ostici del corso \n")

            tmp = "| "
            tmp2 = "| "
            for i in range(n_clusters):
                tmp = "%sCluster%d | " %(tmp, i)
                tmp2 = "%s:--- | " %(tmp2)
            tmp = "%s\n" %(tmp); tmp2 = "%s\n" %(tmp2)
            md_file.write(tmp)
            md_file.write(tmp2)

            tmp = "| "
            for cluster in users_clusters:
                for i,id_user in enumerate(cluster):
                    if i%2 == 1:
                        tmp = "%s%s<br/> " %(tmp, id_user)
                    else:
                        tmp = "%s%s " %(tmp, id_user)
                if i%2 == 1:
                    tmp = tmp[:-6]
                tmp = "%s | " %(tmp)

            tmp = "%s\n\n" %(tmp)
            md_file.write(tmp)

        md_file.write("Visione media: media percentuale tra le percentuali di visione delle lezioni viste dall'utente \n")
        md_file.write("Lezione pi&#249; vista: in termini di secondi di lezione visti dall'utente <br/> \n")

        md_file.write("| UTENTE | #SESSIONI | #LEZIONI | VISIONE MEDIA | LEZIONE PI&#217; VISTA | #EVENTI | #PAUSE | #BACKWARD | \n")
        md_file.write("| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | \n")

        for user_info in users_info:
            md_file.write("| %s | %s | %s | %s | %s | %s | %s | %s | \n" %(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5], user_info[6], user_info[7]))

        md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
        cur_page += 1

        return bookmarks


    """
        Stampa informazioni riguardo le keyword cercate

        Parametri:
            - md_file: iowrapper
                file markdown del report

            - id_course: str
                id del corso a cui si fa riferimento nel report
    """
    def keywords_info(self, md_file, id_course):

        cur_page = 0
        bookmarks = [("Dettagli sulle keyword", cur_page), list()]

        keywords = self.rm.get_keywords(id_course)

        md_file.write("## Dettagli sulle keyword cercate \n")
        md_file.write("**Numero di ricerche effettuate:** %s \n" %(len(keywords)))

        md_file.write("**Keywords cercate:** \n")
        md_file.write("| KEYWORD | LEZIONE | MINUTAGGIO LEZIONE | ID UTENTE | \n")
        md_file.write("| ------- | ------- | ------- | ------- | \n")
        for k in keywords:
            md_file.write("| %s | %s | %s | %s | \n" %(k[0], k[1], k[2], k[3]))

        #md_file.write("<div style=\"page-break-after: always;\"></div>\n\n")
        #cur_page += 1

        return bookmarks

    #--------------------------------------------------------------------------

    """
        Crea pdf con bookmarks

        Parametri:
            - name_file: str
                path del file senza estensione

            - total_bookmarks: list()
                lista dei bookmarks da inserire
    """
    def create_pdf_bookmarks(self, name_file, total_bookmarks):

        #-- scorimento bookmark principali per calcolo pagine
        titles = ["Report per il corso"]
        for b in total_bookmarks[1:]:
            titles.append(b[0][0])
        #--

        output_file = PdfFileWriter()

        #-- aggiornamento pagine
        with fitz.open("%s.pdf" %(name_file)) as doc:
            for p,page in enumerate(doc):
                for i,title in enumerate(titles):
                    if title in page.get_text():
                        total_bookmarks[i] = self.update_pages(total_bookmarks[i], p)

        #--

        #-- lettura contenuto pdf
        input_stream = open("%s.pdf" %(name_file), "rb")
        input_file = PdfFileReader(input_stream)
        n_pages = input_file.numPages
        for p in range(n_pages):
            output_file.addPage(input_file.getPage(p))
        #--

        #-- inserimento bookmarks
        self.compute_bookmarks(output_file, total_bookmarks)
        #--

        #--
        with Path("%s.pdf" %(name_file[:-4])).open(mode="wb") as pdf_file:
            output_file.write(pdf_file)

        input_stream.close()
        return

    """
        Aggiornamento pagine dei bookmarks

        Parametri:
            - bookmarks: list()
                lista bookmark

            - p: int
                pagina corrispondente al bookmark principale a cui fanno
                riferimento i bookmark figli

        Return:
            - bookmarks: list()
                lista bookmark con pagine aggiornate
    """
    def update_pages(self, bookmarks, p):

        if type(bookmarks) == list:
            bookmarks[0] = (bookmarks[0][0], bookmarks[0][1]+p)
            for i, node in enumerate(bookmarks[1]):
                bookmarks[1][i] = self.update_pages(node, p)
        else:
            bookmarks = (bookmarks[0], bookmarks[1]+p)

        return bookmarks

    """
        Crea bookmarks in modo ricorsivo nel pdf

        Parametri:
            output_file:
                file pdf finale

            bookmarks: list()
                lista bookmarks

            parent: int
                bookmark padre
    """
    def compute_bookmarks(self, output_file, bookmarks, parent=None):

        for b in bookmarks:

            if type(b) != tuple:
                node = output_file.addBookmark(b[0][0], b[0][1], parent)
                self.compute_bookmarks(output_file, b[1], node)
            else:
                node = output_file.addBookmark(b[0], b[1], parent)

        return
    """
        Modifica formato data YYYY-MM-DD -> DD-MM-YYYY

        Parametri:
            - date: str
                data da modificare
    """
    def edit_date(self, date):
        y = date[:4]; m = date[5:7]; d = date[8:]
        return "%s-%s-%s" %(d,m,y)
