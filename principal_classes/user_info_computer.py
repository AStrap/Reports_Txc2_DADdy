# -*- coding: utf-8 -*-
import os
import csv
import math

import config

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
        
        with open(output_file, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            for id_user in self.dm.get_users_by_course(id_course):
                user_info = self.get_user_frequencies(id_course, id_user)
                spamwriter.writerow([id_user]+user_info)
                
        return
    
    
    """
        Calcolo delle varie frequenze richieste
    """
    def get_user_frequencies(self, id_course, id_user):
        
        sessions = self.dm.get_session_by_course_user(id_course, id_user)

        # play, pause, download, condition, seek, slide, keyword, bookmark, resume  
        user_info = [0 for _ in range(9)]
        
        tot_time_vision = 0
        for s in sessions:
            tot_time_vision += s[5]
            
            skip_event = False
            for i,e in enumerate(s[3]):
                
                if skip_event:
                    skip_event = False
                    continue
                
                if e[0]=="PL":
                    user_info[0] += 1
                elif e[0]=="PS":
                    user_info[1] += 1
                elif e[0]=="DL":
                    user_info[2] += 1
                elif e[0]=="F0" or e[0]=="F1" or e[0]=="T0" or e[0]=="T1" or e[0]=="S0" or e[0]=="S1" or e[0]=="S2" or e[0]=="S3" or e[0]=="S4":
                    user_info[3] += 1
                elif e[0] == "SK":
                    user_info[4] += 1
                elif e[0]=="SC" and i+1<len(e) and s[3][i+1]=="SK":
                    user_info[4] += 1
                    skip_event = True
                elif e[0] == "SL":
                    user_info[5] += 1
                elif e[0]=="SL" and i+1<len(e) and s[3][i+1]=="SK":
                    user_info[5] += 1
                    skip_event = True
                elif e[0] == "KW":
                    user_info[6] += 1
                elif e[0]=="KW" and i+1<len(e) and s[3][i+1]=="SK":
                    user_info[6] += 1
                    skip_event = True
                elif e[0] == "BM":
                    user_info[7] += 1
                elif e[0] == "RS":
                    user_info[8] += 1
        
        for i,info in enumerate(user_info):
            user_info[i] = info/float(tot_time_vision)
        
        return user_info
        
    