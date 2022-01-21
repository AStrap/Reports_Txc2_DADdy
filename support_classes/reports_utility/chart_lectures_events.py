# -*- coding: utf-8 -*-

import config
import utility.time_date as time_date

class Chart_lectures_events:
    
    PATH_OUTPUT = config.PATH_OUTPUT
    
    def __init__(self, dm, em):
        # data manager
        self.dm = dm
        
        # excel manager
        self.em = em
        
        return

    """
        Calcolo e stampa dei grafici riguardo un corso
    """
    def compute_print(self, id_course, label_period, period):
        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))
        
        workbook_name = "lezioni_eventi_%s_%s.xlsx" %(label_period, self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)
        
        self.compute_events_per_lecture("Eventi_per_lezione", id_course, label_period, period)
        
        self.em.close_workbook()
        return workbook_name
    
    """
        Calcolo e stampa del numero di utenti per lezione
    """
    def compute_events_per_lecture(self, sheet, id_course, label_period, period):
        
        self.em.add_worksheet(sheet)
        self.em.set_cursors(1, 1)
        
        #-- sessioni per giornata
        c_x_i, c_y = self.em.get_cursors()
        
        head = [["LEZIONE", "NUMERO EVENTI"]]
        body = []
        
        #-- giorni da considerare
        days = time_date.get_days_by_period(period)
        #--
        
        max_events = 0
        for l in self.dm.get_lectures_by_course(id_course):
            sessions = self.dm.get_sessions_by_course_lecture_days(id_course, l, days)
            
            n_events = 0
            for s in sessions:
                for i,e in enumerate(s[3]):
                    if e[0] in ["PL", "PS", "SC", "SL", "KW", "SK", "BM"]:
                        if e[0] in ["SL", "SC", "KW"]:
                            if i+1 != len(s[3]) and s[3][i+1]=="SK":
                                n_events -= 1
                        n_events += 1
            
            body.append([self.dm.get_lecture_name(l), n_events])
            if n_events>max_events:
                max_events = n_events
                
        option_x = dict()
        if max_events < 10:
            option_x['major_unit'] = 1
            
        self.em.write_head_table(head)
        self.em.write_body_table(body)
        
        c_x, c_y = self.em.get_cursors()
        
        self.em.print_bar_chart("ver", (c_x_i+1,c_x-1), (c_y, c_y+1), sheet, "Eventi per lezione - %s" %(label_period), "numero eventi", "lezione", c_x_i, c_y+3, option_x)
        #--
        return
    
