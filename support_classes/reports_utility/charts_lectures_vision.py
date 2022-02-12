# -*- coding: utf-8 -*-
import math

import config
import utility.time_date as time_date

class Charts_lectures_vision:

    PATH_OUTPUT = config.PATH_OUTPUT
    UNIT = config.TIME_UNIT

    def __init__(self, dm, em):

        #-- data manager
        self.dm = dm
        #--

        #-- excel manager
        self.em = em
        #--

        self.max_y = 0
        self.max_y2 = 0
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

        workbook_name = "copertura_visione_lezione_%s.xlsx" %(self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)

        self.compute_support("Supporto_grafici", id_course)

        self.compute_lecture_vision("Coperura di visione", "Supporto_grafici", id_course)

        self.em.close_workbook()

        return workbook_name

    """
        Calcolo e produzione del foglio di supporto per studio dei vari punti di
        interesse, in base a particolari criteri

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

            #-- calcolo informazioni riguardo la visione
            total_vision = self.compute_n_vision(id_course, l)
            user_vision = self.compute_n_vision_users(id_course, l)
            #--

            #-- scrittura elementi
            head = [[str(time_date.seconds_hours(seconds=i*self.UNIT)) for i in range(math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)+1)]]
            body = [total_vision, user_vision]

            self.em.write_head_table(head)
            self.em.write_body_table(body)
            #--

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT
        return

    """
        Stampa i grafici delle distribuzione di visione

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - support_sheet: str
                nome foglio in cui presenti dati per grafici

            - id_course: str
                corso di riferimento
    """
    def compute_lecture_vision(self, sheet, support_sheet, id_course):

        for i,l in enumerate(self.dm.get_lectures_by_course(id_course)):

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = 10*60

            if i==0:
                self.em.add_worksheet_support_sheet("%s%d" %(sheet,i))
            else:
                self.em.add_worksheet("%s%d" %(sheet,i))

            ind_labels = i*2+i
            duration = math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)


            title = "Coperture di visone - %s" %(self.dm.get_lecture_name(l))
            if self.max_y > 20:
                unit = 10
            else:
                unit = 1
            self.em.print_line_chart("oriz", (ind_labels,ind_labels+1), (0, duration), support_sheet, title, "minutaggio", "numero visioni", 1, 1, {'max':self.max_y, 'min':0, 'major_unit':unit})

            title = "Coperture di visone univoca per utente - %s" %(self.dm.get_lecture_name(l))
            if self.max_y2 > 20:
                unit = 10
            else:
                unit = 1
            self.em.print_line_chart("oriz", (ind_labels,ind_labels+2), (0, duration), support_sheet, title, "minutaggio", "numero visioni", 1, 14, {'max':self.max_y2, 'min':0, 'major_unit':unit})

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT

        return

    """
        Calcolo numero visioni della lezione

        Parametri:
            - id_course: str
                corso di riferimento

            - id_lecture: str
                lezione di riferimento

        Return:
            - total_vision: list()
                lista di numero visione per unità di tempo nella lezione

    """
    def compute_n_vision(self, id_course, id_lecture):

        total_vision = [0 for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]

        sessions = self.dm.get_sessions_by_course_lecture(id_course, id_lecture)

        cur_unit = -1
        for s in sessions:
            play=0; speed=1

            t_ses_pr = 0; t_lec_pr = 0
            for e in s[3]:
                event = e[0]; t_ses = e[1]; t_lec = e[2]
                if event in ["SL","KW"] and t_lec==0:
                    continue
                elif event == "DL":
                    continue

                if play:
                    if event!="SK" :
                        if t_lec>t_lec_pr:
                            # controllo intervallo
                            while t_lec_pr<t_lec:
                                tmp = round(t_lec_pr/self.UNIT)
                                if tmp != cur_unit:
                                    total_vision[tmp] += 1
                                    cur_unit=tmp
                                t_lec_pr+=1
                    elif event=="SK":
                        date = time_date.get_datetime(s[0])
                        date_update_sk = time_date.get_datetime("2021-11-08")

                        if date > date_update_sk:
                            while t_lec_pr<e[3]:
                                tmp = round(t_lec_pr/self.UNIT)
                                if tmp != cur_unit:
                                    total_vision[tmp] += 1
                                    cur_unit=tmp
                                t_lec_pr+=1
                        else:
                            while t_ses_pr<t_ses:
                                if play and t_lec_pr<self.dm.get_lecture_duration(id_lecture):
                                    tmp = round(t_lec_pr/self.UNIT)
                                    if tmp != cur_unit:
                                        total_vision[tmp] += 1
                                        cur_unit=tmp
                                    t_lec_pr+=speed
                                    if speed==2 and (t_lec_pr-1)<self.dm.get_lecture_duration(id_lecture):
                                        tmp = round((t_lec_pr-1)/self.UNIT)
                                        if tmp != cur_unit:
                                            total_vision[tmp] += 1
                                            cur_unit=tmp
                                    t_ses_pr+=1
                                else:
                                    t_ses_pr = t_ses

                #-- aggiornamento del play e speed
                if event=="PL":
                    play = 1
                elif event=="PS":
                    play = 0
                elif event=="S0" or event=="S1":
                    speed = 1
                elif event=="S2" or event=="S3" or event=="S4":
                    speed = 2
                #--

                t_lec_pr = t_lec; t_ses_pr = t_ses

        for y in total_vision:
            if y > self.max_y:
                self.max_y = y
        return total_vision

    """
        Calcolo numero visioni della lezione univoci per utente

        Parametri:
            - id_course: str
                corso di riferimento

            - id_lecture: str
                lezione di riferimento

        Return:
            - total_vision: list()
                lista di numero visione per unità di tempo nella lezione
    """
    def compute_n_vision_users(self, id_course, id_lecture):

        lecture_users = [[] for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]

        sessions = self.dm.get_sessions_by_course_lecture(id_course, id_lecture)

        for s in sessions:
            user = s[-1]
            play=0; speed=1

            t_ses_pr = 0; t_lec_pr = 0
            for e in s[3]:
                event = e[0]; t_ses = e[1]; t_lec = e[2]
                if event in ["SL","KW"] and t_lec==0:
                    continue
                elif event == "DL":
                    continue

                if play:
                    if event!="SK" :
                        if t_lec>t_lec_pr:
                            # controllo intervallo
                            while t_lec_pr<t_lec:
                                if not user in lecture_users[round(t_lec_pr/self.UNIT)]:
                                    lecture_users[round(t_lec_pr/self.UNIT)].append(user)
                                t_lec_pr += 1
                    elif event=="SK":
                        date = time_date.get_datetime(s[0])
                        date_update_sk = time_date.get_datetime("2021-11-08")

                        if date > date_update_sk:
                            while t_lec_pr<e[3]:
                                if not user in lecture_users[round(t_lec_pr/self.UNIT)]:
                                    lecture_users[round(t_lec_pr/self.UNIT)].append(user)
                                t_lec_pr+=1
                        else:
                            while t_ses_pr<t_ses:
                                if play and t_lec_pr<self.dm.get_lecture_duration(id_lecture):
                                    if not user in lecture_users[round(t_lec_pr/self.UNIT)]:
                                        lecture_users[round(t_lec_pr/self.UNIT)].append(user)
                                    t_lec_pr+=speed
                                    if speed==2 and (t_lec_pr-1)<self.dm.get_lecture_duration(id_lecture):
                                        if not user in lecture_users[round(t_lec_pr/self.UNIT)]:
                                            lecture_users[round(t_lec_pr/self.UNIT)].append(user)
                                t_ses_pr+=1;

                #-- aggiornamento del play e speed
                if event=="PL":
                    play = 1
                elif event=="PS":
                    play = 0
                elif event=="S0" or event=="S1":
                    speed = 1
                elif event=="S2" or event=="S3" or event=="S4":
                    speed = 2
                #--

                t_lec_pr = t_lec; t_ses_pr = t_ses

        lecture_vision=[0 for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]
        for i,users in enumerate(lecture_users):
            lecture_vision[i] = len(users)
            if len(users)>self.max_y2:
                self.max_y2 = len(users)

        return lecture_vision
