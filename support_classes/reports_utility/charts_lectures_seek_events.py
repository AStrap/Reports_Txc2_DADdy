# -*- coding: utf-8 -*-
import math
import datetime

import config

class Charts_lectures_seek_events:

    PATH_OUTPUT = config.PATH_OUTPUT
    UNIT = config.TIME_UNIT

    def __init__(self, dm, em):
        # data manager
        self.dm = dm

        # excel manager
        self.em = em

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
    def compute_print(self, id_course):

        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        workbook_name = "lectures_seek_events_%s.xlsx" %(self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)

        info_events = self.compute_support("Supporto_grafici", id_course)

        self.print_charts_average_speed("Seek_eventi", "Supporto_grafici", id_course, info_events)

        self.em.close_workbook()

        return workbook_name

    """
        Calcolo e produzione del foglio di supporto per studio della tipologia
        e numero di eventi che puntano ad uno specifico minutaggio

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - id_course: str
                corso di riferimento

        Return:
            - r_info_events: list()
                informazioni riguardo eventi di salto usati
    """
    def compute_support(self, sheet, id_course):

        self.em.add_worksheet(sheet)

        r_info_events = list()
        for l in self.dm.get_lectures_by_course(id_course):

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = 10*60

            #-- calcolo velocità medie per lezione
            info_events = self.compute_seek_events(l, self.dm.get_sessions_by_course_lecture(id_course, l))
            r_info_events.append(info_events)
            #--

            #-- scrittura elementi
            head = [[str(datetime.timedelta(seconds=i*self.UNIT)) for i in range(math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)+1)]]
            self.em.write_head_table(head)

            for i,type_seek in enumerate(info_events):
                body = [[]]

                for j,m in enumerate(type_seek):
                    if m != 0:
                        tmp = ["" for _ in range(j)]; tmp.append(m)
                        body[0].extend(tmp)

                self.em.write_body_table(body)

            self.em.add_row(1)
            #--

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT

        return r_info_events

    """
        Calcolo numero eventi per tipologie che puntano ad un certo minutaggio

        Parametri:
            - id_lecture: str
                lezione di riferimento

            - sessions: list()
                lista sessioni da considerare

        Return:
            - info_events: list()
                lista per ogni tipologia di seek,
                ogni lista divisa per unità di tempo, numero eventi in
                riferimento all'unità di tempo

                ind. 0 - backward seek
                ind. 1 - sezione seek
                ind. 2 - slide seek
                ind. 3 - keyword seek

    """
    def compute_seek_events(self, id_lecture, sessions):

        info_events = [[0 for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)] for _ in range(4)]

        t_lect_pr = 0
        for s in sessions:

            t_lect_pr = 0; t_ses_pr = 0
            speed = 0; play = 0;
            skip_event = False
            for i,e in enumerate(s[3]):
                event = e[0]; t_ses = e[1]; t_lect = int(e[2])

                if skip_event:
                    skip_event = False
                    t_lect_pr = t_lect
                    continue

                while t_ses_pr < t_ses:
                    if play and t_lect_pr<self.dm.get_lecture_duration(id_lecture):
                        t_lect_pr+=1
                        if speed == 2 and t_lect_pr<self.dm.get_lecture_duration(id_lecture):
                            t_lect_pr += 1
                        t_ses_pr+=1
                    else:
                        t_ses_pr = t_ses

                #-- verifica presenza salti
                if event == "SK":
                    if t_lect < t_lect_pr:
                        tmp = round(t_lect/self.UNIT)
                        info_events[0][tmp] += 1
                elif event == "SC" and i+1<len(s[3]) and s[3][i+1][0]=="SK":
                    tmp = round(s[3][i+1][2]/self.UNIT)
                    info_events[1][tmp] += 1
                    skip_event = True
                elif event=="SL" and i+1<len(s[3]) and s[3][i+1][0]=="SK":
                    tmp = round(s[3][i+1][2]/self.UNIT)
                    info_events[2][tmp] += 1
                    skip_event = True
                elif event=="KW" and i+1<len(s[3]) and s[3][i+1][0]=="SK":
                    tmp = round(s[3][i+1][2]/self.UNIT)
                    info_events[3][tmp] += 1
                    skip_event = True


                #-- aggiornamento del play e speed
                if event == "PL":
                    play = 1
                elif event == "PS":
                    play = 0
                elif event == "S0" or event == "S1":
                    speed = 1
                elif event == "S2" or event == "S3" or event == "S4":
                    speed = 2
                #--

        return info_events

    """
        Stampa dei grafici delle medie di velocità

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - support_sheet: str
                nome foglio in cui presenti dati per grafici

            - id_course: str
                corso di riferimento

            - info_events: list()
                informazioni sulle eventi di salto utilizzati
    """
    def print_charts_average_speed(self, sheet, support_sheet, id_course, info_events):

        for i,l in enumerate(self.dm.get_lectures_by_course(id_course)):

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = 10*60

            if i==0:
                self.em.add_worksheet_support_sheet("%s%d" %(sheet,i))
            else:
                self.em.add_worksheet("%s%d" %(sheet,i))

            x = [i*6, (i*6)+1, (i*6)+2, (i*6)+3, (i*6)+4, (i*6)+5]
            y = [0, math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)]

            title = "Numero eventi di salto temporale - %s" %(self.dm.get_lecture_name(l))
            self.em.print_line_chart_seek_events(x, y, info_events[i], support_sheet, title, "minutaggio", "numero di eventi", 1, 1, {"min":0})

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT

        return
