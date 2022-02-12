# -*- coding: utf-8 -*-
import math

import config
import utility.time_date as time_date

class Chart_lectures_events:

    PATH_OUTPUT = config.PATH_OUTPUT
    N_LECTURES_PER_CHART = config.N_LECTURES_PER_CHART

    def __init__(self, dm, em):
        # data manager
        self.dm = dm

        # excel manager
        self.em = em

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
        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        workbook_name = "lezioni_eventi_%s_%s.xlsx" %(label_period, self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)

        self.compute_events_per_lecture("Eventi_per_lezione", id_course, label_period, period)

        self.em.close_workbook()
        return workbook_name

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

        Return:
            - workbook_name: str
                nome file excel dove sono salvati i grafici
    """
    def compute_events_per_lecture(self, sheet, id_course, label_period, period):

        lectures = self.dm.get_lectures_by_course(id_course)
        n_charts = math.ceil(len(lectures)/self.N_LECTURES_PER_CHART)

        #-- giorni da considerare
        days = time_date.get_days_by_period(period)
        #--

        for c in range(n_charts):

            self.em.add_worksheet("%s%s" %(sheet, c))
            self.em.set_cursors(1, 1)

            tmp_lectures = 0
            if c != n_charts-1:
                tmp_lectures = lectures[c*self.N_LECTURES_PER_CHART:(c+1)*self.N_LECTURES_PER_CHART]
            else:
                tmp_lectures = lectures[c*self.N_LECTURES_PER_CHART:]

            c_x_i, c_y = self.em.get_cursors()

            head = [["LEZIONE", "NUMERO EVENTI"]]
            body = []

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

                body.append([self.dm.get_lecture_name(l), n_events])
                if n_events>max_events:
                    max_events = n_events

            option_x = dict()
            if max_events < 10:
                option_x['major_unit'] = 1

            self.em.write_head_table(head)
            self.em.write_body_table(body)

            c_x, c_y = self.em.get_cursors()

            self.em.print_bar_chart("ver", (c_x_i+1,c_x-1), (c_y, c_y+1), "%s%s" %(sheet, c), "Eventi per lezione - %s" %(label_period), "numero eventi", "lezione", c_x_i, c_y+3, option_x)
            #--
        return
