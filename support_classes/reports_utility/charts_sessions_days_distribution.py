# -*- coding: utf-8 -*-
import math
import calendar

import support_classes.chart_printer as chart_printer

import config
import utility.time_date as time_date

class Charts_sessions_days_distribution:

    PATH_OUTPUT = config.PATH_OUTPUT

    def __init__(self, dm):
        #-- data manager
        self.dm = dm
        #--

        return

    """
        Calcolo e stampa grafici riguardo la distribuzioni di istanziamento
        delle sessioni

        Parametri:
            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio
    """
    def compute_print(self, id_course, label_period, period):
        path_output_course = "%s/%s-%s" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        self.compute_sessions_per_days(id_course, label_period, period, path_output_course)

        if label_period == "primo periodo":
            self.compute_sessions_from_pubblication(id_course, label_period, period, path_output_course)

        return

    """
        Calcolo e stampa delle informazioni riguardo al numero di sessioni per giornata

        Parametri:
            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio

            - path_output_course: str
                path output specifica per il corso considerato
    """
    def compute_sessions_per_days(self, id_course, label_period, period, path_output_course):

        #-- giorni presenti nel periodo
        days_period = time_date.get_days_by_period(period)
        #--

        #-- stampa grafico
        val_x = list(); val_y = list()
        for day in days_period:
            val_x.append(day)
            val_y.append(len(self.dm.get_sessions_by_course_days(id_course, [day])))
        cp = chart_printer.Chart_printer()
        cp.print_line_chart(val_x, val_y, "Sessioni per giornata - %s" %(label_period), "giornata", "numero sessioni", {'min':0}, path_output_course, "Sessioni_giorni_%s" %(label_period))
        del cp
        #--
        return

    """
        Calcolo e stampa delle numero di sessioni totale istanziate dalla pubblicazione
        di ogni lezione e grafico

        Parametri:
            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio

            - days_period: list() (es. ["YYYY-MM-DD", "YYYY-MM-DD"])
                giorni da cosiderare

            - path_output_course: str
                path output specifica per il corso considerato
    """
    def compute_sessions_from_pubblication(self, id_course, label_period, period, path_output_course):

        #-- giorni presenti nel periodo
        days_period = time_date.get_days_by_period(period)
        #--

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

        days = [i for i in range(1, self.days_max+2)]
        val_x = list(); val_y = list()

        for i,d in enumerate(days):
            tot = 0
            n_sessions = 0
            for l in lectures_sessions.keys():
                if lectures_sessions[l][i] > 0:
                    tot += lectures_sessions[l][i]
                    n_sessions += 1

            val_x.append(d)
            val_y.append(tot)
        #--

        #-- stampa del grafico
        cp = chart_printer.Chart_printer()
        cp.print_line_chart(val_x, val_y, "Sessioni per giornata dalla pubblicazione - %s" %(label_period), "giornata", "numero sessioni", {'min':0}, path_output_course, "Sessioni_pubblicazione_%s" %(label_period))
        del cp
        #--

        return
