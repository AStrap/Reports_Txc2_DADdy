# -*- coding: utf-8 -*-
import math
import datetime

import config
import utility.chart_printer as chart_printer

class Charts_lectures_average_speed:

    PATH_OUTPUT = config.PATH_OUTPUT
    UNIT = config.TIME_UNIT

    def __init__(self, dm):
        #-- data manager
        self.dm = dm
        #--

        return

    """
        Calcolo e stampa grafici riguardo la velocità media di visione delle
        lezioni

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - workbook_name: str
                nome file excel in cui salvati i grafici
    """
    def compute_print(self, id_course):
        path_output_course = "%s\\%s-%s" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        val_x, val_y = self.compute_data(id_course)

        self.print_charts_average_speed(id_course, val_x, val_y, path_output_course)

        return

    """
        Calcolo e produzione del foglio di supporto per studio delle velocità
        medie di visione

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def compute_data(self, id_course):

        val_x = list(); val_y = list()

        for l in self.dm.get_lectures_by_course(id_course):

            #-- calcolo velocità medie per lezione
            info_speed = self.compute_speed(l, self.dm.get_sessions_by_course_lecture(id_course, l))
            #--

            #-- scrittura elementi
            val_x.append([str(datetime.timedelta(seconds=i*self.UNIT)) for i in range(math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)+1)])
            val_y.append([])

            for s in info_speed:
                val_y[-1].append(s)
            #--

        return val_x, val_y

    """
        Calcolo medie di velocità

        Parametri:
            - id_lecture: str
                lezione di riferimento

            - sessions: list()
                lista sessioni da considerare

        Return:
            - r_info_speed: list()
                media di velocità ogni unità di tempo
    """
    def compute_speed(self, id_lecture, sessions):

        info_speed = [[] for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]

        for s in sessions:
            #tempo lezione e velocita lezione correnti
            t_cor = 0; v_cor = 1; play=0
            for e in s[3]:
                if int(e[2])>t_cor:
                    if play == 1:
                        #aggiornamento velocita intervalli tra t_cor e t rispetto al evento
                        while int(e[2])>=t_cor:
                            info_speed[math.floor(t_cor/self.UNIT)].append(v_cor)
                            t_cor += self.UNIT
                t_cor = int(e[2])

                if e[0] in ["S0", "S1", "S2", "S3", "S4"]:
                    v_cor = int(e[0][1])
                elif e[0]=="PL":
                    play = 1
                elif e[0]=="PS":
                    play = 0


        r_info_speed = [0 for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]
        for i,inter in enumerate(info_speed):
            if len(inter)>0:
                # media velocità usata
                r_info_speed[i] = sum(inter)/len(inter)
            else:
                r_info_speed[i] = 0
        return r_info_speed

    """
        Stampa i grafici delle medie di velocità

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def print_charts_average_speed(self, id_course, val_x, val_y, path_output_course):

        for i,l in enumerate(self.dm.get_lectures_by_course(id_course)):

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = 10*60

            # x = [i*2, (i*2)+1]
            # y = [0, math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)]
            #
            # #- inserimento dei skip
            # c_y=0
            # # spazi bianchi
            # s=0
            # while s<math.ceil(self.dm.get_lecture_duration(l)/self.UNIT):
            #     y_s = c_y; y_e = c_y+s+1
            #     y.append((y_s, y_e))
            #
            #     c_y += s+2
            #     s += 1

            title = "Velocità media - %s" %(self.dm.get_lecture_name(l))
            cp = chart_printer.Chart_printer()
            cp.print_speed_chart(val_x[i], val_y[i], title, "minutaggio", "livello di velocità", {"max":4, "min":0, 'major_unit':1}, path_output_course, "lezioni\\lezione_%d\\Velocita_lezione_%d"%(i,i))
            del cp

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT

        return
