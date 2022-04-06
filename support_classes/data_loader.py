# -*- coding: utf-8 -*-
import csv
import json
import codecs

import config
import utility.time_date as time_date

"""
    Caricamento dati dai file:
        YY-MM
            YYYY-MM-DD.json
        all_courses.csv
        all_lectures.csv
"""
class Data_loader:

    PATH_DATA = config.PATH_DATA
    DATE_RANGE_STUDY = config.DATE_RANGE_STUDY
    PATH_COURSES_DATA = config.PATH_COURSES_DATA
    PATH_LECTURES_DATA = config.PATH_LECTURES_DATA

    def __init__(self):
        #-- giorni compresi nel periodo di raccolta dati
        self.days = list()
        #--

        #-- dizionari dati base
        self.courses = dict()
        self.lectures = dict()
        self.users = dict()
        self.sessions = dict()
        #--

        #-- relazione corsi-lezioni N-N
        self.courses_lectures = dict()
        #--
        #-- relazione corsi-utenti N-N
        self.courses_users = dict()
        #--

        #-- corsi di test o corsi da non considerare
        self.test_courses = list()
        self.ign_courses = list()
        #--

        #-- dati mancanti
        self.miss_courses = list()
        self.miss_lectures = list()
        #--
        return


    """
        Caricamento dei dati dai file csv
    """
    def load_data(self):

        #-- calcolo giorni considerati
        self.days = time_date.get_days_by_period(self.DATE_RANGE_STUDY)
        #--

        #-- lettura dei dati riguardo corsi, lezioni e sessioni
        self.load_courses()
        self.load_lectures()
        self.load_sessions()
        #--

        return

    """
        Caricamento dei dati riguardo i corsi
    """
    def load_courses(self):

        #-- file .csv con informazioni dei corsi
        file_courses = self.PATH_COURSES_DATA
        #--

        #-- lettura informazioni
        with open(file_courses, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for i_r,row in enumerate(csv_reader):
                #se docente==-- allora corso di test da ignorare
                if row[2]!="--" and row[0]!="#" and i_r>0:
                    self.courses[row[0]] = [row[1],row[2],row[3],row[4]]
                    self.courses_lectures[row[0]] = list()
                    self.courses_users[row[0]] = list()
                elif i_r==0:
                    continue
                elif row[2]=="--":
                    self.test_courses.append(row[0])
                elif row[0]=="#":
                    self.ign_courses.append(row[1])
        #--

        return


    """
        Caricamento dei dati riguardo le lezioni caricate
    """
    def load_lectures(self):

        #-- file con informazioni delle lezioni
        file_lectures = self.PATH_LECTURES_DATA
        #--

        #-- lettura informazioni
        with open(file_lectures, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar=None)

            for i_r,row in enumerate(csv_reader):
                lectureUUID = row[0]
                n_added_courses = 0
                if row[1][0]!="\"":
                    courses = row[1]
                else:
                    courses = [row[1][1:]]
                    i=2
                    while row[i][-1] != "\"":
                        courses.append(row[i])
                        n_added_courses+=1
                        i+=1
                    courses.append(row[i][:-1])
                    n_added_courses+=1
                insertedAt = row[2+n_added_courses]
                title = row[3+n_added_courses]
                if len(row)>6+n_added_courses:
                    for i in range(len(row)+n_added_courses-6)[1:]:
                        title = "%s,%s" %(title, row[3+n_added_courses+i])
                    title = title[1:-1]

                duration = row[-2]
                turboDuration = row[-1]
                if i_r == 0:
                    continue

                if (time_date.cmp_dates(insertedAt[:10], self.days[-1]) <= 0) and (not courses in self.test_courses) and (not courses in self.ign_courses):

                    lecture_name = ""
                    for i,c in enumerate(title):
                        if c.isupper():
                            if i > 0 and title[i-1].islower():
                                lecture_name += " "
                        lecture_name += c
                    self.lectures[lectureUUID] = [lecture_name, insertedAt, int(duration), int(turboDuration)]
                    if type(courses) == list:
                        for c in courses:
                            if c in self.courses.keys():
                                self.courses_lectures[c].append(lectureUUID)
                    else:
                        if courses in self.courses.keys():
                            self.courses_lectures[courses].append(lectureUUID)
        #--

        return

    """
        Caricamento dei dati riguardo le sessioni
    """
    def load_sessions(self):
        path = self.PATH_DATA

        #-- lettura informazioni
        for day in self.days:
            y = day[2:4]; m = day[5:7]
            json_file = "%s\\%s-%s\\%s.json" %(path, y, m, day)
            try:
                with open(json_file, 'r') as json_f:
                    sessions = json.load(json_f)
                    for s in sessions:
                        id_session   = s["sessionId"]
                        id_course    = s["courseId"]
                        uuid_lecture = s["lectureUUID"]
                        id_user      = s["userId"]
                        user_agent   = s["userAgent"]
                        timestamp    = s["timestamp"]
                        events       = s["events"]
                        duration = events[-1][1] if len(events)>0 else 0
                        try:
                            # dato inserito dal 9/11
                            languageCode = s["languageCode"]
                        except:
                            languageCode = "null"

                        #-- ignorare sessioni di test
                        if id_course in self.test_courses or id_course in self.ign_courses:
                            continue
                        #--

                        #-- controlli conformita' informazioni corsi e lezione
                        miss = False
                        if not id_course in self.courses.keys():
                            if not id_course in self.miss_courses:
                                self.miss_courses.append(id_course)
                            miss = True
                        if not uuid_lecture in self.lectures.keys():
                            if not uuid_lecture in self.miss_lectures:
                                self.miss_lectures.append(uuid_lecture)
                            miss = True
                        if miss:
                            continue
                        #--

                        #- conversione delle durate turbo a durate normali
                        events = self.fix_turbo_timestamp(events, self.lectures[uuid_lecture][2], self.lectures[uuid_lecture][3])
                        #-

                        #- ottimizzazione dei ritardi di registrazione dei eventi salto
                        if time_date.cmp_dates(day, "2021-11-08") < 0:
                            events = self.fix_events(events)
                        #-

                        #-- eliminazione eventi con durata <5 minuti e visione lezione <1 minuto
                        if (len(events)==0) or (self.lecture_time_vision(events)<60) or (duration<(5*60)):
                            continue
                        #--

                        self.sessions[id_session] = [day, timestamp, user_agent, events, languageCode, duration, id_course, uuid_lecture, id_user]

                        #-- aggiornamento courses_lectures
                        if not uuid_lecture in self.courses_lectures[id_course]:
                            self.courses_lectures[id_course].append(uuid_lecture)
                        #--

                        #-- aggiornamento users e users_lectures
                        if not id_user in self.users.keys():
                            self.users[id_user] = list()

                        if not id_user in self.courses_users[id_course]:
                            self.courses_users[id_course].append(id_user)
                        #--

                        #-- controllo durata lezione
                        for e in events:
                            if e[2]>self.lectures[uuid_lecture][2]:
                                self.lectures[uuid_lecture][2] = e[2]
                        #--
            except:
                print("Mancata lettura: %s" %(json_file))
            #except Exception as e: print(e)
        #--
        return

    """
        Calcolo tempo totale di visione della lezione in base agli eventi

        Parametri:
            -events: list() (es. [['PL', 0 ,0], ['PS', 1, 1]])
                eventi eseguti dall'utente

        Return:
            - tot: int
                tempo totale di visione in secondi
    """
    def lecture_time_vision(self, events):
        play=0; tot=0;
        lect_pr=0

        ses_pr = 0
        for e in events:
            if play==1:
                if e[2]>lect_pr and e[0]!="SK":
                    tot += e[2]-lect_pr

            if e[0]=="PL":
                play=1
            elif e[0]=="PS":
                play=0

            if (e[0]!="SL" and e[0]!="DL") or e[2]!=0:
                lect_pr = e[2]

            ses_pr = e[1]
        return tot

    """
        Aggiustamento degli eventi di salto non precisi (risolto 8/11 dalla sorgente)

        Parametri:
            - events: list() (es. [['PL', 0 ,0], ['PS', 2, 2], ['SK', 2, 2]])
                eventi eseguiti dall'utente

        Return:
            - events: list() (es. [['PL', 0 ,0], ['SK', 2, 2], ['PS', 2, 2]])
                eventi migliorati
    """
    def fix_events(self, events):
        tmp_events = list()

        # minutaggio sessione e lezione precedente
        t_ses_pr=0; t_lec_pr=0;
        # minutaggio sessione e lezione corrente
        t_ses=0; t_lec=0
        e=""
        # indici da controllare sk "fuori posto"
        del_index = list()
        i=0

        #-- aggiustamento eventi
        for event in events:
            e=event[0]; t_ses=event[1]; t_lec=event[2]

            if e!="SK" and e!="DL" and e[0]!="T" and ((e!="SL" and e!="KW") or t_lec!=0) and abs(t_lec-t_lec_pr)>((t_ses-t_ses_pr)*2.5):
                tmp_events.append(["SK",t_ses,t_lec])
                del_index.append(i)
                i += 1

            tmp_events.append(event)
            i+=1

            if e!="DL" and (e!="SL" or e!="KW" or t_lec!=0):
                t_ses_pr = t_ses; t_lec_pr=t_lec
        #--

        #-- eliminazione SK dupplicati
        for i in del_index:
            end = False
            tmp = i
            i += 1

            while (i<len(tmp_events) and abs(tmp_events[i][1]-tmp_events[tmp][1])<5 and abs(tmp_events[i][2]-tmp_events[tmp][2])<3) and not end:
                if tmp_events[i][0]=="SK":
                    del tmp_events[i]
                    end = True
                i+=1
        #--

        return tmp_events

    """
        Aggiustamento degli eventi, conversione tutti i timestampa "turbo" a
        "normale" (in modalità turbo viene considerato come il timestamp di un
        video con durata minore, anche se è la stessa lezione)

        Parametri:
            - events: list() (es. [['PL', 0, 0], ['PS', 1, 1])
                eventi eseguiti dall'utente

            - duration: int
                durata "normale" della lezione

            -turbo_duration: int
                durata in modalita "turbo" della lezione (<"normale")

        Return:
            - events: list() (es. [['PL', 0 ,0], ['PS', 1, 1]])
                eventi migliorati
    """
    def fix_turbo_timestamp(self, events, duration, turbo_duration):
        tmp_events = list()

        turbo = False
        ignore_SK = False
        time_turbo=0
        for i,e in enumerate(events):
            if e[0]=="SK" and ignore_SK:
                ignore_SK = False
                continue

            if turbo:
                if e[0]=="SK":
                    try:
                        e[3] = round((e[3]*duration)/turbo_duration)
                        if e[3]>duration:
                            continue
                    except:
                        pass
                else:
                    if i>0:
                        if e[0]!="T0" or e[2]!=time_turbo:
                            if e[2]!=time_turbo:
                                e[2] = round((e[2]*duration)/turbo_duration)

            if e[0]=="T1":
                turbo = True
                time_turbo = e[2]

                tmp = i
                while tmp < i+3 and tmp<len(events):
                    if events[tmp][0]=="SK":
                        ignore_SK = True
                    tmp += 1
            elif e[0]=="T0":
                turbo = False

                tmp = i
                while tmp < i+3 and tmp<len(events):
                    if events[tmp][0]=="SK":
                        ignore_SK = True
                    tmp += 1

            tmp_events.append(e)

        return tmp_events


    #--------------------------------------------------------------------------

    """
        Return informazioni riguardo i corsi

        Return:
            - courses: dict() (es. {id_corso : ["nome corso", "nome docente", 2022-01-01, 2022-02-01]})
                informazioni riguardo i corsi
    """
    def get_courses(self):
        return self.courses

    """
        Return informazioni riguardo le lezioni

        Return:
            - lectures: dict() (es. {id_lezione : ["nome lezione", 2021-10-01T00:01:00.000000, 10000, 8000]})
                informazioni riguardo le lezioni
    """
    def get_lectures(self):
        return self.lectures

    """
        Return informazioni riguardo le sessioni

        Return:
            - sessions: dict() (se. {id_sessione : [ 2021-10-01, 2021-10-01T00:00:00.000000+02:00, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36", ["PL", 0, 0], "it", 10000, id_course, id_lecture, id_user]})
                informazioni riguardo le sessioni
    """
    def get_sessions(self):
        return self.sessions

    """
        Return informazioni riguardo gli utenti

        Return:
            - users: dict() (es. {id_user : []})
                informazioni riguardo gli utenti
    """
    def get_users(self):
        return self.sessions

    """
        Return informazioni riguardo le relazioni tra corsi e lezioni

        Return:
            - courses_lectures: dict() (es. {id_corso : [id_lezione1, id_lezione2]})
                lista lezioni che conpongono ogni corso

    """
    def get_courses_lectures(self):
        return self.courses_lectures

    """
        Return informazioni riguardo le relazioni tra corsi e utenti

        Return:
            - courses_users: dict() (es. {id_corso : [id_utente1, id_utente2]})
                lista utenti che hanno partecipato un corso
    """
    def get_courses_users(self):
        return self.courses_users

    """
        Return lista corsi e lezioni di cui mancano le informazioni

        Return:
            - miss_courses: list()
                lista corsi di cui mancano le informazioni

            - miss_lectures: list()
                lista lezioni di cui mancano le informazioni
    """
    def get_miss_info(self):
        return self.miss_courses, self.miss_lectures
