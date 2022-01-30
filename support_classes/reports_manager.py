# -*- coding: utf-8 -*-
import os

from win32com.client import Dispatch

import config
import utility.time_date as time_date

import support_classes.reports_utility.info_users as info_users
import support_classes.reports_utility.info_lectures as info_lectures
import support_classes.reports_utility.chart_lectures_events as chart_lectures_events
import support_classes.reports_utility.charts_sessions_days_distribution as charts_sessions_days_distribution
import support_classes.reports_utility.chart_sessions_hours_distribution as chart_sessions_hours_distribution
import support_classes.reports_utility.chart_course_vision as chart_course_vision
import support_classes.reports_utility.charts_lectures_average_speed as charts_lectures_average_speed
import support_classes.reports_utility.charts_lectures_vision as charts_lectures_vision
import support_classes.reports_utility.charts_lectures_seek_events as charts_lectures_seek_events
import support_classes.reports_utility.chart_user_agents as chart_user_agents

class Reports_manager:

    PATH_OUTPUT = config.PATH_OUTPUT
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
        Return informazioni generali riguardo le lezioni
    """
    def get_lectures_total_info(self, id_course):
        
        c_lectures = info_lectures.Info_lectures(self.dm)
        
        return c_lectures.compute_info_lectures(id_course)

    
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
    
    #- GRAFICI ----------------------------------------------------------------
    """
        Stampa i grafici riguardo il numero di eventi per lezione
    """
    def print_lectures_events(self, id_course, period, label_period):
        
        c_lectures_events = chart_lectures_events.Chart_lectures_events(self.dm, self.em)
        workbook = c_lectures_events.compute_print(id_course, label_period, period)
        self.save_chart(id_course, workbook, "lectures_events_%s" %(label_period))
        return
    
    """
        Stampa i grafici riguardo le sessioni distribuite per giorni e dalla 
        data di pubblicazione di una lezione
    """
    def print_session_day_distribution(self, id_course, period, label_period):
        
        c_sessions_day_distribution = charts_sessions_days_distribution.Charts_sessions_days_distribution(self.dm, self.em)
        workbook = c_sessions_day_distribution.compute_print(id_course, label_period, period)
        self.save_chart(id_course, workbook, "day_distribution_%s" %(label_period))
        
        return
    
    """
        Stampa i grafici riguardo le sessioni distribuite per giorni e dalla 
        data di pubblicazione di una lezione
    """
    def print_session_hours_distribution(self, id_course, period, label_period):
        
        c_sessions_hours_distribution = chart_sessions_hours_distribution.Chart_sessions_hours_distribution(self.dm, self.em)
        workbook = c_sessions_hours_distribution.compute_print(id_course, label_period, period)
        self.save_chart(id_course, workbook, "hours_distribution_%s" %(label_period))
        
        return
    
    """
        Stampa grafico che indica la copertura di visione del corso: numero 
        utenti per lezione
    """
    def print_course_vision(self, id_course, period, label_period):
        
        c_course_vision = chart_course_vision.Chart_course_vision(self.dm, self.em)
        workbook = c_course_vision.compute_print(id_course, label_period, period)
        self.save_chart(id_course, workbook, "course_vision_%s" %(label_period))
        
        return
    
    """
        Stampa grafico riguardo alla velocità media di visione di una lezione
    """
    def print_lectures_average_speed(self, id_course):
        
        c_charts_lectures_average_speed = charts_lectures_average_speed.Charts_lectures_average_speed(self.dm, self.em)
        workbook = c_charts_lectures_average_speed.compute_print(id_course)
        self.save_chart(id_course, workbook, "lecture_average_speed")
        
        return
    
    """
        Stampa grafico riguardo la copertura di visione della lezione
    """
    def print_lectures_vision(self, id_course):
        
        c_charts_lectures_vision = charts_lectures_vision.Charts_lectures_vision(self.dm, self.em)
        workbook = c_charts_lectures_vision.compute_print(id_course)
        self.save_chart(id_course, workbook, "lecture_vision")
        
        return
        
    """
        Stampa grafico riguardo la tipologia e il numero di eventi che puntano ad un specifico minutaggio 
    """
    def print_lectures_seek_events(self, id_course):
        
        c_charts_lectures_seek_events = charts_lectures_seek_events.Charts_lectures_seek_events(self.dm, self.em)
        workbook = c_charts_lectures_seek_events.compute_print(id_course)
        self.save_chart(id_course, workbook, "lecture_seek_events")
        
        return
    
    def print_user_agent_info(self, id_course):
        
        c_chart_user_agents = chart_user_agents.Chart_user_agents(self.dm, self.em)
        workbook = c_chart_user_agents.compute_print(id_course)
        self.save_chart(id_course, workbook, "user_agent")
        
        return
        
    #--------------------------------------------------------------------------  
    """
        Salvataggio grafici come immagini
    """
    def save_chart(self, id_course, workbook_name, sub_path):
        path = "%s\\%s-%s\\img" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))
        try:
            os.mkdir(path)
        except:
            pass
        path = "%s\\%s\\" %(path, sub_path)
        try:
            os.mkdir(path)
        except:
            pass
        
        app = Dispatch("Excel.Application")
        workbook_file_name = "%s\\%s-%s\\%s" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course), workbook_name)
        workbook = app.Workbooks.Open(Filename=workbook_file_name)
        
        #WARNING: The following line will cause the script to discard any unsaved changes in your workbook
        app.DisplayAlerts = False
        
        i = 1
        for sheet in workbook.Worksheets:
            for chartObject in sheet.ChartObjects():
                chartObject.Chart.Export("%s//chart"%(path) + str(i) + ".png")
                i += 1
        
        workbook.Close(SaveChanges=False, Filename=workbook_file_name)
    
        return