# -*- coding: utf-8 -*-
import math

import support_classes.chart_printer as chart_printer

import config
import utility.time_date as time_date

class Charts_lectures_vision:

    PATH_OUTPUT = config.PATH_OUTPUT
    UNIT = config.TIME_UNIT

    def __init__(self, dm):

        #-- data manager
        self.dm = dm
        #--

        self.max_y = 0
        self.max_y2 = 0
        return

    """
        Calcolo e stampa grafici riguardo lo studio di visione delle lezioni da
        parte degli utenti

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def compute_print(self, id_course):
        path_output_course = "%s/%s-%s" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        val_x, val_y_vision, val_y_users = self.compute_data(id_course)

        self.compute_lecture_vision(id_course, val_x, val_y_vision, val_y_users, path_output_course)

        return

    """
        Calcolo e produzione del foglio di supporto per studio dei vari punti di
        interesse, in base a particolari criteri

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def compute_data(self, id_course):
        val_x = list(); val_y_vision = list(); val_y_users = list()

        for l in self.dm.get_lectures_by_course(id_course):

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = 10*60

            val_x.append([str(time_date.seconds_hours(seconds=i*self.UNIT)) for i in range(math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)+1)])

            #-- calcolo informazioni riguardo la visione
            val_y_vision.append(self.compute_n_vision(id_course, l))
            val_y_users.append(self.compute_n_vision_users(id_course, l))
            #--

            if self.dm.get_lecture_duration(l)>10000:
                self.UNIT = config.TIME_UNIT

        return val_x, val_y_vision, val_y_users

    """
        Stampa i grafici delle distribuzione di visione

        Parametri:
            - id_course: str
                corso di riferimento

            - val_x: list
                lista minutaggi della lezione

            - val_y_vision: list
                lista numero visioni per minutaggio

            - val_y_users: list
                lista numero utenti per minutaggio

            - path_output_course: str
                path output specifica per il corso considerato
    """
    def compute_lecture_vision(self, id_course, val_x, val_y_vision, val_y_users, path_output_course):

        for i,l in enumerate(self.dm.get_lectures_by_course(id_course)):

            # if self.dm.get_lecture_duration(l)>10000:
            #     self.UNIT = 10*60
            #
            # ind_labels = i*2+i
            # duration = math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)

            #-- stampa grafico visioni per minutaggio
            title = "Coperture di visone - %s" %(self.dm.get_lecture_name(l))
            if self.max_y > 20:
                unit = 10
            else:
                unit = 1
            cp = chart_printer.Chart_printer()
            cp.print_line_chart(val_x[i], val_y_vision[i], title, "minutaggio", "numero visioni", {'max':self.max_y, 'min':0, 'major_unit':unit}, path_output_course, "lezioni\\lezione_%d\\Visioni_lezione_%d"%(i,i))
            del cp
            #--

            #-- stampa grafico utenti per minutaggio
            title = "Coperture di visone univoca per utente - %s" %(self.dm.get_lecture_name(l))
            if self.max_y2 > 20:
                unit = 10
            else:
                unit = 1

            cp = chart_printer.Chart_printer()
            cp.print_line_chart(val_x[i], val_y_users[i], title, "minutaggio", "numero visioni", {'max':self.max_y2, 'min':0}, path_output_course, "lezioni\\lezione_%d\\Visioni_unic_lezione_%d"%(i,i))
            del cp
            #--

            # if self.dm.get_lecture_duration(l)>10000:
            #     self.UNIT = config.TIME_UNIT

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
