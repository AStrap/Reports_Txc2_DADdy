# -*- coding: utf-8 -*-
import math

import config
import utility.time_date as time_date
import utility.chart_printer as chart_printer

class Chart_course_vision:

    PATH_OUTPUT = config.PATH_OUTPUT
    N_LECTURES_PER_CHART = config.N_LECTURES_PER_CHART

    def __init__(self, dm):
        #-- data manager
        self.dm = dm
        #--

        return

    """
        Calcolo e stampa dei grafici riguardo un corso

        Parametri:
            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio

        Return:
            - workbook_name: str
                nome file excel dove sono salvati i grafici

    """
    def compute_print(self, id_course, label_period, period):
        path_output_course = "%s\\%s-%s" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        self.compute_users_per_lecture(id_course, label_period, period, path_output_course)

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
    """
    def compute_users_per_lecture(self, id_course, label_period, period, path_output_course):

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

            val_x = list()
            val_y = list()

            max_user = 0
            for l in tmp_lectures:
                sessions = self.dm.get_sessions_by_course_lecture_days(id_course, l, days)

                users = list()
                for s in sessions:
                    if not s[-1] in users:
                        users.append(s[-1])

                val_x.append(self.dm.get_lecture_name(l))
                val_y.append(len(users))

                if len(users)>max_user:
                    max_user = len(users)

            # option_x = dict()
            # if max_user < 10:
            #     option_x['unit'] = 1

            chart_printer.print_bar_chart(val_x, val_y, "Utenti per lezione - %s" %(label_period), "numero utenti", "lezione", {}, path_output_course, "Utenti_lezioni(%d)_%s"%(c,label_period))
        #--
        return
