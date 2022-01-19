# -*- coding: utf-8 -*-
import config
import utility.time_date as time_date

import support_classes.reports_utility.info_users as info_users

class Reports_manager:

    DATE_RANGE_STUDY = config.DATE_RANGE_STUDY

    def __init__(self, dm, em):

        #-- data_manager
        self.dm = dm
        #--        
        
        #-- excel_manager
        self.em = em
        #--

        return

    """
        Return data del primo video pubblicato e dell'ultimo video pubblicato 
    """
    def get_first_last_lecture_dates(self, id_course):
        lectures = self.dm.get_lectures_by_course(id_course)
             
        first_date = self.dm.get_lecture_release_date(lectures[0])[:10]
        last_date = self.dm.get_lecture_release_date(lectures[-1])[:10]
            
        return first_date, last_date
    
    """
        Return data del primo appello d'esame e del secondo appello d'esame 
    """
    def get_first_second_exam_dates(self, id_course):
        exam_dates = self.dm.get_exam_dates(id_course)
        
        return exam_dates[0], exam_dates[1]
    
    """
        Return intervalli di tempo dei due periodi
    """
    def get_periods(self, id_course):
        
        first_period = list(); second_period = list()
        
        first_lecture_date, last_lecture_date = self.get_first_last_lecture_dates(id_course)
        first_period.append(first_lecture_date)
        first_period.append(time_date.add_days(last_lecture_date, 2))
        
        tmp = time_date.get_datetime(time_date.add_days(last_lecture_date, 3))
        if tmp > time_date.get_datetime(self.DATE_RANGE_STUDY[1]):
            second_period=[str(tmp)[:10], "-"]
        else:
            second_period.append(str(tmp)[:10])
            second_period.append(self.DATE_RANGE_STUDY[1])
        
        return first_period, second_period
    
    """
        Return utenti dato id_corso e periodo di tempo
    """
    def users_period(self, period, id_course):
        
        days = time_date.get_days_by_period(period)
        
        users = list()
        
        for s in self.dm.get_sessions_by_course_days(id_course, days):
            if not s[-1] in users:
                users.append(s[-1])
                    
        return users
    
    
    """
        Return sessioni dato id_corso e periodo di tempo
    """
    def sessions_period(self, period, id_course):
        
        days = time_date.get_days_by_period(period)
        
        return self.dm.get_sessions_by_course_days(id_course, days)
    
    """
        Return informazioni riguardo un utente ed un corso specifico
    """
    def get_users_info(self, id_course):
        c_users = info_users.Info_users(self.dm)
        
        return c_users.compute_info_users(id_course)
    
    """
        Return informazioni riguardo le keywords cercate
    """
    def get_keywords(self, id_course):
        
        keywords = list()
        for id_lecture in self.dm.get_lectures_by_course(id_course): 
            tmp = list()
            for s in self.dm.get_sessions_by_course_lecture(id_course, id_lecture):
                for e in s[3]:
                    if e[0]=="KW":
                        keyword = e[3]
                        timestamp = time_date.seconds_hours(e[2])
                        tmp.append([keyword, self.dm.get_lecture_name(id_lecture), timestamp, s[-1]])
            tmp.sort(key=lambda x:x[2])
            keywords.extend(tmp)
        
        return keywords