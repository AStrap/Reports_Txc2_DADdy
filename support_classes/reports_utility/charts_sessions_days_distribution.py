# -*- coding: utf-8 -*-
import math
import calendar

import config
import utility.time_date as time_date

class Charts_sessions_days_distribution:

    PATH_OUTPUT = config.PATH_OUTPUT

    def __init__(self, dm, em):
        #-- data manager
        self.dm = dm
        #--

        #-- excel manager
        self.em = em
        #--

        return

    """
        Calcolo e stampa grafici riguardo l'uso dei dispositivi

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - workbook_name: str
                nome file excel in cui salvati i grafici
    """
    def compute_print(self, id_course, label_period, period):
        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        workbook_name = "sessions_days_distribution_%s_%s.xlsx" %(label_period, self.dm.get_course_name(id_course))

        self.em.set_workbook(workbook_name, path_output_course)

        #-- giorni presenti nel periodo
        days_period = time_date.get_days_by_period(period)
        #--

        self.compute_sessions_per_days("Sessioni_per_giornata", id_course, label_period, period, days_period)

        if label_period == "primo periodo":
            self.compute_sessions_from_pubblication("Sessioni_da_pubblicazione", id_course, label_period, period, days_period)

        self.em.close_workbook()

        return workbook_name

    """
        Calcolo e stampa delle informazioni riguardo al numero di sessioni per giornata

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio

            - days_period: list() (es. ["YYYY-MM-DD", "YYYY-MM-DD"])
                giorni da cosiderare
    """
    def compute_sessions_per_days(self, sheet, id_course, label_period, period, days_period):

        self.em.add_worksheet(sheet)
        self.em.set_cursors(1, 1)

        #-- sessioni per giornata
        c_x_i, c_y = self.em.get_cursors()

        head = [["GIORNO", "NUMERO SESSIONI"]]
        body = []

        for day in days_period:
            body.append([day, len(self.dm.get_sessions_by_course_days(id_course, [day]))])

        self.em.write_head_table(head)
        self.em.write_body_table(body)

        c_x, c_y = self.em.get_cursors()

        self.em.print_line_chart("ver", (c_x_i+1,c_x-1), (c_y, c_y+1), sheet, "Sessioni per giornata - %s" %(label_period), "giornata", "numero sessioni", c_x_i, c_y+3, {'min':0})
        #--
        return

    """
        Calcolo e stampa delle numero di sessioni totale istanziate dalla pubblicazione
        di ogni lezione e grafico

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio

            - days_period: list() (es. ["YYYY-MM-DD", "YYYY-MM-DD"])
                giorni da cosiderare
    """
    def compute_sessions_from_pubblication(self, sheet, id_course, label_period, period, days_period):

        y = int(period[1][:4]); m = int(period[1][5:7]); d = int(period[1][8:])
        if d == calendar.monthrange(y,m)[1]:
            d = 1
            if m == 12:
                m = 1; y += 1
            else:
                m += 1
        else:
            d += 1
        last_date = "%d-%.2d-%.2dT%.2d:%.2d:%.2d.00" %(y,m,d,2,0,0)
        last_date = time_date.get_datetime(last_date)

        self.em.add_worksheet(sheet)
        self.em.set_cursors(1, 1)

        self.days_max = 0

        # dizionario lezione:giorno, indica quanti giorni ci sono tra la
        # pubblicazione della lezione e l'ultimo giorno considerato dallo studio
        self.dict_days=dict()

        for l in self.dm.get_lectures_by_course(id_course):
            #calcolo giorni
            release_date = self.dm.get_lecture_release_date(l)
            release_date = time_date.get_datetime(release_date)
            diff = last_date-release_date
            days = math.ceil((diff.total_seconds()/3600)/24)
            if days > self.days_max:
                self.days_max = days

            self.dict_days[l]=days

        #-- calcolo delle sessioni
        lectures_sessions = dict()
        for l in self.dm.get_lectures_by_course(id_course):
            lectures_sessions[l] = [0 for _ in range(self.days_max+2)]
            if self.dict_days[l]<self.days_max:
                lectures_sessions[l][self.dict_days[l]+1]=-1
            sessions = self.dm.get_sessions_by_course_lecture_days(id_course, l, days_period)

            for s in sessions:
                date = time_date.get_datetime(s[1][:-6])
                release_date = self.dm.get_lecture_release_date(l)
                release_date = time_date.get_datetime(release_date)
                diff = date-release_date
                days = math.floor((diff.total_seconds()/3600)/24)
                lectures_sessions[l][days]+=1
        #--

        #-- stampa della tabella
        days = [i for i in range(1, self.days_max+2)]
        head = [["GIORNI DA PUBBLICAZIONE", "TOTALE SESSIONI"]]
        body = []
        c_x_i, c_y_i = self.em.get_cursors()
        #media sessioni
        for i,d in enumerate(days):
            tot = 0
            n_sessions = 0
            for l in lectures_sessions.keys():
                if lectures_sessions[l][i] > 0:
                    tot += lectures_sessions[l][i]
                    n_sessions += 1
            body.append([d,tot])

        self.em.write_head_table(head)
        self.em.write_body_table(body)
        #--

        #-- stampa del grafico
        c_x, c_y = self.em.get_cursors()
        self.em.print_line_chart("ver", (c_x_i+1,c_x-1), (c_y, c_y+1), sheet, "Sessioni per giornata dalla pubblicazione - %s" %(label_period), "giornata", "numero sessioni", c_x_i, c_y+3, {'min':0})

        return
