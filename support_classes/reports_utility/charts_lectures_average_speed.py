# -*- coding: utf-8 -*-
import math
import datetime

import config

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
        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        workbook_name = "average_speed_%s.xlsx" %(self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)

        self.compute_support("Supporto_grafici", id_course)

        self.print_charts_average_speed("Velocita_di_visione", "Supporto_grafici", id_course)

        self.em.close_workbook()

        return workbook_name

    """
        Calcolo e produzione del foglio di supporto per studio delle velocità
        medie di visione

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - id_course: str
                corso di riferimento
    """
    def compute_support(self, sheet, id_course):

        self.em.add_worksheet(sheet)

        for l in self.dm.get_lectures_by_course(id_course):

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = 10*60

            #-- calcolo velocità medie per lezione
            info_speed = self.compute_speed(l, self.dm.get_sessions_by_course_lecture(id_course, l))
            #--

            #-- scrittura elementi
            head = [[str(datetime.timedelta(seconds=i*self.UNIT)) for i in range(math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)+1)]]
            body = [[]]

            for i,s in enumerate(info_speed):
                tmp = ["" for _ in range(i)]
                tmp.append(s); tmp.append(s)
                body[0].extend(tmp)

            self.em.write_head_table(head)
            self.em.write_body_table(body)
            #--

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT
        return

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
            - sheet: str
                nome foglio su cui stampare i grafici

            - support_sheet: str
                nome foglio in cui presenti dati per grafici

            - id_course: str
                corso di riferimento
    """
    def print_charts_average_speed(self, sheet, support_sheet, id_course):

        for i,l in enumerate(self.dm.get_lectures_by_course(id_course)):

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = 10*60

            if i==0:
                self.em.add_worksheet_support_sheet("%s%d" %(sheet,i))
            else:
                self.em.add_worksheet("%s%d" %(sheet,i))

            x = [i*2, (i*2)+1]
            y = [0, math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)]

            #- inserimento dei skip
            c_y=0
            # spazi bianchi
            s=0
            while s<math.ceil(self.dm.get_lecture_duration(l)/self.UNIT):
                y_s = c_y; y_e = c_y+s+1
                y.append((y_s, y_e))

                c_y += s+2
                s += 1

            title = "Velocità media - %s" %(self.dm.get_lecture_name(l))
            self.em.print_line_chart_speed(x, y, support_sheet, title, "minutaggio", "livello di velocità", 1, 1, {"max":4, "min":0, 'major_unit':1})

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT

        return
