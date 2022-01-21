# -*- coding: utf-8 -*-
import math

import config
import utility.time_date as time_date

class Charts_lectures_vision:

    PATH_OUTPUT = config.PATH_OUTPUT
    UNIT = config.TIME_UNIT     

    def __init__(self, dm, em):

        # data manager
        self.dm = dm

        # excel manager
        self.em = em

        self.max_y = 0
        return

    def compute_print(self, id_course):
        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        workbook_name = "copertura_visione_lezione_%s.xlsx" %(self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)

        self.compute_support("Supporto_grafici", id_course)

        self.compute_lecture_vision("Coperura di visione", "Supporto_grafici", id_course)

        self.em.close_workbook()
        
        return workbook_name

    #-
    # Calcolo e produzione del foglio di supporto per studio dei vari punti di
    # interesse, in base a particolari criteri
    #-
    def compute_support(self, sheet, id_course):

        self.em.add_worksheet(sheet)

        for l in self.dm.get_lectures_by_course(id_course):

            #-- calcolo informazioni riguardo la visione
            total_vision, info_vision = self.compute_n_visione(id_course, l)
            #--

            #-- scrittura elementi
            head = [[str(time_date.seconds_hours(seconds=i*self.UNIT)) for i in range(math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)+1)]]
            body = [total_vision, info_vision]

            self.em.write_head_table(head)
            self.em.write_body_table(body)
            #--
        return

    #-
    # stampa i grafici delle distribuzione di visione
    #-
    def compute_lecture_vision(self, sheet, support_sheet, id_course):

        for i,l in enumerate(self.dm.get_lectures_by_course(id_course)):

            if i==0:
                self.em.add_worksheet_support_sheet("%s%d" %(sheet,i))
            else:
                self.em.add_worksheet("%s%d" %(sheet,i))

            ind_labels = i*2+i
            duration = math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)


            title = "Coperture di visone - %s" %(self.dm.get_lecture_name(l))
            self.em.print_line_chart("oriz", (ind_labels,ind_labels+1), (0, duration), support_sheet, title, "minutaggio", "numero visioni", 1, 1, {'min':0})

            title = "Coperture di visone univoca per utente - %s" %(self.dm.get_lecture_name(l))
            if self.max_y > 20:
                unit = 10
            else:
                unit = 1
            self.em.print_line_chart("oriz", (ind_labels,ind_labels+2), (0, duration), support_sheet, title, "minutaggio", "numero visioni", 1, 14, {'min':0, 'major_unit':unit})


        return

    # calcolo numero visioni
    def compute_n_visione(self, id_course, id_lecture):

        total_vision = [0 for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]
        lecture_users = [[] for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]

        sessions = self.dm.get_sessions_by_course_lecture(id_course, id_lecture)

        for s in sessions:
            user = s[-1]
            play=0; speed=1

            t_ses_pr=0; t_lec_pr = 0
            for e in s[3]:
                event = e[0]; t_ses = e[1]; t_lec=e[2]
                if event in ["SL","KW"] and t_lec==0:
                    continue
                elif event == "DL":
                    continue

                if play:
                    if event!="SK" :
                        if t_lec>t_lec_pr:
                            # controllo intervallo
                            while t_lec_pr<t_lec:
                                total_vision[round(t_lec_pr/self.UNIT)] += 1
                                if not user in lecture_users[round(t_lec_pr/self.UNIT)]:
                                    lecture_users[round(t_lec_pr/self.UNIT)].append(user)
                                t_lec_pr+=1
                    elif event=="SK":
                        date = time_date.get_datetime(s[0])
                        date_update_sk = time_date.get_datetime("2021-11-08")

                        if date > date_update_sk:
                            while t_lec_pr<e[3]:
                                total_vision[round(t_lec_pr/self.UNIT)] += 1
                                if not user in lecture_users[round(t_lec_pr/self.UNIT)]:
                                    lecture_users[round(t_lec_pr/self.UNIT)].append(user)
                                t_lec_pr+=1
                        else:
                            while t_ses_pr<t_ses:
                                if play and t_lec_pr<self.dm.get_lecture_duration(id_lecture):
                                    total_vision[round(t_lec_pr/self.UNIT)] += 1
                                    if not user in lecture_users[round(t_lec_pr/self.UNIT)]:
                                        lecture_users[round(t_lec_pr/self.UNIT)].append(user)
                                    t_lec_pr+=speed
                                    if speed==2 and (t_lec_pr-1)<self.dm.get_lecture_duration(id_lecture):
                                        total_vision[round(t_lec_pr/self.UNIT)] += 1
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

        lecture_scores=[0 for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]
        for i,users in enumerate(lecture_users):
            lecture_scores[i] = len(users)
            if len(users)>self.max_y:
                self.max_y = len(users)

        return total_vision, lecture_scores
