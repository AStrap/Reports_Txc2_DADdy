# -*- coding: utf-8 -*-

import utility.info_vision as info_vision

class Info_users:

    def __init__(self, dm):

        #-- data_manager
        self.dm = dm
        #--

        return

    """
        Calcolo informazioni riguardo l'utente
    """
    def compute_info_users(self, id_course):

        #-- lista utenti
        # [id_utente, numero sessioni, perc. media di visione delle lezioni, #eventi, #pause, #backward, velocità media visione]
        # ordinati per perc. media di visione
        users_info = list()
        #--

        for id_user in self.dm.get_users_by_course(id_course):

            n_sessions, lectures = self.compute_sessions_lectures(id_course, id_user)

            lect_max_vision = self.compute_lecture_max_vision(id_course, id_user)

            perc_average_vision = self.compute_average_vision(id_course, id_user, lectures)

            n_events = self.compute_n_events(id_course, id_user)

            n_pauses = self.compute_n_pauses(id_course, id_user)

            n_backwards = self.compute_n_backward(id_course, id_user)

            users_info.append([id_user, n_sessions, len(lectures), perc_average_vision, lect_max_vision, n_events, n_pauses, n_backwards])

        users_info.sort( key=lambda x:x[1], reverse=True)

        return users_info

    """
        Calcolo sessioni istanziate e lezioni frequentate dall'utente
    """
    def compute_sessions_lectures(self, id_course, id_user):
        sessions = self.dm.get_session_by_course_user(id_course, id_user)

        lectures = list()
        for s in sessions:
            if not s[-2] in lectures:
                lectures.append(s[-2])

        return len(sessions), lectures

    """
        Calcolo della lezione più vista da parte dell'utente
    """
    def compute_lecture_max_vision(self, id_course, id_user):
        lect_max_vision = ["", 0]
        for l in self.dm.get_lectures_by_course(id_course):
            tot_vision = info_vision.compute_user_tot_vision_lecture(self.dm, id_user, l, id_course)

            if tot_vision > lect_max_vision[1]:
                lect_max_vision[0] = self.dm.get_lecture_name(l)
                lect_max_vision[1] = tot_vision

        return lect_max_vision[0]

    """
        Calcolo della percentuale media di visione tra tutte le lezioni viste
        dall'utente
    """
    def compute_average_vision(self, id_course, id_user, lectures):

        tot = 0
        lect_max_vision = ["", 0]
        for l in lectures:
            perc_vision = info_vision.compute_user_perc_vision_lecture(self.dm, id_user, l, id_course)

            tot += perc_vision

            if perc_vision > lect_max_vision[1]:
                lect_max_vision[0] = self.dm.get_lecture_name(l)
                lect_max_vision[1] = perc_vision

        n_lectures = len(lectures)
        average_vision = round((tot/n_lectures), 2)

        return average_vision

    """
        Calcolo numero di eventi eseguiti dall'utente
    """
    def compute_n_events(self, id_course, id_user):
        n_events = 0

        for s in self.dm.get_session_by_course_user(id_course, id_user):
            n_events += len(s[3])

        return n_events

    """
        Calcolo numero di pause eseguite dall'utente
    """
    def compute_n_pauses(self, id_course, id_user):
        n_pauses = 0

        for s in self.dm.get_session_by_course_user(id_course, id_user):

            for e in s[3]:
                if e[0] == "PS":
                    n_pauses += 1

        return n_pauses

    """
        Calcolo numero di eventi backward eseguiti dall'utente
    """
    def compute_n_backward(self, id_course, id_user):
        n_backwards = 0

        for s in self.dm.get_session_by_course_user(id_course, id_user):

            lecture_duration = self.dm.get_lecture_duration(s[-2])

            t_lec_pr = 0; t_ses_pr = 0
            t_lec_cor = 0; t_ses_cor = 0; v_cor = 1; play=0
            for e in s[3]:
                t_lec_cor = e[2]; t_ses_cor = e[1]

                if play:
                    diff = t_ses_cor-t_ses_pr
                    if t_lec_pr+(diff*v_cor) <= lecture_duration:
                        t_lec_pr += diff*v_cor


                if e[0] == "SK":
                    if t_lec_cor < t_lec_pr:
                        n_backwards += 1
                elif e[0] == "S0":
                    v_cor = 1
                elif e[0] == "S1":
                    v_cor = 1.25
                elif e[0] == "S2":
                    v_cor = 1.5
                elif e[0] == "S3":
                    v_cor = 1.75
                elif e[0] == "S4":
                    v_cor = 2
                elif e[0]=="PL":
                    play = 1
                elif e[0]=="PS":
                    play = 0

                if (e[0]!="SL" and e[0]!="DL") or e[2]!=0:
                    t_lec_pr = t_lec_cor; t_ses_pr = t_ses_cor


        return n_backwards
