# -*- coding: utf-8 -*-
import config
import utility.time_date as time_date
import utility.chart_printer as chart_printer

class Chart_sessions_hours_distribution:

    PATH_OUTPUT = config.PATH_OUTPUT

    def __init__(self, dm):
        #-- data manager
        self.dm = dm
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
        path_output_course = "%s\\%s-%s" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        #-- giorni presenti nel periodo
        days_period = time_date.get_days_by_period(period)
        #--

        self.compute_sessions_per_hours(id_course, label_period, period, days_period, path_output_course)

        return


    """
        Calcolo e stampa delle informazioni di distribuzione delle sessioni nelle
        ore del giorno

        Parametri:

            - id_course: str
                corso di riferimento

            - label_period: str
                label come riferimento al periodo considerato

            - period: (str, str)
                periodo di studio

            - days_period: list() (es. ["YYYY-MM-DD", "YYYY-MM-DD"])
                giorni da cosiderare

    """
    def compute_sessions_per_hours(self, id_course, label_period, period, days_period, path_output_course):

        #-- sessioni per giornata

        val_x = list()
        for h in range(24):
            val_x.append("[%d,%d)"%(h,h+1))

        sessions = self.dm.get_sessions_by_course_days(id_course, days_period)

        val_y = [0 for _ in range(24)]
        for s in sessions:
            time = int(s[1][11:13])

            hours = 0
            while hours<=s[5]:
                val_y[time] += 1
                hours += 3600
                time = time+1 if time<23 else 0

        chart_printer.print_isto_chart(val_x, val_y, "Sessioni attive per orario - %s" %(label_period), "orario", "numero sessioni", {'min':0}, path_output_course, "Sessioni_orario_%s" %(label_period))
        #--
        return
