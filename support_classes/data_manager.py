# -*- coding: utf-8 -*-
import config
import support_classes.data_loader as data_loader

class Data_manager:

    PATH_PRJ = config.PATH_PRJ

    def __init__(self):
        #-- data loader per il caricamento dei dati
        self.dl = data_loader.Data_loader()
        #--

        #-pseodo DATABASE------------------------------------------------------

        # dizionario corsi     -  ID: [Nome, Docente, Primo appello, Secondo appello]
        self.courses = dict()
        # dizionario lezioni   -  ID: [Nome, Data_caricamento, durata, durata_turbo]
        self.lectures = dict()
        # dizionario utenti    -  ID: []
        self.users = dict()
        # dizionario sessioni  -  ID: [timestamp, userAgent, eventi, languageCode, durata, ID_corso, ID_lezione, ID_utente]
        self.sessions = dict()

        #-- RELAZIONI
        # dizionario corsi_lezioni(N-N) -  ID_CORSO: [lezioni]
        self.courses_lectures = dict()
        # dizionario corsi_utenti(N-N)  -  ID_CORSO: [utenti]
        self.courses_users = dict()
        #--

        #----------------------------------------------------------------------
        return

    """
        Lettura e caricamento dei dati
    """
    def load_data(self):

        #-- lettura e caricamento dei dati
        self.dl.load_data()
        self.courses = self.dl.get_courses()
        self.lectures = self.dl.get_lectures()
        self.users = self.dl.get_users()
        self.sessions = self.dl.get_sessions()
        
        self.courses_lectures = self.dl.get_courses_lectures()
        self.courses_users = self.dl.get_courses_users()
        #--

        return

    #-CORSI-------------------------------------------------------------------
    """
        Return inforamzioni sui corsi
    """
    def get_courses(self):
        return self.courses

    """
        Return nome di un corso specifico
    """
    def get_course_name(self, id_course):
        return self.courses[id_course][0]

    """
        Return docente di un corso specifico
    """
    def get_professor(self, id_course):
        return self.courses[id_course][1]

    """
        Return date esami di un corso specifico
    """
    def get_exam_dates(self, id_course):
        return (self.courses[id_course][2], self.courses[id_course][3])

    #-LEZIONI-----------------------------------------------------------------
    """
        Return informazioni sulle lezioni
    """
    def get_lectures(self):
        return self.lectures

    """
        Return nome di una lezione specifica
    """
    def get_lecture_name(self, id_lecture):
        return self.lectures[id_lecture][0]

    """
        Return data di pubblicazione di una lezione specifica
    """
    def get_lecture_release_date(self, id_lecture):
        return self.lectures[id_lecture][1]

    """
        Return durata normale di una lezione specifica
    """
    def get_lecture_duration(self, id_lecture):
        return self.lectures[id_lecture][2]

    """
        Return durata in modalità turbo di una lezione specifica
    """
    def get_lecture_turbo_duration(self, id_lecture):
        return self.lectures[id_lecture][3]

    """
        Return lista lezioni che compongono un corso
    """
    def get_lectures_by_course(self, id_course):
        lects = list()
        for l in self.courses_lectures[id_course]:
            lects.append((l, self.lectures[l][0], self.lectures[l][1]))
        lects.sort(key=lambda x: x[2])
        for i,l in enumerate(lects):
            lects[i] = l[0]
        return lects

    #-UTENTI-------------------------------------------------------------------
    """
        Return informazioni sugli utenti
    """
    def get_users(self):
        return self.users

    """
        Return utenti che hanno frequentato un specifico corso
    """
    def get_users_by_course(self, id_course):
        return self.courses_users[id_course]

    """
        Return utenti che hanno frequentato un corso e una lezione specifica
    """
    def get_users_by_course_lecture(self, id_course, id_lecture):
        sessions = self.get_sessions_by_course_lecture(id_course, id_lecture)
        r_users=list()
        for s in sessions:
            if not s[-1] in r_users:
                r_users.append(s[-1])
        return r_users
   

    #-SESSIONI----------------------------------------------------------------
    """
        Return informazioni sulle sessioni
    """
    def get_sessions(self):
        return self.sessions.values()

    """
        Return sessioni associate ad un corso
    """
    def get_sessions_by_course(self, id_course):
        r_sessions = list()
        for s in self.sessions.values():
            if s[-3]==id_course:
                r_sessions.append(s)
        r_sessions.sort(key=lambda x:x[2])
        return r_sessions

    """
        Return sessioni associati ad un corso e una lezione specifica
    """
    def get_sessions_by_course_lecture(self, id_course, id_lecture):
        r_sessions = list()
        for s in self.sessions.values():
            if s[-2]==id_lecture and s[-3]==id_course:
                r_sessions.append(s)
        r_sessions.sort(key=lambda x:x[1])
        return r_sessions

    """
        Return sessioni associati ad un corso in un periodo di giorni
        
        Parametri:
            id_course: string
                
            days: list()
                lista giorni in formato YYYY-MM-DD
    """
    def get_sessions_by_course_days(self, id_course, days):
        r_sessions = list()
        for day in days:
            tmp = list()
            for s in self.get_sessions_by_course(id_course):
                if s[0]==day:
                    tmp.append(s)
            r_sessions.extend(tmp)
        return r_sessions

    """
        Return sessioni di una data specifica
    """
    def get_sessions_by_day(self, day):
        r_sessions = list()
        for s in self.sessions.values():
            if s[0]==day:
                r_sessions.append(s)
        return r_sessions

    """
        Return sessioni associati ad un corso ed un utente specifico
    """
    def get_session_by_course_user(self, id_course, id_user):
        r_sessions = list()
        for s in self.get_sessions_by_course(id_course):
            if s[-1]==id_user:
                r_sessions.append(s)
        return r_sessions


    """
        Return sessioni associati ad un corso, una lezione ed un utente specifico
    """
    def get_sessions_by_lecture_user(self, id_course, id_lecture, id_user):
        r_sessions = list()
        for s in self.sessions.values():
            if s[-3]==id_course and s[-2]==id_lecture and s[-1]==id_user:
                r_sessions.append(s)
        return r_sessions


    """
        Return sessioni associati ad un corso in un periodo di giorni
        
        Parametri:
            id_course: string
            
            id_lecture: string
                
            days: list()
                lista giorni in formato YYYY-MM-DD
    """
    def get_sessions_by_course_lecture_days(self, id_course, id_lecture, days):
        r_sessions = list()
        for day in days:
            tmp = list()
            for s in self.get_sessions_by_course_lecture(id_course, id_lecture):
                if s[0]==day:
                    tmp.append(s)
            r_sessions.extend(tmp)
        return r_sessions