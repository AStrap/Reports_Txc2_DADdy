# -*- coding: utf-8 -*-
import math

import support_classes.chart_printer as chart_printer

import config
import utility.time_date as time_date

class Chart_lectures_events:

    PATH_OUTPUT = config.PATH_OUTPUT
    N_LECTURES_PER_CHART = config.N_LECTURES_PER_CHART

    def __init__(self, dm):
        # data manager
        self.dm = dm

        return

    """
        Calcolo e stampa dei grafici riguado numero eventi totali eseguiti nelle
        lezioni

        Parametri:
            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio
    """
    def compute_print(self, id_course, label_period, period):
        path_output_course = "%s\\%s-%s" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        self.compute_events_per_lecture(id_course, label_period, period, path_output_course)

        return

    """
        Calcolo e stampa del numero di utenti per lezione

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio

            - path_output_course: str
                path output specifica per il corso considerato
    """
    def compute_events_per_lecture(self, id_course, label_period, period, path_output_course):

        lectures = self.dm.get_lectures_by_course(id_course)
        n_charts = math.ceil(len(lectures)/self.N_LECTURES_PER_CHART)

        #-- giorni da considerare
        days = time_date.get_days_by_period(period)
        #--

        for c in range(n_charts):

            tmp_lectures = 0
            if c != n_charts-1:
                tmp_lectures = lectures[c*self.N_LECTURES_PER_CHART:(c+1)*self.N_LECTURES_PER_CHART]
            else:
                tmp_lectures = lectures[c*self.N_LECTURES_PER_CHART:]

            #-- calcolo dati
            val_x = list(); val_y = list()

            max_events = 0
            for l in tmp_lectures:
                sessions = self.dm.get_sessions_by_course_lecture_days(id_course, l, days)

                n_events = 0
                for s in sessions:
                    for i,e in enumerate(s[3]):
                        if e[0] in ["PL", "PS", "SC", "SL", "KW", "SK", "BM"]:
                            if e[0] in ["SL", "SC", "KW"]:
                                if i+1 != len(s[3]) and s[3][i+1]=="SK":
                                    n_events -= 1
                            n_events += 1
                val_x.append(self.dm.get_lecture_name(l))
                val_y.append(n_events)

                if n_events>max_events:
                    max_events = n_events
            #--

            #-- stampa grafico
            cp = chart_printer.Chart_printer()
            cp.print_bar_chart(val_x, val_y, "Eventi per lezione - %s" %(label_period), "numero eventi", "lezione", {'max':max_events}, path_output_course, "Eventi_lezioni(%d)_%s"%(c, label_period))
            del cp
            #--
        return
