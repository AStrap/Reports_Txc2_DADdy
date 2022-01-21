# -*- coding: utf-8 -*-
"""
    Calcolo delle informazioni riguardo alla percentuale di corso vista dall'utente 
"""
def compute_user_perc_vision_course(dm, id_user, id_course):
    
    sessions = dm.get_session_by_course_user(id_course, id_user)

    sessions.sort(key=lambda x: (x[-3], x[-2]))
    
    #- calcolo visione per ogni lezione e totale
    tot = 0
    for l in dm.get_lectures_by_course(id_course):
        tot += compute_user_perc_vision_lecture(dm, id_user, l, id_course)
    #-
    
    return (tot*100)/(100*len(dm.get_lectures_by_course(id_course)))

#-
# Calcolo della percentuale di visione di una lezione date le sessioni
#-
def compute_user_perc_vision_lecture(dm, id_user, id_lecture, id_course):
    sessions = dm.get_sessions_by_lecture_user(id_course, id_lecture, id_user)
    
    duration = dm.get_lecture_duration(id_lecture)
    if duration==0:
        return 0
    
    seconds = [0 for _ in range(duration+1)]
    seconds_seen = 0
    
    for s in sessions:
        play=0; speed=1
            
        t_ses_pr=0; t_lec_pr = 0
        for e in s[3]:
            t_ses = e[1]; t_lec=e[2]
            
            #-- controllo intervallo
            while t_ses_pr<t_ses:
                if play and t_lec_pr<duration:
                    if seconds[t_lec_pr]==0:
                        seconds[t_lec_pr]=1
                        seconds_seen += 1
                    t_lec_pr+=speed
                    if speed==2 and (t_lec_pr-1)<duration:
                        if seconds[t_lec_pr-1]==0:
                            seconds[t_lec_pr-1]=1
                            seconds_seen += 1
                t_ses_pr+=1;
            #--   
        
            #-- aggiornamento del play
            if e[0]=="PL":
                play = 1
            elif e[0]=="PS":
                play = 0
            elif e[0]=="S0" or e[0]=="S1":
                speed = 1
            elif e[0]=="S2" or e[0]=="S3" or e[0]=="S4":
                speed = 2
            #--
        
            t_lec_pr = t_lec; t_ses_pr = t_ses
    
    
    return (seconds_seen*100)/duration 

#-
# Calcolo tempo totale visione della lezione
#-
def compute_user_tot_vision_lecture(dm, id_user, id_lecture, id_course):
    sessions = dm.get_sessions_by_lecture_user(id_course, id_lecture, id_user)
    
    duration = dm.get_lecture_duration(id_lecture)
    if duration==0:
        return 0

    seconds_seen = 0
    
    for s in sessions:
        play=0; speed=1
            
        t_ses_pr=0; t_lec_pr = 0
        for e in s[3]:
            t_ses = e[1]; t_lec=e[2]
            
            #-- controllo intervallo
            while t_ses_pr<t_ses:
                if play and t_lec_pr<duration:
                    seconds_seen += 1
                    t_lec_pr+=speed
                    if speed==2 and (t_lec_pr-1)<duration:
                        seconds_seen += 1
                t_ses_pr+=1;
            #--   
        
            #-- aggiornamento del play
            if e[0]=="PL":
                play = 1
            elif e[0]=="PS":
                play = 0
            elif e[0]=="S0" or e[0]=="S1":
                speed = 1
            elif e[0]=="S2" or e[0]=="S3" or e[0]=="S4":
                speed = 2
            #--
        
            t_lec_pr = t_lec; t_ses_pr = t_ses
    
    
    return seconds_seen




