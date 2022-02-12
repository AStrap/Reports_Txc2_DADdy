# -*- coding: utf-8 -*-
import config
import utility.time_date as time_date

class Chart_sessions_hours_distribution:

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
        Calcolo e stampa dei grafici nella distribuzione di sessione nei vari
        periodi della giornata

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

        workbook_name = "sessions_hours_distribution_%s_%s.xlsx" %(label_period, self.dm.get_course_name(id_course))

        self.em.set_workbook(workbook_name, path_output_course)

        #-- giorni presenti nel periodo
        days_period = time_date.get_days_by_period(period)
        #--

        self.compute_sessions_per_hours("Sessioni_per_orario", id_course, label_period, period, days_period)

        self.em.close_workbook()

        return workbook_name


    """
        Calcolo e stampa delle informazioni di distribuzione delle sessioni nelle
        ore del giorno

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
                giorni da co

    """
    def compute_sessions_per_hours(self, sheet, id_course, label_period, period, days_period):

        self.em.add_worksheet(sheet)
        self.em.set_cursors(1, 1)

        #-- sessioni per giornata
        c_x_i, c_y = self.em.get_cursors()

        head = [["ORARIO", "NUMERO SESSIONI"]]
        body = []

        for h in range(24):
            body.append(["[%d,%d)"%(h,h+1),0])

        sessions = self.dm.get_sessions_by_course_days(id_course, days_period)

        for s in sessions:
            time = int(s[1][11:13])

            hours = 0
            while hours<=s[5]:
                body[time][1] += 1
                hours += 3600
                time = time+1 if time<23 else 0

        self.em.write_head_table(head)
        self.em.write_body_table(body)

        c_x, c_y = self.em.get_cursors()

        self.em.print_isto_chart("ver", (c_x_i+1,c_x-1), (c_y, c_y+1), sheet, "Sessioni attive per orario - %s" %(label_period), "orario", "numero sessioni", c_x_i, c_y+3, {'min':0})
        #--
        return
