# -*- coding: utf-8 -*-
import csv
import json

import config
import utility.time_date as time_date

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

        #-- corsi di test da non considerare
        self.test_courses = list()
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

            for row in csv_reader:
                #se docente==-- allora corso di test da ignorare
                if row[2]!="--":
                    self.courses[row[0]] = [row[1],row[2],row[3],row[4]]
                    self.courses_lectures[row[0]] = list()
                    self.courses_users[row[0]] = list()
                else:
                    self.test_courses.append(row[0])
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
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                if (time_date.cmp_dates(row[2][:10], self.days[-1]) <= 0) and (not row[1] in self.test_courses):
                    self.lectures[row[0]] = [row[3], row[2], int(row[4]), int(row[5])]
                    self.courses_lectures[row[1]].append(row[0])
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
            
            with open(json_file, 'r') as json_file:
                sessions = json.load(json_file)
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
                    if id_course in self.test_courses:
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
                    
                    #-- controlli conformita' informazioni corsi e lezione
                    if not id_course in self.courses.keys():
                        print("Corso non presente: %s" % id_course)
                    if not uuid_lecture in self.lectures.keys():
                        print("Lezione non presente: %s" % uuid_lecture)
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
        #--
        return
    
    """
        Calcolo tempo totale di visione della lezione in base agli eventi
        
        Parametri:
            events: list()
            
        Return:
            tot: int
                tempo totale di visione
    """
    def lecture_time_vision(self, events):
        play=0; tot=0;
        lect_pr=0

        ses_pr = 0
        for e in events:
            if play==1:
                if e[2]>lect_pr and e[0]!="SK" and (e[1]-ses_pr)*2>=e[2]-lect_pr:
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
        Aggiustamento degli eventi di salto non precisi (risolto 8/11)

        Parametri:
            events: list()

        Return:
            events: list()
                eventi aggiustati
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

        # criteri di visulizzazione
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


        # eliminazione SK ritardati
        for i in del_index:
            end = False
            tmp = i
            i += 1

            while (i<len(tmp_events) and abs(tmp_events[i][1]-tmp_events[tmp][1])<5 and abs(tmp_events[i][2]-tmp_events[tmp][2])<3) and not end:
                if tmp_events[i][0]=="SK":
                    del tmp_events[i]
                    end = True
                i+=1

        return tmp_events

    """
        Aggiustamento degli eventi, conversione tutti i timestampa "turbo" a
        "normale"

        Parametri:
            events: list()

            duration: int
                durata "normale" della lezione

            turbo_duration: int
                durata "turbo" della lezione

        Return:
            events: list()
                eventi aggiustati
    """
    def fix_turbo_timestamp(self, events, duration, turbo_duration):
        tmp_events = list()

        turbo = False
        ignore_SK = False
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
                    e[2] = round((e[2]*duration)/turbo_duration)

            if e[0]=="T1":
                turbo = True

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
            courses: dict()
                id_corso : [nome_corso, docente, primo appello, secondo appello]          
    """
    def get_courses(self):
        return self.courses
    
    """
        Return informazioni riguardo le lezioni

        Return:
            lectures: dizionario
                id_lezione : [nome_lezione, data_caricamento, durata, durata_turbo]               
    """
    def get_lectures(self):
        return self.lectures

    """
        Return informazioni riguardo le sessioni

        Return:
            sessions: dizionario
                id_sessione : [ data, time_stamp, user_agent, events, languageCode, durata, id_course, id_lecture, id_user]          
    """
    def get_sessions(self):
        return self.sessions

    """
        Return informazioni riguardo gli utenti

        Return:
            users: dizionario
                id_user : []
    """
    def get_users(self):
        return self.sessions

    """
        Return informazioni riguardo le relazioni tra corsi e lezioni

        Return:
            courses_lectures: dizionario
                id_corso : [lista id lezioni] 
                
    """
    def get_courses_lectures(self):
        return self.courses_lectures
    
    """
        Return informazioni riguardo le relazioni tra corsi e utenti

        Return:
            courses_users: dizionario
                id_corso : [lista id utenti]           
    """
    def get_courses_users(self):
        return self.courses_users
    
    
    