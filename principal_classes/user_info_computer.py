# -*- coding: utf-8 -*-
import csv

import config
import utility.info_vision as info_vision

class User_info_computer:
    
    PATH_OUTPUT = config.PATH_OUTPUT
    
    def __init__(self, dm):
        
        #-- data_manager
        self.dm = dm
        #--

        return
    
    """
        Calcolo e stampa delle informazioni degli utenti su csv
    """
    def compute_save(self, id_course):
        
        output_file = "%s\\_users_info\\%s-%s.csv"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))
        
        users_perc = list()
        
        with open(output_file, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            for id_user in self.dm.get_users_by_course(id_course):
                user_info = self.get_user_frequencies(id_course, id_user)
                perc_vision = info_vision.compute_user_perc_vision_course(self.dm, id_user, id_course)
                spamwriter.writerow(user_info+[id_user])
                
                users_perc.append((id_user, perc_vision))
        
        users_perc.sort(key=lambda x:x[1], reverse=True)
        
        print("\n%s-%s" %(id_course, self.dm.get_course_name(id_course)))
        for u,p in users_perc:
            print("\t%s: %f" %(u,p))
        return

    
    """
        Calcolo delle varie frequenze richieste
    """
    def get_user_frequencies(self, id_course, id_user):
        
        sessions = self.dm.get_session_by_course_user(id_course, id_user)

        # play_time_vision, pause_time_vision play, pause, condition, seek, slide, keyword, bookmark
        user_info = [0 for _ in range(9)]
        
        tot_time_vision = 0
        play = False; t_ses_pr = 0
        for s in sessions:
            tot_time_vision += s[5]
            
            skip_event = False
            for i,e in enumerate(s[3]):
                
                if e[1]>t_ses_pr and play:
                    user_info[0] += e[1]-t_ses_pr
                elif e[1]>t_ses_pr and not play:
                    user_info[1] += e[1]-t_ses_pr
                
                if skip_event:
                    skip_event = False
                    continue
                
                if e[0]=="PL":
                    user_info[2] += 1
                    play = True
                elif e[0]=="PS":
                    user_info[3] += 1
                    play = False
                elif e[0]=="F0" or e[0]=="F1" or e[0]=="T0" or e[0]=="T1" or e[0]=="S0" or e[0]=="S1" or e[0]=="S2" or e[0]=="S3" or e[0]=="S4":
                    user_info[4] += 1
                elif e[0] == "SK":
                    user_info[5] += 1
                elif e[0]=="SC" and i+1<len(e) and s[3][i+1]=="SK":
                    user_info[5] += 1
                    skip_event = True
                elif e[0] == "SL":
                    user_info[6] += 1
                elif e[0]=="SL" and i+1<len(e) and s[3][i+1]=="SK":
                    user_info[6] += 1
                    skip_event = True
                elif e[0] == "KW":
                    user_info[7] += 1
                elif e[0]=="KW" and i+1<len(e) and s[3][i+1]=="SK":
                    user_info[7] += 1
                    skip_event = True
                elif e[0] == "BM":
                    user_info[8] += 1
                    
                t_ses_pr = e[1]
        
        for i,info in enumerate(user_info[2:]):
            user_info[i+2] = info/float(tot_time_vision)
        
        return user_info
        
    