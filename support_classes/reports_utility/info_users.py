# -*- coding: utf-8 -*-
import csv

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import config
import utility.info_vision as info_vision

class Info_users:

    PATH_OUTPUT = config.PATH_OUTPUT

    def __init__(self, dm):

        #-- data_manager
        self.dm = dm
        #--

        return

    """
        Calcolo informazioni riguardo l'utente

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - users_info: list() (es. [id_utente, numero sessioni, perc. media di visione delle lezioni, #eventi, #pause, #backward, velocità media visione])
                informazioni riguardo l'utente
    """
    def compute_info_users(self, id_course):

        #-- lista utenti
        # [id_utente, numero sessioni, perc. media di visione delle lezioni, #eventi, #pause, #backward, velocità media visione]
        # ordinati per perc. media di visione
        users_info = list()
        #--

        output_file = "%s\\%s-%s\\users_info.csv"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))
        output_csvfile = open(output_file, 'w', newline='')
        spamwriter = csv.writer(output_csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for id_user in self.dm.get_users_by_course(id_course):

            n_sessions, lectures = self.compute_sessions_lectures(id_course, id_user)

            lect_max_vision = self.compute_lecture_max_vision(id_course, id_user)

            perc_average_vision = self.compute_average_vision(id_course, id_user, lectures)

            n_events = self.compute_n_events(id_course, id_user)

            n_pauses = self.compute_n_pauses(id_course, id_user)

            n_backwards = self.compute_n_backward(id_course, id_user)

            users_info.append([id_user, n_sessions, len(lectures), perc_average_vision, lect_max_vision, n_events, n_pauses, n_backwards])

            perc_lectures = round((len(lectures)*100.00)/len(self.dm.get_lectures_by_course(id_course)), 2)
            course_vision = info_vision.compute_user_perc_vision_course(self.dm, id_user, id_course)
            spamwriter.writerow([perc_lectures,course_vision,perc_average_vision,id_user])

        users_info.sort( key=lambda x:x[1], reverse=True)

        output_csvfile.close()

        return users_info

    """
        Calcolo sessioni istanziate e lezioni frequentate dall'utente

        Parametri:
            - id_course: str
                corso di riferimento

            - id_user: str
                utente di riferimento

        Return:
            - numero sessioni: int
                numero sessioni istanziati dall'utente

            - lectures: list()
                lista lezioni che l'utente ha frequentato
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

        Parametri:
            - id_course: str
                corso di riferimento

            - id_user: str
                utente di riferimento

        Return:
            - lezione: str
                nome lezione più vista
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

        Parametri:
            - id_course: str
                corso di riferimento

            - id_user: str
                utente di riferimento

            - lectures: list()
                lista id lezioni da considerare

        Return:
            - average_vision: float
                percentuale di visione media delle lezioni considerate
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

        Parametri:
            - id_course: str
                corso di riferimento

            - id_user: str
                utente di riferimento

        Return:
            - n_events: int
                numero eventi eseguiti dall'utente
    """
    def compute_n_events(self, id_course, id_user):
        n_events = 0

        for s in self.dm.get_session_by_course_user(id_course, id_user):
            n_events += len(s[3])

        return n_events

    """
        Calcolo numero di pause eseguite dall'utente

        Parametri:
            - id_course: str
                corso di riferimento

            - id_user: str
                utente di riferimento

        Return:
            - n_pauses: int
                numero pause eseguite dall'utente
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

        Parametri:
            - id_course: str
                corso di riferimento

            - id_user: str
                utente di riferimento

        Return:
            - n_backwards: int
                numero backward eseguiti
    """
    def compute_n_backward(self, id_course, id_user):
        n_backwards = 0

        for s in self.dm.get_session_by_course_user(id_course, id_user):

            id_lecture = s[-2]

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
                        n_backwards += 1
                elif (event == "SC" or event=="SL" or event=="KW") and i+1<len(s[3]) and s[3][i+1][0]=="SK":
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

        return n_backwards

    #--------------------------------------------------------------------------

    """
        Calcolo cluster e componenti in base alla visione del corso e alla
        visione media delle lezioni

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - r_clusters: list()
                lista dei vari gruppi di divisione
    """
    def compute_clusters_activity(self, id_course):

        users = list()

        file_name = "%s\\%s-%s\\users_info.csv" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                users.append(row[-1])

        if len(users)<2:
            return []

        #-- letture dati da csv
        features = ["#lezioni","perc.visione corso","perc.visione media"]
        df = pd.read_csv(file_name, names=features+['target'])

        x = df.loc[:, features].values
        x = StandardScaler().fit_transform(x)
        #--

        #-- scelta numero di cluster
        n_clust = 2
        if len(users)>=6:
            n_clust = 4
        #--

        #-- esecuzione algoritmo pam
        kmeans = KMeans(n_clusters=n_clust).fit(x)
        results = kmeans.labels_
        #--

        clusters = [[] for _ in range(n_clust)]
        tot_perc_vision_clusters = [0 for _ in range(n_clust)]
        for i,r in enumerate(results):
            clusters[r].append(users[i])
            tot_perc_vision_clusters[r] += info_vision.compute_user_perc_vision_course(self.dm, users[i], id_course)

        for i,val in enumerate(tot_perc_vision_clusters):
            tot_perc_vision_clusters[i] = round(float(val)/len(clusters[i]),2)

        r_clusters = list()
        while len(clusters)>0:
            min_val = tot_perc_vision_clusters[0]
            min_ind = 0
            for i,val in enumerate(tot_perc_vision_clusters):
                if val < min_val:
                    min_val = tot_perc_vision_clusters[i]
                    min_ind = i

            r_clusters.insert(0,clusters[min_ind])
            del(clusters[min_ind])
            del(tot_perc_vision_clusters[min_ind])

        return r_clusters
