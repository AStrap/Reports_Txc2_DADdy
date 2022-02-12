# -*- coding: utf-8 -*-

import utility.info_vision as info_vision

class Info_lectures:

    def __init__(self, dm):

        #-- data_manager
        self.dm = dm
        #--

        return

    """
        Calcolo informazioni riguardo una lezione

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - lectures_info: list() (es. [nome lezione, #utenti, #sessioni, #download, % media di visione per ogni utente])
                informazioni riguardo le lezioni

    """
    def compute_info_lectures(self, id_course):

        #-- lista utenti
        # [nome lezione, #utenti, #sessioni, #download, % media di visione per ogni utente]
        lectures_info = list()
        #--

        for id_lecture in self.dm.get_lectures_by_course(id_course):

            name_lecture = self.dm.get_lecture_name(id_lecture)

            n_users = len(self.dm.get_users_by_course_lecture(id_course, id_lecture))

            n_sessions = len(self.dm.get_sessions_by_course_lecture(id_course, id_lecture))

            n_download = self.compute_n_download(id_course, id_lecture)

            perc_average_vision = self.compute_average_vision(id_course, id_lecture)

            lectures_info.append([name_lecture, n_users, n_sessions, n_download, str(perc_average_vision)])

        return lectures_info

    """
        Return numero download eseguiti per una lezione

        Parametri:
            - id_course: str
                corso di riferimento

            - id_lecture: str
                lezione di riferimento

        Return:
            - n_download: int
                numero download eseguiti della lezione considerata
    """
    def compute_n_download(self, id_course, id_lecture):

        users = list()

        n_download = 0
        for session in self.dm.get_sessions_by_course_lecture(id_course, id_lecture):

            for e in session[3]:
                if e[0] == "DL":
                    if not session[-1] in users:
                        n_download += 1
                        users.append(session[-1])
                    break

        return n_download

    """
        Return percentuale media di visione di ogni utente

        Parametri:
            - id_course: str
                corso di riferimento

            - id_lecture: str
                lezione di riferimento

        Return:
            - average_vision: float
                percentuale di visione media tra tutti gli utenti che hanno
                visto la lezione
    """
    def compute_average_vision(self, id_course, id_lecture):
        tot = 0
        users = self.dm.get_users_by_course_lecture(id_course, id_lecture)

        for id_user in users:
            tot += info_vision.compute_user_perc_vision_lecture(self.dm, id_user, id_lecture, id_course)

        average_vision = 0
        if len(users)>0:
            average_vision = round((tot/len(users)), 2)

        return average_vision
